# Import, export and deployment

## Choose the right artifact

| Artifact | Intended use |
|---|---|
| Component clipboard content | Copy/paste inside a target-version Designer using its clipboard envelope |
| View/resource directory | Source editing or verified filesystem workflow; includes manifest and data files |
| Project export ZIP | Designer selected-resource import or Gateway whole-project import |
| Gateway backup | Wider Gateway recovery/migration; not an interchangeable view package |

Project exports omit Gateway-level tags, Tag Providers, connections and other Gateway configuration. List dependencies separately: named queries/project scripts, inherited resources, style classes, themes/fonts/images/icons, reports, IdPs, modules and data providers. Named Queries are project resources, but their database connections are Gateway resources.

## Designer workflow

1. Open the intended project in the matching Designer and preserve an export of resources that will change.
2. File > Export lets you choose resources; File > Import opens an export ZIP and lets you select resources to merge.
3. Review conflict choices per resource (overwrite, skip, rename or cancel). Renaming a view can require updating references; it is not a complete dependency migration.
4. Save, close/reopen the affected views, check Configuration Explorer and bindings, launch a real session, then export the result for comparison.

Inherited resources may be read-only until overridden. Decide whether a change belongs in the parent or child. An inheritable project is not a launchable application; test the runnable child and its effective resources.

## Gateway workflow

Platform > System > Projects > Export produces a project ZIP. Import Project restores a whole project and may overwrite one if explicitly selected. Use a new test project first when validating generated resources. Check project enabled/inheritable/parent settings and destination data dependencies before launch.

For a partial package, prefer Designer import into the intended existing project; creating a new Gateway project from a partial package can leave missing routes, scripts or inherited resources. The packager preserves project.json, so inspect it before selecting Gateway import.

## Bundled packager

`package_resources.py` reads one directory/export, checks structure, selects resource directories and builds a ZIP rooted at project.json. It includes discoverable local view, style and query dependencies to a fixed point, preserves resource bytes and unknown data files, reports unresolved/dynamic dependencies, and does not overwrite the output. No `--output` means preview only.

Use explicit `--resource` selections for project scripts and script-only dependencies. For example:

```sh
python3 scripts/package_resources.py /path/to/project \
  --view Overview --view Dialogs/Editor \
  --resource com.inductiveautomation.perspective/page-config
```

A script opening a popup does not guarantee automatic detection of that popup path. Inspect `dependencies_requiring_review` and the source scripts. If route/session configuration references unrelated views, include them or intentionally edit a copy of that configuration. Do not silently strip unknown resources to make a validator pass.

## Filesystem and API workflows

Ignition 8.3 stores project resources under `data/projects/<project>/`. Work on an isolated copy, inspect a diff, then apply the authorized files using the target's documented synchronization mechanism. 8.3 supports explicit project filesystem scans. A write to disk alone is not evidence that the running project adopted it. Coordinate with open Designer sessions to avoid overwriting unsaved edits. Preserve rollback files outside the watched project tree.

Gateway APIs are discovered at `/openapi` and `/openapi.json`. Configuration-resource routes, project routes and project scan routes have distinct contracts. Use only operations present in the target spec. Read the request schema, authorization, signature/concurrency requirements and response before a mutation. Do not transplant an endpoint from another patch or use guessed internal routes. The bundled discovery script is read-only and accepts saved specs for offline review.

The API token is read from an environment variable. HTTPS verification stays enabled; use `--ca-file` for private trust. Plain HTTP is supported only for loopback test Gateways. Redirects are rejected rather than forwarding credentials elsewhere.

## Readback and rollback

Re-export after import/save and compare normalized JSON plus unchanged bytes for unrelated resources. Calculated metadata can differ. Verify pages, embedded views, popups, docks, bindings and scripts in the running project. On failure, preserve diagnostics and restore only the affected authorized resources, then repeat readback. A successful HTTP response or ZIP extraction alone is insufficient.

Sources: [project export/import](https://www.docs.inductiveautomation.com/docs/8.3/platform/projects/project-export-and-import), [inheritance](https://www.docs.inductiveautomation.com/docs/8.3/platform/projects/project-inheritance), [version control](https://www.docs.inductiveautomation.com/docs/8.3/tutorials/version-control-guide), [Gateway API](https://www.docs.inductiveautomation.com/docs/8.3/platform/gateway/openapi), [folder structure](https://www.docs.inductiveautomation.com/docs/8.3/appendix/reference-pages/gateway-folder-structure).
