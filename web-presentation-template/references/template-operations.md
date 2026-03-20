# WebPresentationTemplate Operations Reference

## Common Commands

```bash
# Serve locally
python3 -m http.server 8000

# Regenerate service worker cache and bump versions
./build.sh

# Find unused assets
./cleanup-assets.sh

# Delete unused assets, then rebuild cache
./cleanup-assets.sh --delete
./build.sh
```

## Transition Patterns

```javascript
transitions: {
    'slide-1→slide-2': 'wipe',
    'slide-2→slide-3': 'crossfade',
    'slide-3↔slide-4': 'alvaro',
},
```

Use `→` for one-way transitions and `↔` for both directions.

## Slide Group Pattern

```javascript
groups: {
    book: ['slide-5', 'slide-6', 'slide-7', 'slide-8'],
},
groupTransitions: {
    book: 'pageTurn',
},
```

## Slide Link Pattern

```javascript
slideLinks: {
    'slide-3': 'https://example.com',
},
```

## Safe Renumbering Checklist

1. Renumber `id="slide-N"` in `index.html` sequentially.
2. Renumber nav dots so `data-slide` is `0..N-1`.
3. Renumber nav dot `aria-label` to `Slide 1..Slide N`.
4. Update `js/slide-config.js` slide references.
5. Update `css/presentation.css` if it includes `#slide-N` selectors.
6. Run `python scripts/check_presentation_template.py .`.

## Asset Naming Rule

Use camelCase names without spaces in `assets/images/` and `assets/video/`.

- Valid: `titleCard.jpg`, `customerQuote.png`, `introVideo.mp4`
- Invalid: `title card.jpg`, `intro-video.mp4`, `Intro Video.mov`
