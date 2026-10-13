"""Bounded, read-only project loading and conservative Perspective inspection.

Python 3.9+, standard library only. No Ignition runtime or expression evaluation.
"""
import json
import math
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

MODULE = "com.inductiveautomation.perspective"
VIEWS = MODULE + "/views/"
MAX_FILES = 10000
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024


class ProjectError(ValueError):
    pass


def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name or "\x00" in name:
        raise ProjectError("Unsafe resource path: {!r}".format(name))
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ("", ".", "..") for x in name.split("/")):
        raise ProjectError("Unsafe resource path: {!r}".format(name))
    return name


def parse_json(data, name):
    def pairs(items):
        obj = {}
        for k, v in items:
            if k in obj:
                raise ProjectError("Duplicate JSON key {!r} in {}".format(k, name))
            obj[k] = v
        return obj

    def constant(value):
        raise ProjectError("Non-finite JSON number {} in {}".format(value, name))

    def number(value):
        result = float(value)
        if not math.isfinite(result):
            return constant(value)
        return result

    try:
        return json.loads(data, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProjectError("Invalid JSON in {}: {}".format(name, exc)) from exc


def load_files(source):
    """Read a project directory or ZIP without extracting archive contents."""
    source = Path(source)
    if source.is_symlink():
        raise ProjectError("Source may not be a symbolic link")
    files = {}
    total = 0

    def add(name, size, read):
        nonlocal total
        safe_name(name)
        if name in files:
            raise ProjectError("Duplicate archive member: " + name)
        total += size
        if size > MAX_FILE or total > MAX_TOTAL or len(files) >= MAX_FILES:
            raise ProjectError("Project exceeds bounded loader limits")
        data = read()
        if len(data) != size:
            raise ProjectError("File changed while reading: " + name)
        files[name] = data

    try:
        if source.is_dir():
            for p in sorted(source.rglob("*")):
                if p.is_symlink():
                    raise ProjectError("Symbolic link in project: " + str(p))
                if p.is_file():
                    add(p.relative_to(source).as_posix(), p.stat().st_size, p.read_bytes)
        else:
            with zipfile.ZipFile(source) as archive:
                if len(archive.infolist()) > MAX_FILES:
                    raise ProjectError("Too many archive entries")
                for info in archive.infolist():
                    safe_name(info.filename.rstrip("/"))
                    if stat.S_ISLNK(info.external_attr >> 16):
                        raise ProjectError("Symbolic link in archive: " + info.filename)
                    if info.flag_bits & 1:
                        raise ProjectError("Encrypted archives are unsupported")
                    if not info.is_dir():
                        add(info.filename, info.file_size, lambda i=info: archive.read(i))
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise ProjectError("Cannot read project: {}".format(exc)) from exc
    # A Designer/Gateway export has project.json at its root. Accept one enclosing
    # directory, but never discard siblings outside the detected project root.
    if "project.json" not in files:
        candidates = [n for n in files if n.endswith("/project.json")]
        if len(candidates) != 1:
            raise ProjectError("Expected one project.json; select a single project directory/export")
        prefix = candidates[0][:-len("project.json")]
        if any(not n.startswith(prefix) for n in files):
            raise ProjectError("Files outside project root; select or re-export a single project")
        files = {n[len(prefix):]: b for n, b in files.items()}
    return files


def walk(value, path=""):
    yield path, value
    if isinstance(value, dict):
        for k, v in value.items():
            yield from walk(v, path + "/" + str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, path + "/" + str(i))


def documents(files):
    return {n: parse_json(b, n) for n, b in files.items() if n.endswith(".json")}


def view_name(filename):
    return filename[len(VIEWS):-len("/view.json")]


def dependencies(doc, filename):
    """Candidates, not a complete dependency graph. Scripts/dynamic paths need review."""
    found = []
    def add(kind, value, path, dynamic=False):
        if isinstance(value, str) and value:
            found.append({"kind": kind, "target": value, "file": filename,
                          "location": path, "dynamic": dynamic})
    for path, obj in walk(doc):
        if not isinstance(obj, dict):
            continue
        # Only properties of recognized embedding components are treated as paths.
        typ = obj.get("type", "")
        props = obj.get("props", {})
        if typ in ("ia.display.view", "ia.display.flex-repeater") and isinstance(props, dict):
            cfg = obj.get("propConfig", {})
            bound = isinstance(cfg, dict) and isinstance(cfg.get("props.path"), dict) and "binding" in cfg["props.path"]
            add("view", props.get("path"), path + "/props/path", bound)
        # viewPath is used by page configs, dashboard widgets, carousel, accordion,
        # and table renderers. Treat arbitrary data with this key as a candidate.
        if "viewPath" in obj:
            add("view", obj["viewPath"], path + "/viewPath", bool(obj.get("binding")))
        if typ == "ia.display.viewcanvas" and isinstance(props, dict):
            instances = props.get("instances", [])
            for i, instance in enumerate(instances if isinstance(instances, list) else []):
                if isinstance(instance, dict):
                    add("view", instance.get("viewPath", instance.get("path")), path + "/props/instances/" + str(i))
        binding = obj.get("binding")
        if isinstance(binding, dict):
            config = binding.get("config", {})
            if isinstance(config, dict):
                btype = binding.get("type")
                if btype == "tag":
                    add("tag", config.get("tagPath"), path, config.get("mode", "direct") != "direct")
                elif btype == "query":
                    add("query", config.get("queryPath"), path, config.get("pathMode", "direct") != "direct")
                elif btype in ("expr", "expr-struct", "http", "tag-history", "mongodb"):
                    add("manual", str(btype), path, True)
        classes = obj.get("classes")
        if isinstance(classes, str):
            for name in classes.split():
                add("style", name, path + "/classes")
        if isinstance(obj.get("script"), str):
            add("manual", "script dependencies", path + "/script", True)
    return found


def inspect(files):
    docs = documents(files)
    views = []
    refs = []
    resources = []
    for filename, doc in sorted(docs.items()):
        if filename.endswith("/resource.json"):
            resources.append(filename[:-len("/resource.json")])
        refs.extend(dependencies(doc, filename))
        if filename.startswith(VIEWS) and filename.endswith("/view.json"):
            nodes = [(p, x) for p, x in walk(doc.get("root", {})) if isinstance(x, dict) and isinstance(x.get("type"), str) and x["type"].startswith("ia.")] if isinstance(doc, dict) else []
            views.append({"name": view_name(filename), "file": filename,
                          "components": [{"location": p, "name": x.get("meta", {}).get("name") if isinstance(x.get("meta"), dict) else None, "type": x["type"]} for p, x in nodes]})
    return {"resources": resources, "views": views, "dependencies": refs,
            "limits": ["Dependency candidates only: computed paths, script references, inherited resources and external Gateway resources require review.",
                       "This tool does not execute Ignition expressions or Jython."]}


def validate(files):
    issues = []
    def issue(level, code, file, location, message):
        issues.append(dict(level=level, code=code, file=file, location=location, message=message))
    docs = documents(files)
    project = docs.get("project.json")
    if not isinstance(project, dict):
        issue("error", "project-shape", "project.json", "", "Project metadata must be an object")
    inherited = isinstance(project, dict) and bool(project.get("parent"))
    views = {view_name(n) for n in docs if n.startswith(VIEWS) and n.endswith("/view.json")}
    for filename, doc in docs.items():
        if filename.endswith("/resource.json"):
            if not isinstance(doc, dict) or not isinstance(doc.get("files"), list):
                issue("error", "manifest-shape", filename, "", "Resource manifest requires a files array")
                continue
            base = filename.rsplit("/", 1)[0]
            for member in doc["files"]:
                try:
                    safe_name(member)
                    if base + "/" + member not in files:
                        issue("error", "missing-data-file", filename, "files", "Missing manifest file: " + member)
                except ProjectError as exc:
                    issue("error", "unsafe-data-path", filename, "files", str(exc))
        if filename.startswith(VIEWS) and filename.endswith("/view.json"):
            manifest = filename.rsplit("/", 1)[0] + "/resource.json"
            if manifest not in files:
                issue("error", "missing-manifest", filename, "", "View resource.json is missing")
            elif isinstance(docs.get(manifest), dict) and isinstance(docs[manifest].get("files"), list) and "view.json" not in docs[manifest]["files"]:
                issue("error", "unlisted-view", manifest, "files", "Manifest does not list view.json")
            if not isinstance(doc, dict) or not isinstance(doc.get("root"), dict):
                issue("error", "view-root", filename, "root", "View requires one root component object")
                continue
            for key in ("props", "params", "custom", "propConfig"):
                if key in doc and not isinstance(doc[key], dict):
                    issue("error", "view-properties", filename, key, "Expected an object")
            if not str(doc["root"].get("type", "")).startswith("ia.container."):
                issue("warning", "root-type", filename, "root/type", "Confirm this is a registered container type in the target Gateway")
            def component(node, path):
                if not isinstance(node, dict):
                    issue("error", "component-shape", filename, path, "Component must be an object")
                    return
                if not isinstance(node.get("type"), str) or not node["type"]:
                    issue("error", "component-type", filename, path, "Component requires a type identifier")
                for key in ("props", "position", "meta", "custom", "propConfig", "events"):
                    if key in node and not isinstance(node[key], dict):
                        issue("error", "component-properties", filename, path + "/" + key, "Expected an object")
                children = node.get("children", [])
                if not isinstance(children, list):
                    issue("error", "children-shape", filename, path, "children must be an array")
                    return
                names = set()
                for i, child in enumerate(children):
                    if isinstance(child, dict) and isinstance(child.get("meta"), dict):
                        name = child["meta"].get("name")
                        if isinstance(name, str):
                            if name in names:
                                issue("error", "duplicate-sibling", filename, path, "Duplicate sibling name: " + name)
                            names.add(name)
                    component(child, path + "/children/" + str(i))
            component(doc["root"], "root")
        for path, obj in walk(doc):
            if not isinstance(obj, dict):
                continue
            if "binding" in obj and ("propConfig/" in path):
                b = obj["binding"]
                if not isinstance(b, dict) or not isinstance(b.get("type"), str) or not isinstance(b.get("config", {}), dict):
                    issue("error", "binding-shape", filename, path, "Binding requires a type and object configuration")
                elif b.get("type") not in ("tag", "property", "expr", "expr-struct", "query", "tag-history", "http", "mongodb"):
                    issue("warning", "unknown-binding", filename, path, "Confirm binding type against target module/version")
                if isinstance(b, dict) and "transforms" in b and not isinstance(b["transforms"], list):
                    issue("error", "transform-shape", filename, path, "transforms must be an array")
            if "paramDirection" in obj and obj["paramDirection"] not in ("input", "output", "inout"):
                issue("error", "parameter-direction", filename, path, "Expected input, output or inout")
    inventory = inspect(files)
    for ref in inventory["dependencies"]:
        if ref["kind"] == "view" and not ref["dynamic"] and ref["target"] not in views:
            issue("warning", "unresolved-view", ref["file"], ref["location"], "View dependency candidate not present{}: {}".format(" (project inherits resources)" if inherited else "", ref["target"]))
    return {"ok": not any(i["level"] == "error" for i in issues), "issues": issues,
            "view_count": len(views), "limits": inventory["limits"] + ["Static checks do not prove importability, component property validity, authorization, bindings, or runtime behavior."]}
