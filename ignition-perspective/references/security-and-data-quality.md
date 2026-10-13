# Security and data quality

## Permissions belong at the execution boundary

Determine the project's Identity Provider and security-level model before implementing protected views or commands. Configure session access, view permissions and event-action security where appropriate. Use backend tag/query permissions and validation for data changes. An enabled/visible expression or filtered table can communicate permissions but does not enforce them.

Property access levels have different purposes: Public permits browser-originated reads/writes, Protected blocks browser-originated writes, Private also hides values from the browser, and System is framework-owned. They do not prevent trusted Gateway bindings/scripts from operating in the same way. Do not treat a password input's masked rendering as a secret store. Avoid persistent plaintext secrets in project JSON, props, params, scripts or examples.

Named Query execution occurs on the Gateway. Bind parameters rather than assembling SQL strings. Validate user-controlled asset identifiers and request parameters against the operation's allowed scope. For commands, check value type/range, identity, authorization and the write result. A response or local display change alone does not confirm equipment state.

## Quality is part of the value

Define explicit loading, no-data, bad-quality, disconnected and healthy states. Preserve the distinction between a legitimate numeric zero and an unavailable reading. Do not suppress overlays without providing an equivalent indication. A retained last value during an outage should be labeled stale; restoration needs a fresh successful read/quality transition.

Tag bindings expose options that affect initial uncertain values, fallback timing, overlay display and writeback. Review them for the operation rather than setting all defaults globally. Transforms and script extraction can strip or obscure quality metadata; handle it explicitly when producing an operator-facing result.

History quality filtering and interpolation change the evidence shown. Show gaps or explanatory status where needed, and avoid implying that interpolated or sampled data is raw acquisition. Alarm and process states are separate from connection quality.

## Validation scenarios

For a read-only display: healthy input, null/empty input, non-Good quality, disconnect with retained value and recovery. For a write: authorized success, denied authorization, invalid input, write failure, and confirmed readback. For multi-session UI: separate local drafts and shared process state. For imported assets: external dependencies and inherited permissions must be tested in the destination.

These scenarios are proportional to the requested feature. A static demo with synthetic values does not require plant writes; label its evidence accordingly.

Sources: [Perspective security](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/security-in-perspective), [property access](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/perspective-component-properties), [tag bindings](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/bindings-in-perspective/tag-bindings-in-perspective), [Named Queries](https://www.docs.inductiveautomation.com/docs/8.3/platform/sql-in-ignition/named-queries).
