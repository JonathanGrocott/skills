#!/usr/bin/env python3
"""Preview or package project resources; never upload or modify the source."""
import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
from project_lib import MODULE, VIEWS, ProjectError, inspect, load_files, safe_name, validate


def select_files(files, views=(), resources=()):
    result = validate(files)
    if not result["ok"]:
        raise ProjectError("Source has structural errors; run validate_project.py first")
    inventory = inspect(files)
    known = set(inventory["resources"])
    selected = {VIEWS + safe_name(v) for v in views}
    selected.update(safe_name(r) for r in resources)
    if not selected:
        selected = set(known)
    if selected - known:
        raise ProjectError("Unknown resource(s): " + ", ".join(sorted(selected - known)))
    # Include discoverable local view, style and named-query dependencies to a fixed
    # point. Dynamic/script-only dependencies are reported for human/agent review.
    pending = True
    while pending:
        pending = False
        for ref in inventory["dependencies"]:
            if ref["dynamic"] or not any(ref["file"].startswith(r + "/") for r in selected):
                continue
            prefix = {"view": VIEWS, "style": MODULE + "/style-classes/", "query": "ignition/query/"}.get(ref["kind"])
            target = prefix + ref["target"] if prefix else None
            if target in known and target not in selected:
                selected.add(target)
                pending = True
    chosen = {"project.json": files["project.json"]}
    chosen.update({n: b for n, b in files.items() if any(n.startswith(r + "/") for r in selected)})
    refs = [r for r in inventory["dependencies"] if r["file"] in chosen]
    unresolved = []
    for ref in refs:
        prefix = {"view": VIEWS, "style": MODULE + "/style-classes/", "query": "ignition/query/"}.get(ref["kind"])
        if ref["dynamic"] or not prefix or prefix + ref["target"] not in selected:
            unresolved.append(ref)
    report = {"resources": sorted(selected), "files": sorted(chosen),
              "sha256": {n: hashlib.sha256(b).hexdigest() for n, b in sorted(chosen.items())},
              "dependencies_requiring_review": unresolved,
              "source_issues": result["issues"],
              "notes": ["project.json is retained; inspect enabled, parent and inheritance settings before Gateway import.",
                        "Gateway tags, connections, themes, images, modules and credentials are not bundled by this helper.",
                        "ZIP structure is not proof of import or runtime behavior. Import into a test project and read it back."]}
    return chosen, report


def write_archive(files, output):
    # Exclusive creation prevents an accidental overwrite, including the input ZIP.
    path = Path(output)
    if path.suffix.lower() != ".zip":
        raise ProjectError("Output must use a .zip extension")
    try:
        with path.open("xb") as stream:
            try:
                with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
                    for name, data in sorted(files.items()):
                        info = zipfile.ZipInfo(safe_name(name), (2020, 1, 1, 0, 0, 0))
                        info.compress_type = zipfile.ZIP_DEFLATED
                        info.external_attr = 0o100644 << 16
                        archive.writestr(info, data)
            except Exception:
                path.unlink(missing_ok=True)
                raise
    except OSError as exc:
        raise ProjectError("Cannot create output: {}".format(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Project directory or export ZIP")
    parser.add_argument("--view", action="append", default=[], help="View path; repeat to select several. Includes known local dependencies")
    parser.add_argument("--resource", action="append", default=[], help="Additional project-relative resource directory")
    parser.add_argument("--output", help="Create a new ZIP; omit for a read-only preview")
    args = parser.parse_args()
    try:
        chosen, report = select_files(load_files(args.source), args.view, args.resource)
        if args.output:
            output = Path(args.output).resolve()
            source = Path(args.source).resolve()
            if source.is_dir() and (output == source or source in output.parents):
                raise ProjectError("Place output outside the source project")
            write_archive(chosen, output)
            report["output"] = str(output)
        print(json.dumps(report, indent=2))
        return 0
    except ProjectError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
