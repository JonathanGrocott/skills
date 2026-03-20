---
name: web-presentation-template
description: Build, edit, troubleshoot, and deploy presentations using the Chad-NextStep WebPresentationTemplate (vanilla HTML/CSS/JS slides). Use when tasks involve creating or modifying slides in `index.html`, configuring transitions in `js/slide-config.js`, managing media assets in `assets/`, running `build.sh` for service-worker cache updates, or preparing static hosting deployments.
license: Complete terms in LICENSE.txt
---

# Web Presentation Template

Use this skill to implement presentation changes safely in the WebPresentationTemplate project while preserving navigation, transitions, and offline caching.

## Quick Workflow

1. Confirm project root contains `index.html`, `js/slide-config.js`, and `build.sh`.
2. Read current `index.html` structure before editing.
3. Apply requested content/layout changes.
4. Keep slide IDs and nav dots synchronized (see integrity rules below).
5. If assets changed, run `./build.sh` to refresh `sw.js` and cache-busting versions.
6. Run `python scripts/check_presentation_template.py <project-root>` before handoff.

## Integrity Rules (Do Not Break)

- Keep slide IDs sequential and 1-indexed: `slide-1`, `slide-2`, `slide-3`, ...
- Keep nav dots sequential and aligned with slides:
  - `data-slide` is 0-indexed (`0..N-1`)
  - `aria-label` is 1-indexed (`Slide 1..Slide N`)
- When inserting/removing/reordering slides, update all affected slide IDs and nav dots.
- Update `js/slide-config.js` references (`transitions`, `groups`, `slideLinks`) after renumbering.
- Use camelCase asset names without spaces for files in `assets/images/` and `assets/video/`.

## Editing Tasks

### Edit Slide Content

- Edit `<div class="slide-content">` inside target slide sections in `index.html`.
- Keep structural wrappers intact:

```html
<section class="slide" id="slide-N">
    <div class="slide-background">...</div>
    <div class="slide-content">...</div>
</section>
```

### Add Slide

1. Insert new `<section class="slide" id="slide-N">` in `index.html`.
2. Add matching nav dot in `<nav class="slide-nav">`.
3. Renumber all following slide IDs if inserted in the middle.
4. Renumber nav dot `data-slide` and `aria-label` accordingly.
5. Update relevant entries in `js/slide-config.js`.

When doing bulk renumber replacements, match exact suffixes (for example `slide-3"`) to avoid accidental changes to `slide-30`.

### Remove or Reorder Slides

- Remove/move `<section>` blocks in `index.html`.
- Recreate sequential slide numbering and nav-dot numbering.
- Reconcile every `slide-N` reference in `js/slide-config.js`.

### Configure Transitions

Edit `js/slide-config.js`:

```javascript
transitions: {
    'slide-1→slide-2': 'wipe',
    'slide-3↔slide-4': 'alvaro',
},
groups: {
    chapterA: ['slide-5', 'slide-6', 'slide-7'],
},
groupTransitions: {
    chapterA: 'pageTurn',
},
slideLinks: {
    'slide-3': 'https://example.com',
},
```

### Add or Replace Media

- Put images in `assets/images/` and videos in `assets/video/`.
- Enforce camelCase filenames with no spaces.
- Prefer `.mp4` for background videos.

After adding/removing media, run:

```bash
./build.sh
```

This regenerates `sw.js` and bumps `?v=` query parameters in `index.html`.

## Validation and Preview

Run this validation sequence from project root:

```bash
python scripts/check_presentation_template.py .
python3 -m http.server 8000
```

Then open `http://localhost:8000` and verify:
- Slide order and navigation dots
- Transition behavior forward/backward
- Video/image loading
- Direct links via URL hash (`#N`)

## Deployment

Treat the project as a static site:
- GitHub Pages
- Netlify
- Vercel
- S3/static web hosting
- Any basic web server

No build pipeline is required beyond `./build.sh` when assets change.

## Bundled Resources

- `scripts/check_presentation_template.py`: structural consistency checker
- `references/template-operations.md`: quick snippets and change recipes
