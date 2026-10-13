# Styles, themes and assets

## Styling layers

Use inline style for local adjustments, project style classes for reusable design rules, and Gateway themes for shared theme-level behavior. Inline settings override conflicting class settings; component-specific styles may be more specific than general component styles. Use CSS-compatible values and units; don't confuse styling with container positioning.

Style class names in Perspective properties are project names/paths. CSS selectors for generated style classes use Perspective's naming conventions; inspect an existing stylesheet rather than inventing selectors. Renaming a style class does not automatically repair all consumers. Inspect nested style properties, expression-built class names and script assignments.

Use style-class element states for hover/focus/disabled appearance, media-query rules for width/orientation conditions, and animations where the interface calls for them. Provide focus and touch alternatives to hover. Avoid excessive flashing and retain status text alongside color. The Advanced Stylesheet is project-level CSS: account for its enablement and resources during import.

## 8.3 themes

Themes are Gateway configuration resources in 8.3, distinct from project style classes. Follow the target Gateway's documented theme APIs or verified filesystem resource workflow. The documented filesystem location is under:

```text
data/config/resources/core/com.inductiveautomation.perspective/themes/<theme>/
```

Inspect `resource.json`, `config.json`, the CSS entrypoint and every referenced file. Keep the base theme imported/inherited as required, and control CSS import order. The manual's description of `isPrivate` contains potentially confusing wording; verify listing behavior on the target before changing it. Do not edit built-in base-theme copies expecting them to override live built-ins; use a custom theme.

Fonts are separate resources/dependencies. Verify font URLs, formats and browser loading. Select themes using a session property or the documented theme action/function and test both normal and error/disabled states. Older 8.1 theme-directory instructions should not be applied blindly to 8.3.

## Images, icons, drawings and branding

Use Image Management for shared images or an explicitly managed external URL. Images in Image Management are served through `/system/images/...`; export/transfer them separately when needed. Dragging an image can embed data in a view or save/link it; large inline images increase resource size. Built-in icons use repository/icon paths. Custom icon repositories are additional Gateway assets and need their own deployment/readback.

The Drawing component stores an SVG-style element tree. Preserve element IDs, transforms, masks and clips; check unsupported or adapted attributes and runtime rendering. Converting an SVG-based component to a drawing may change its semantic behavior, so verify original bindings/events.

Co-branding customizes session launch/login surfaces and is distinct from view styling. Edition support and Gateway branding settings are separate dependencies. Do not package credentials or private image assets in a reusable skill example.

## Localization and time zones

Use translation keys/terms and locale-aware formatting where required. Test label growth, numeric formats and language fallback. Keep numeric values numeric for charts and calculations; format only presentation properties. Distinguish Gateway, project/session and device time zones. Some browser-rendered dates and Gateway script formatting can differ. Test a known timestamp, daylight-saving boundary and required locale rather than assuming every component formats identically.

Sources: [Styles](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/styles), [style classes](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/styles/style-classes), [custom themes](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/styles/creating-and-using-custom-perspective-themes), [images/icons](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/working-with-perspective-components/images-and-icons-in-perspective), [time zones](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/time-zones-in-perspective).
