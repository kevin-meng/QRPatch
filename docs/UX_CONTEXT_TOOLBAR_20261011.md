# Contextual toolbar UX — 2026-10-11

QRPatch uses two contextual surfaces, not a dense global inspector.

## QR and image overlays

The floating toolbar follows the selected image:
`整体 | 裁切 | 形状 ▾ | 图片 − 100% ＋ | ⋯`

- **整体** moves and scales image and mask together, maintaining framing.
- **裁切** moves/zooms the image behind an independent mask.
- **形状** has 方形, 圆角, 圆形; choosing a shape enters crop mode.
- **图片 −/＋** zooms source without resizing mask.
- **⋯** holds secondary actions: white backing, duplicate, delete.
- The right sidebar retains precise coordinates, padding, fit details, and layer ordering, but no duplicate shape selector.
- QR images should normally keep their complete square quiet zone.

## Background image

Click the poster canvas outside overlays to select the background. Its floating toolbar:
`背景图片 | 更换 | 调整 | 重置调色`

- **更换** retains overlays when pixel dimensions match. It confirms before clearing overlays for differently sized backgrounds.
- **调整** sets brightness/contrast, 40–160%, applied to the **background only** in canvas and PNG export.
- **重置调色** restores 100% brightness/contrast.
- Color adjustments do not resize the canvas, recolor overlays, or change exported resolution.

Floating toolbars are editor-only, menus are mutually exclusive, and the UI wraps on narrow screens. Position/size numeric controls and undo/redo remain available.

## QA

On 2026-10-11 the live browser runner passed **20 tests, 0 failures, 1 skipped** (native BarcodeDetector unsupported). New checks cover the shape popup, background selection, background pixel adjustments without QR pixel changes, background replacement preservation, and prior mask/PNG transforms.

https://qrpatch-studio.onrender.com/tests/browser-qa.html
