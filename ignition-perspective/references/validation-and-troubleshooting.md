# Validation and troubleshooting

## Evidence levels

1. **Source/static:** JSON parses without duplicate/non-finite values; manifests/data files agree; component tree and property containers have plausible structure; dependencies reviewed.
2. **Package:** ZIP can be reopened; selected file bytes and unknown fields survive; source remains unchanged; dependencies/report match the selected scope.
3. **Ignition import:** The target Gateway/Designer accepts the archive and the project/resources appear. Record actual version and module/trial state.
4. **Designer:** Open, inspect, save and reopen resources; test the relevant binding previews and event configuration; compare a new export. A browser session does not prove Designer editability.
5. **Runtime:** Actual browser/Workstation/mobile behavior: values, navigation, popups, docks, input validation, scrolling/resizing, console/Gateway errors and reload behavior.
6. **Integration:** Live tags/queries/history, permissions, write readback, quality/outage/recovery, multi-session behavior and required devices. Synthetic examples do not provide this evidence.

State the levels completed and concrete remaining gaps. Do not collapse them into a single "validated" claim.

## Helper contracts and limits

All helpers use the Python 3.9+ standard library. Inventory/validation read either one project directory or ZIP, requiring project.json. They do not accept a bare view.json as a project export. A single enclosing archive folder is accepted only if no sibling content lies outside it. Archive paths, symbolic links, duplicate members and encrypted ZIPs are rejected. Bounds are 10,000 entries, 32 MiB per file and 128 MiB total uncompressed data. A very large legitimate project needs a deliberately reviewed limit change or a selected-resource export.

The validator checks common structure and manifests, sibling names, basic binding/parameter shapes and unresolved view candidates. It does **not** validate all component properties against a vendor schema, compile expression syntax, execute Jython, resolve every dynamic dependency, verify styles/images/security or connect to a Gateway. Unknown module-specific fields remain intact. Unresolved candidates are warnings because inheritance and dynamic values may be legitimate; use `--strict` to fail warnings in a self-contained fixture.

Exit codes: inspect/package/discovery return 0 on success and 2 for invalid inputs or operation errors; validate returns 0 for pass, 1 for reported validation failures (including warnings under `--strict`), and 2 for unreadable/invalid input. CLI usage errors also return 2. Packaging with --output creates a new ZIP exclusively and does not deploy it.

## Behavioral scenarios

| Scenario | Observable pass criterion |
|---|---|
| Parameterized card twice | Different instances display distinct supplied values |
| Popup editor | Passed value loads; changed draft is local; apply validates; close/reopen has intended state |
| Navigation | Correct route, title and primary view; docks remain correct |
| Responsive layout | Required controls are reachable at narrow and wide widths; no accidental clipping |
| Table/chart | Data keys, timestamps, axes and units agree with known values |
| Import/edit/export | Edited values visible; unrelated resource content preserved on readback |
| Authorization | Denied operations fail at the execution boundary, not just in appearance |
| Data outage | Bad/stale state visible and fresh recovery demonstrated |

## Diagnose by symptom

- **View missing:** resource path/case, project enabled/inheritable state, parent project, import selection, manifest or missing module. Check project scan after disk edits.
- **Blank component:** type ID/property shape, dimensions and flex shrink/basis, embedded view path, parameter contract, default-view size flags, or missing module/assets.
- **Dock absent:** page configuration scope, view path, ID, show/auto settings, breakpoint and serialized field names. A UI label may differ from a JSON key.
- **Binding errors:** provider/query path, property path scope, parameter direction, data shape, quality, evaluation error and target patch.
- **Script ignored/fails:** actual event, enabled action, scope, wrapper/body format, indentation, Jython syntax, correct event fields and Gateway logs.
- **Input doesn't change:** protected/direct entry mode, defer-update settings, bound target ownership, bidirectionality, permissions and write result.
- **Wrong timestamps:** epoch unit, source time zone, session time zone and browser versus Gateway formatting.
- **Session won't connect:** module/license/trial, network/websocket/proxy, browser support and auth; don't assume successful HTTP means live data.

Use small reproduction views and targeted logs; stop before speculative rewrites or repeated production mutations. The [documentation map](documentation-map.md) links each relevant reference. Record actual verification separately from these general acceptance targets.
