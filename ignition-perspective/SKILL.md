---
name: ignition-perspective
description: Create, inspect, edit, package, import, and troubleshoot Ignition 8.3 Perspective views and project resources, including components, bindings, Jython scripts, styles, navigation, and runtime validation. Use for Perspective Designer or exported project work.
---

# Ignition Perspective

Produce editable native Perspective resources and verify the requested behavior. Target the user's installed **8.3.x patch**, not a generic interpretation of the 8.3 manual. This skill supports Designer work, local resource editing, and imports. It does not turn a browser mockup into an Ignition view or convert Vision resources automatically.

## Establish the working contract

Identify the target version, installed modules, project/export, view paths, intended screens and devices, data sources, and intended edit/import destination from available context. Inspect existing resources before designing replacements. Ask only for missing information that affects correctness; use explicit synthetic values while actual tag/query paths are unavailable.

Keep project-wide resources (page configuration, session properties, styles, project scripts, named queries) and Gateway resources (tags, providers, connections, themes, images, IdPs) distinct. An imported view is not a self-contained application unless its dependencies are present.

Read [version-compatibility.md](references/version-compatibility.md) and the relevant workflow below. [documentation-map.md](references/documentation-map.md) maps every reviewed manual page to authoritative links; search it for an unfamiliar component, method or feature. Load only relevant references.

## Create

1. Define view inputs/outputs, page URLs, reuse boundaries, container choice, loading/empty/bad-quality behavior, and any permitted writes.
2. Use [components-and-layouts.md](references/components-and-layouts.md) to choose containers/components; consult the exact component page for properties and events. Use [views-and-resource-format.md](references/views-and-resource-format.md) for serialization.
3. Start from an existing target-version export or the tested [example project](assets/examples/SkillDemo). Confirm unfamiliar component type IDs and serialized binding/event shapes with a Designer export; documentation property tables are not a complete JSON schema.
4. Connect behavior using [bindings-and-transforms.md](references/bindings-and-transforms.md) and [scripting-and-events.md](references/scripting-and-events.md). Embedded scripts use Jython 2.7; the bundled CLI helpers use Python 3.9+.
5. Configure [pages, navigation and sessions](references/pages-navigation-and-sessions.md), [styles/assets](references/styles-themes-and-assets.md), and [security/data quality](references/security-and-data-quality.md) as needed.
6. Validate, import into the authorized destination, then inspect actual rendered behavior. Include dependencies and remaining validation limits with the deliverable.

## Edit

Run inventory and inspect the affected resource, its manifest, callers and dependencies. Preserve unknown keys, component types, custom properties, array order, event actions, parameter directions, resource attributes, and inherited-resource semantics. Change the narrowest subtree that implements the request. Component renames/reparenting may break property paths and scripts; view renames may break navigation, popups, embedding, dashboards and table renderers. Update known references and flag dynamic references for review.

Use JSON-aware editing; do not use text replacement across an entire export. Compare the resulting files before packaging. Do not reconstruct a complex existing view from defaults. A new root container generally calls for a new view and an intentional migration of children and their positioning.

## Import or deploy

Follow [import-export-and-deployment.md](references/import-export-and-deployment.md). Prefer Designer File > Import for selected resources and Gateway project import for a whole new project. Review the exact destination, conflicts and dependency report. Preserve an export of resources being replaced. User authorization carries through the requested work; do not create an extra approval loop for already-authorized imports. Do not infer authorization to overwrite an unrelated project, change Gateway infrastructure or write to plant equipment.

For API work, first discover the target Gateway's OpenAPI spec; do not assume a Gateway configuration-resource endpoint can modify project views. The discovery helper only reads the spec. When using a documented mutation, inspect its target-version request/response schema, apply the bounded requested change, and read it back. Stop on a version/schema mismatch instead of guessing alternative mutating routes.

## Helpers

Run from the skill directory (or use absolute script paths):

```sh
python3 scripts/inspect_project.py /path/to/project-or-export.zip
python3 scripts/validate_project.py /path/to/project-or-export.zip --strict
python3 scripts/package_resources.py /path/to/project --view Overview
python3 scripts/package_resources.py /path/to/project --output /path/to/new-export.zip
python3 scripts/discover_gateway_api.py --url https://gateway.example
python3 scripts/discover_gateway_api.py --spec /path/to/openapi.json
```

Packaging without `--output` is a preview. `--view`/`--resource` select resources; discoverable local view/style/query dependencies are included. Dynamic paths, script-only references, inheritance and external resources remain explicit review items. No helper uploads, scans a Gateway, executes a view script, or overwrites an existing output. Authentication for discovery uses an existing token from `IGNITION_API_TOKEN`; never put tokens in command arguments or generated artifacts.

## Completion evidence

Follow [validation-and-troubleshooting.md](references/validation-and-troubleshooting.md). Report separately: static checks, archive round-trip checks, actual Ignition import, Designer reopen/save, browser behavior, live data/permission tests, and device-specific checks. Do not call a view production-ready from a JSON pass or screenshot. The bundled synthetic examples are starting points; verify Designer editability, runtime behavior, and data integration on the target installation.
