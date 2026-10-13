# Scripting and events

## Runtime and scope

Ignition 8.3 uses Jython 2.7 for these scripts. Avoid f-strings, Python 3-only syntax, CPython-only packages, browser JavaScript and Vision `system.gui` assumptions. Perspective scripts run on the Gateway, including session-scoped scripts. File operations therefore address the Gateway filesystem; use `system.perspective.download` to deliver a file to the browser.

Component scripts receive `self` and event-specific arguments. Use each component's event reference; `event` fields are not universal. Configure events separately from custom methods, message handlers and extension functions. Extension functions have fixed signatures and documented return contracts.

The serialized event script in the tested example stores an indented body in `events.component.onActionPerformed.config.script`, with action `type: script` and `scope: G`. Designer wraps the function. For lifecycle actions use the actual exported system-event structure. Preserve multiple-action configurations from existing exports.

## State and communication

Use view custom properties for local state and params for reusable interfaces. Session properties are unique per session, while tag values are shared across sessions. Do not use tags as a convenient temporary form buffer.

`self.getSibling`, `getChild`, `parent`, `view`, `page`, and `session` support traversal, but component traversal stays within a view instance and becomes brittle after reparenting/renaming. For independent views, use explicit params or component message handlers with a meaningful message type and payload.

```python
# Body of a button script, in a Perspective session:
system.perspective.sendMessage(
    "equipment-refresh", {"assetId": self.view.params.assetId}, scope="page")
```

Match the receiving handler's scope and filter by asset/instance ID when several instances listen. Messages run asynchronously: neither side can assume completion order. Component message handlers invoked by `system.perspective.sendMessage` are different from Session Event Message handlers. Use the appropriate documented API for the latter.

## Change scripts and lifecycle

Property change scripts receive `previousValue`, `currentValue`, `origin`, `missedEvents` and `self`. QualifiedValues include value, quality and timestamp. Filter only origins appropriate to the operation; guard against reentrant writes and handle missed events when state reconstruction matters. Prefer expressions/transforms for pure derived data.

Session Startup/Shutdown and Page Startup have different lifetimes. Closing a tab does not immediately destroy the session. Navigating within an existing page does not necessarily fire Page Startup again. Form Submission handlers are Gateway-side events and may be used with offline submissions; current documentation places them alongside other Perspective event scripts. Do not assume a live component `self` in a Gateway form handler.

## Common actions

```python
system.perspective.navigate(page="/history")
system.perspective.openPopup(
    "asset-editor", "Dialogs/Editor", params={"value": 42},
    title="Edit preview", modal=True, viewportBound=True)
system.perspective.closePopup("asset-editor")
system.perspective.toggleDock("navigation")
self.refreshBinding("props.data")
```

Choose one navigation target (`page`, `view`, or `url`); they are not equivalent. Dock operations use a configured dock ID; popup close uses the opening ID. In Gateway scope, many `system.perspective` operations require **both** `sessionId` and `pageId`; some have other scope requirements. Consult the exact function page, especially where the manual shows inconsistent `ID` casing. Do not assume every function in the namespace is valid in Gateway scope. Workstation functions and mobile actions require their respective runtime.

`system.perspective.print` is diagnostic output; print/download actions have separate behavior. Do not enable remote logging configuration merely for routine troubleshooting. Keep operations bounded and avoid blocking repeated binding evaluations with database/network work. Business logic used across views belongs in project scripts with explicit inputs.

## Data-changing actions

Validate types, ranges and backend authorization before a write. Use parameterized Named Queries for database mutations; inspect tag write result quality and confirm readback where requested. A hidden/disabled button is only a presentation rule. Use action and backend permissions. Avoid logging credentials or complete sensitive payloads.

Sources: [scripting](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/scripting-in-perspective), [message handlers](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/scripting-in-perspective/component-message-handlers), [events](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/scripting-in-perspective/perspective-session-events-scripts), [function index](https://www.docs.inductiveautomation.com/docs/8.3/appendix/scripting-functions/system-perspective). Individual component and function links are in [documentation-map.md](documentation-map.md).
