# Components and layouts

## Choose the layout from behavior

| Container | Appropriate use | Child positioning to inspect |
|---|---|---|
| Flex | Forms, cards, responsive rows/columns | `grow`, `shrink`, `basis`, `display`; direction, wrap and alignment on parent |
| Coordinate | Process diagrams, overlapping instruments, fixed geometry | `x`, `y`, `width`, `height`, rotation; pixel versus percent mode |
| Column | Same components rearranged across widths | Breakpoint spans, row/column index, order and height |
| Breakpoint | Different compositions at narrow/wide sizes | Small/large children, breakpoint and determinant |
| Tab | Several panels sharing one space | Tabs, active index, menu/content styles |
| Split | Resizable adjacent panels | Orientation, split bounds and child position |

Use Flex for ordinary responsive content when it fits the requirements. Coordinate layouts are often appropriate for P&IDs; choose pixel or percent behavior intentionally. A flex child's percentage dimensions are not a substitute for its basis/grow/shrink settings. Give scrolling tables/charts a deliberate minimum or basis height and test overflow. A root container choice determines the view's layout; use a new view for major root-type changes.

Test with long labels, localized text, empty data, maximum expected rows and target device widths. Do not rely on color alone for equipment/quality status; include a textual status and units. Touch interactions need adequately sized targets and alternatives to hover.

## Component selection

The [documentation map](documentation-map.md) indexes every built-in component, tutorial and component scripting page. Use the exact page for defaults, nested object shapes and event payloads; do not guess internal `ia.*` identifiers from display names.

- **Embedding:** Embedded View uses a path and matching params; Flex Repeater supplies an instance array. Carousel, Accordion, View Canvas, Dashboard and Table renderers also hold view references. Honor default-view width/height flags and per-instance positioning. Avoid excessive nesting or unbounded repeater instances.
- **Tables:** Match column field keys to data. `selection.data` differs from the whole dataset. Cell/row rendering may embed views; preserve the documented parameter contract. Editing events do not automatically persist changes to a database. Resolve edits by stable record identity, accounting for sorting/filtering and `row` versus `rowIndex` semantics in the event's reference.
- **Charts:** Time Series expects time/value data; XY needs matching data-source/axis/series keys. Power Chart adds native historian browsing, pen configuration and historian licensing dependencies. A static chart proves rendering, not historian connectivity. Bound ranges, point counts and polling frequency.
- **Alarms:** Alarm Status Table uses current alarm state; Alarm Journal Table needs a configured journal. Configure acknowledgement/shelving permissions and filters; visual filtering is not access enforcement. Test active, cleared, acknowledged and shelved states where relevant.
- **Inputs:** Prefer a component's semantic action event (for example Button `onActionPerformed`) for keyboard/touch behavior. Text defer-update settings affect when bindings receive edits. Dropdown value/options and multi-select shapes must agree. One-Shot and Multi-State controls have distinct command/readback semantics; a successful request is not physical confirmation.
- **Form (8.3):** Define widget input keys, layout, constraints, data/context, submission routing and response behavior. Validate submitted data again on the Gateway. Offline-capable submissions need retry/idempotency decisions. Number widgets require explicit step configuration for decimals; newer widgets are patch-dependent.
- **Drawing (8.3):** Uses SVG-style elements with Ignition-specific attributes. Verify element names/addresses for click handling; not every SVG attribute behaves identically. Coordinate pipes are a separate feature with connections, origins, segments and anchors.
- **Symbols:** Motor, Pump, Sensor, Valve and Vessel support configured states and session-level appearance. Bind actual states and quality deliberately. Animation is an indication, not evidence of physical motion.
- **Maps/media:** Map and Google Map are different components; Google Map requires its configured API key. Check map tile/network requirements. Audio/video autoplay, codecs, browser support, iframe restrictions and PDF access are runtime concerns.
- **Files/reports:** File Upload events provide Gateway-side file data. Report Viewer additionally needs the Reporting module and report resource. Prefer Image Management for shared images; track images as Gateway dependencies.

## Designer operations

Create a view under Perspective > Views, select the root, drag components from the palette, and configure them in Property Editor. Use Project Browser to select invisible or deeply nested nodes. Deep selection enters a container; Wrap in Container changes the hierarchy. Configuration Explorer locates bindings, scripts and references. Preview mode and a real session test different execution contexts; use both when available.

Sources: [component reference](https://www.docs.inductiveautomation.com/docs/8.3/appendix/components/perspective-components), [working with components](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components), [design tips](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/perspective-design-tips). Consult the map's individual component links for each category above.
