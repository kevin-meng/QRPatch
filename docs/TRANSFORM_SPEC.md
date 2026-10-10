# Canvas transform contract

QRPatch has two operations that must never be conflated.

## Overall mode (整体)

A selected layer is a **composition**: a mask frame and the source image positioned behind it.

- Drag the frame interior: move both frame and source image by the same amount.
- Drag a corner: scale the frame **and** the entire source-image rectangle using the same uniform scale (lock ratio is on by default).
- Switching from crop mode back to overall mode must not discard image pan, zoom, or the selected region.
- Numeric position/size controls and arrow-key nudges respect the same rules.
- The exported image displays only the masked composition. The faint full-image preview and control handles are editor-only.

## Crop mode (裁切)

- The mask shape and source image are **independent**.
- Drag frame corners to resize **only the mask**.
- Drag inside the mask to pan **only the image**.
- Use the image zoom slider or floating +/- buttons to zoom **only the image**, preserving the source image's natural aspect ratio.
- The original image is drawn at reduced opacity outside the mask during editing, for context.
- Shape choice is exclusive: square, rounded, or circle. There is no separate crop popup.
- Leaving crop mode returns to overall mode without changing the composition.

## Floating toolbar

The contextual toolbar follows the selected element within the visible canvas and always exposes:

`整体 | 裁切 | 图片 − 100% ＋`

`整体` and `裁切` are mode switches; `图片 −/＋` affect source zoom only, not the poster viewport zoom.

## Verification

Run `node tests/transform-contract.mjs` to check geometry contracts without packages or services. Browser QA must separately test pointer capture, resize handles, editing, crop preview, exported image and responsive layout with real assets.

For real QR codes, use a square mask, uncut finder patterns and sufficient white quiet zone. The demo QR-like artwork is illustrative and cannot be scanned.
