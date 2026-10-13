# Pages, navigation and sessions

## Page and view identity

A view path identifies a definition, such as `Equipment/Card`. A page URL such as `/equipment/:assetId` maps navigation to a primary view with parameters. A runtime page ID identifies a browser page instance; it is not the URL or view path. Keep all three distinct in scripts and deployment reports.

Configure page routes in Designer's Perspective Page Configuration. Define matching view params for route inputs. Path parameters and URL query parameters behave differently; consult the Pages reference before constructing URLs. Use URL navigation when query parameters are required. Encode values appropriately and do not embed tag paths containing unsupported route characters directly into path parameters.

The demo uses `com.inductiveautomation.perspective/page-config/config.json` with a `pages` object and `sharedDocks`. Each route has `viewPath` and optional title; page-specific dock overrides require inspecting a real export. Preserve unrelated routes.

## Docks and popups

Docks occupy edges of a page and can be shared or page-specific. Choose visible, on-demand or automatic display; push versus cover behavior; size; breakpoint; resize; modal and handle behavior. A header usually needs the appropriate north-edge anchor setting. Use stable dock IDs for script actions.

**Serialization detail verified on 8.3.9:** the Designer's Display concept is stored as `show` in the demo dock configuration, alongside `viewPath`, `id`, `size`, `content` and `anchor`. Do not substitute a UI label (`display`) or an `alterDock` API dictionary key for a serialized resource field. Test that the dock actually appears after import.

Popups use a view path and unique popup ID. Decide if opening twice should reuse a popup or create multiple instances. Pass params explicitly; choose modal/overlay-dismiss behavior, close controls, size and viewport bounds. For editors, create a draft and decide apply/cancel behavior before adding writes.

## Sessions and project settings

Session custom properties are per-session state. Built-in session properties describe auth, locale, theme, time zone, gateway/device connection state, app bar, geolocation and mobile capabilities. Respect system-owned values. Session authorization is not established by changing a client-visible property.

Review project locale, time zone, update notifications, desktop/mobile timeout and inactivity settings for the requested application. Test reload, reconnect, navigation, popup reopen, multiple tabs and multiple sessions where they matter. Data preserved on disconnect is not proof of fresh communication.

## Device/runtime differences

Browser, Perspective Workstation and the mobile App have different capabilities. Mobile sensors, barcode/NFC actions and vibration require the appropriate platform and permissions. Workstation kiosk/window/exit functions are not generic browser operations.

Offline Mode is a mobile-App capability, enabled in project properties with suitable security, cached assets, themes/languages and authentication lifetime. Desktop browsers do not become offline applications through this setting. Cached values can be stale; only supported interactions queue, and form submission processing needs retry/idempotency handling. Validate offline behavior on an actual mobile device before claiming it.

For reverse proxies, validate websocket upgrade/forwarding, required routes, external URL behavior and TLS configuration. A Gateway home page loading does not prove a Perspective websocket stays connected.

Sources: [Pages](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/pages-in-perspective), [Docks](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/views-in-perspective/docked-views), [Sessions](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/perspective-sessions), [session properties](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/perspective-sessions/session-properties), [Offline Mode](https://www.docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective/perspective-sessions/ignition-perspective-app/offline-mode). Proxy and mobile references are also indexed in the documentation map.
