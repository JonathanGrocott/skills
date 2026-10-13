# Version compatibility

Documentation reviewed on **2026-10-12**. The `/docs/8.3/` tree is rolling documentation and contained entries through **8.3.10** when reviewed. The bundled examples target **8.3.9**. Do not infer that every property in the rolling manual exists in 8.3.0 or the target patch. Verify import, Designer save/reopen, and runtime behavior on the installed build.

## Feature gates from the reviewed manual

| Feature | Documented version boundary |
|---|---|
| Drawing and Form components | Introduced in 8.3.0 |
| Mobile App Offline Mode | Introduced with 8.3; also depends on the mobile App and configuration |
| 8.3 theme configuration resources/APIs | Use 8.3 resource workflow, not an assumed 8.1 theme folder |
| Drawing `typeAttr`; Form number-step `any` | 8.3.4 additions |
| Drawing `onElementClicked` | 8.3.5 addition |
| Form File Upload widget and additional Dropdown options | 8.3.8 additions |
| `system.config` Gateway resource functions | 8.3.8 addition; do not treat as project view-editing APIs |

Check the exact component/function page and release notes for later additions. A newer manual property is a capability to discover, not a reason to upgrade the user's Gateway or change unrelated infrastructure.

## Migration and export rules

Project exports are intended for the same version or later; do not promise backward compatibility. Imports from before 8.1 require an intermediate 8.1 upgrade before 8.3. Retain originals and test a copy. Verify installed third-party component modules and licenses independently.

Perspective scripts use Jython 2.7. Ignition 8.3 dataset scripting exposes PyDatasets automatically, so don't assume an 8.1 conversion is always needed. Inspect returned object shape when mixing Java, datasets and Perspective property wrappers.

## Documentation inconsistencies

Some pages retain legacy links, inconsistent argument casing, example typos, or conflicting narrative details. Use a canonical 8.3 URL from the map instead of blindly following relative Markdown paths. For an ambiguous function signature, check target Designer autocomplete and run a bounded test. For a JSON field, export from the target Designer or verify against the installed runtime; UI labels and API parameter names can differ from serialized keys (for example a dock's Display setting).

The manual is not a complete machine-readable schema for `view.json`, every module type ID or resource export envelope. The static validator intentionally accepts unknown fields/components and reports its limits. New types should be retained and checked in the target runtime.

Sources: [new features by patch](https://www.docs.inductiveautomation.com/docs/8.3/new-in-this-version), [Python runtime](https://www.docs.inductiveautomation.com/docs/8.3/platform/scripting/python-scripting), [project compatibility](https://www.docs.inductiveautomation.com/docs/8.3/platform/projects/project-export-and-import).
