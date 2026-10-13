# Views and resource format

## Resource boundaries

A view is a project resource identified by its folder path, such as `Equipment/Card`. Each instance owns its own state; multiple instances can share a definition. The definition has exactly one root container. Pages mount primary, docked and popup views; embedding components mount other view instances.

Typical project tree, as verified with the bundled 8.3.9 examples:

```text
project.json
com.inductiveautomation.perspective/
  views/Equipment/Card/resource.json
  views/Equipment/Card/view.json
  page-config/resource.json
  page-config/config.json
```

A view typically has `props`, `custom`, `params`, `propConfig`, and `root`. Components have `type`, `version`, `props`, `meta`, `position`, `custom`, `propConfig`, optional `events` and optional `children`. These are observed serialization conventions, not a universal schema. Preserve additional fields and version numbers from the source. A component's **position** is interpreted by its parent container. Its own **props** configure its contents.

Use unique sibling `meta.name` values and stable descriptive names. Bindings, scripts, component traversal and test selectors can depend on those names. Preserve child order: layout, rendering and z-order can depend on it.

## Properties and parameters

`props` contains built-in view settings such as `defaultSize`; `custom` is internal view state; `params` is the interface to callers. Parameter definitions under `propConfig["params.name"]` may include `paramDirection` (`input`, `output`, `inout`) and persistence metadata. Input values are supplied by callers; output values are produced inside; in/out values support both directions. Check the contract at each embedding site and page route.

Component property categories also include `position` and `meta`. Arrays, objects and scalar values have different shapes; do not stringify an array when the component expects JSON. Do not invent a writable value for a system-owned property.

Property `persistent` settings affect initial and saved values. Built-in bound properties are commonly transient. A custom property without persistence and without a binding may disappear on save/reopen; declare state deliberately. Access settings are a separate concern from persistence. Review both when editing a binding.

## Manifests

Each project resource's `resource.json` declares its data files, scope and metadata. A view manifest lists `view.json`. In the tested example: scope `G`, version `1`, restricted `false`, overridable `true`, files `["view.json"]`, attributes `{}`. Use the existing manifest for existing resources; do not normalize metadata to these example values.

The manifest version is a serialization version, **not** Ignition's patch version. `lastModification` and `lastModificationSignature` are calculated/audit metadata when present; do not forge or arbitrarily recalculate them. Let a target-version Designer save produce its normal metadata, and compare semantic content on readback. `project.json` controls project-level settings, including parent, enabled and inheritable state.

## Editing procedure

Inventory → preserve original → JSON-aware edit → compare → static validate → import/save/readback → runtime check. Check every caller when changing a view path or parameter. Check scripts and relative paths when moving children between containers. Copying children into a different container requires converting their position properties.

Component clipboard content, a complete view definition, a resource folder and an export ZIP are different formats. For clipboard workflows, obtain a target Designer Copy sample and preserve its envelope. Do not tell the user to paste a full project ZIP or assume a single `view.json` is a Designer File > Import archive.

Sources: [Views](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/views-in-perspective), [component properties](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/perspective-component-properties), [resource metadata](https://www.docs.inductiveautomation.com/docs/8.3/appendix/reference-pages/resource-json-file).
