# Implementation Status · 2026-10-11

## Delivered

- Responsive light UI with editor workspace, left asset panel and right inspector.
- Browser-local background PNG/JPEG/WebP upload and multiple overlay uploads.
- Canvas-based pointer dragging, corner resize, aspect-ratio lock, numeric positioning, keyboard nudge.
- Square, rounded rectangle and circular clip masks on overlays.
- Layer show/hide, reorder, duplicate, delete, select, undo and redo.
- Export original-dimension PNG and no remote runtime dependencies.
- MIT license.

## Run locally

Open `index.html` in a modern browser. Alternatively, use `python3 -m http.server 8080` from the project root and visit `http://localhost:8080`.

Static hosting: host the repository root as a static site, no build command required.

## Limitations / honest QA status

This initial edition was committed through the GitHub API. **Browser interaction, linting, visual screenshots and cross-browser E2E tests have not been executed in this session**. Treat this as an implementation candidate, not a QA-approved production release.

- The square shape is a rectangular crop using the layer bounding rectangle; it does not automatically force 1:1 geometry.
- The drawImage call currently resizes an image to fit its layer dimensions, so turning off aspect-ratio lock can distort its pixels. Keep aspect-ratio lock for QR images.
- The circular mask clips QR modules; use only for avatars/logos or decorations. There is a warning, but it does not prevent use.
- White backing is drawn inside the image layer's shape. It does not introduce an extra safety padding around the QR itself; if the source QR lacks a quiet zone, prepare a padded QR input first.
- Layer resize handles operate on rectangular bounding boxes; there is no separate 4-point perspective transform.
- There is no local automatic QR scan verification yet.
- New background import discards current layers without confirmation; use export before replacing.
- Very large images are limited by browser Canvas memory and raster dimensions.
- Image assets remain retained in session memory until page close; lifecycle cleanup can be improved.
- Mobile touch behavior and all supported browsers need hands-on testing.

## Next iteration priorities

1. Fix QR-safe rendering: use contain fit plus configurable white padding and independent opaque cover rectangle.
2. Add distinct square crop (true 1:1), circle crop and drag-to-reposition crop content inside its clipping frame.
3. Add local QR decode checks and verify exported composite.
4. Establish browser Playwright tests, fixture QR assets and responsive visual QA.
5. Evolve into Vite/React modules when feature behavior is stable, per `TECHNICAL_DESIGN.md`.

## Product quality bar

Do not describe the tool as universally scan-proof until local and physical scan tests pass. All editing and export should remain client-side.
