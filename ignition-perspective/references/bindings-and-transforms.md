# Bindings and transforms

## Binding choice

| Binding | Use and checks |
|---|---|
| Tag | Direct, indirect or expression-selected tag path; provider, data type, quality and write permissions |
| Property | Link properties in the same view or exposed view/page/session state; direction and lifecycle |
| Expression | Derived values using Ignition expression syntax; dependencies and polling functions |
| Expression Structure | Named expression results forming an object; Wait On All and transform inputs |
| Query | Existing Named Query path and typed parameters; return format, polling and cache sharing |
| Tag History | Provider/path, start/end, query mode, aliases, aggregation, interpolation, point count and quality |
| HTTP | URL, method, headers/authentication, body, timeouts, polling and caching; network access is from Gateway |
| MongoDB | Requires connector and configured connection; binding reads; writes use appropriate functions |

A binding owns its target property. Do not simultaneously drive that target with a change script unless the interaction is intentional. Prefer bindings/expressions for derived values and scripts for explicit actions. Shared caching is appropriate only where data and authorization semantics permit shared results.

## Property paths and view interfaces

Use the binding picker to establish paths. `this`, `parent`, `view`, `page`, `session`, `/`, `../`, property scope and array indices have defined meanings. Property bindings do not traverse into another view instance. Pass values through params or send scoped messages instead. Renaming/reparenting components can invalidate paths even when the JSON remains valid.

In the tested serialization a binding is under `propConfig["props.text"].binding` with `type` and `config`. An expression uses type `expr` and `config.expression`. A property binding uses type `property` and `config.path`. Do not extrapolate every binding's serialized shape from these examples; export a configured target-version binding for less familiar types.

## Writes

Tag and property bindings can be bidirectional. Explicitly choose this for intended input/write behavior, verify backend permissions, and handle failed writes. Coalesce combines child-property changes for writeback; it does not make a multi-tag control sequence transactional. For apply/cancel forms, edit a local draft and write only on an explicit action. Keep confirmed process state separate from the user's requested setpoint.

## Transforms

Transforms run in order after the binding. Map converts values/ranges to desired values or styles; Format returns text; Expression uses Ignition expressions; Script uses Jython with `self`, `value`, `quality`, `timestamp` and a return value. Do not add a full function definition to a serialized script-body field if the Designer supplies the signature.

Use return format DOCUMENT when Query/History can already provide the needed object array. Avoid a dataset-to-JSON script solely to duplicate this feature. A custom transformation should handle empty/null values, unexpected shape and bad quality. Do not replace bad-quality readings with zero and present them as valid process values. Inspect quality separately if formatting/transforms obscure it.

For history, preserve numeric timestamps or native dates until the presentation boundary. Alias keys must match chart series/table columns. Distinguish raw versus aggregated results and requested sample count; interpolation or ignoring bad quality changes the meaning of the chart. Verify a known historical interval rather than only seeing a line appear.

HTTP POST/PUT/DELETE bindings may produce repeated side effects on reevaluation/polling. Use a deliberate action for commands unless repeated execution is explicitly required and designed. Never embed secrets in browser-visible props.

Sources: [bindings](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/bindings-in-perspective), [path reference](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/bindings-in-perspective/binding-property-path-reference), [transforms](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/bindings-in-perspective/transforms). Every individual binding and transform page is indexed in [documentation-map.md](documentation-map.md).
