# Release candidate QA — 2026-10-11

## Scope

Target: [QRPatch main](https://github.com/kevin-meng/QRPatch). The intended early version is `v0.1.0-alpha.1`, not a stable 1.0 release.

## What was actually checked

- A remote visual browser opened the [HTMLPreview URL](https://htmlpreview.github.io/?https://github.com/kevin-meng/QRPatch/blob/main/index.html).
- The desktop layout rendered a header, two sidebars, upload controls, the central empty canvas, and the "体验示例画布" button.
- No obvious overlapping components were observed in the initial empty state.
- The interactive-browser tool **could not programmatically access the rendered element IDs** inside the HTMLPreview-hosted document. Consequently it **could not verify** the sample-canvas button, repositioning, clipping, PNG download, or scanability.
- No downloadable screenshot file was returned by the remote browser; **no screenshot was committed**. Do not replace a real screenshot with an AI-generated mock.

## Code added during this pass

- One-click, entirely local sample poster with a deliberately non-scannable **illustrative** QR pattern, to demonstrate layer selection and canvas operations. The demo source does not claim to be a valid QR.
- The demo provides a clear path to interactive review without a real private poster.

## Outstanding release blockers

- [ ] Test on a directly hosted static site or localhost (not an iframe-based HTMLPreview service).
- [ ] Run background and actual QR upload, move, resize, crop and original-resolution PNG export.
- [ ] Decode an exported known-good QR using a real QR scanner.
- [ ] Capture an actual PNG full-page editor screenshot after opening the demo canvas; commit to `docs/assets/editor-preview.png` and link in README.
- [ ] Test desktop and mobile layouts.
- [ ] Create annotated Git tag `v0.1.0-alpha.1` only once above minimum checks pass (the connected GitHub action set does not expose a tag creation operation).

## Screenshot rule

Only commit a screenshot produced by a browser that actually rendered this version; do not use mockups or synthesized approximations.
