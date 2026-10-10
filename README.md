<div align="center">

# QRPatch

**AI creates the art. QRPatch fixes the QR.**

Replace broken QR codes in AI-generated images. Fast, precise, private.

[Try the editor](https://qrpatch-studio.onrender.com) · [Product principles](docs/PRODUCT_PRINCIPLES.md) · [Report an issue](https://github.com/kevin-meng/QRPatch/issues)

</div>

---

## Why QRPatch?

AI image generators can produce beautiful posters, but the QR codes they draw are often unscannable. Instead of repeatedly asking AI to regenerate the entire image, **upload the poster and replace the QR with a real one in seconds.**

**创意交给 AI，二维码由你掌控。** 无需重新生成整张海报，只需上传底图、覆盖错误二维码、拖动缩放真实二维码并导出。

## Quick workflow

**1. Upload** an AI-generated poster → **2. Replace** incorrect QR graphics with your real QR image → **3. Export** as PNG at the original image resolution.

To explore the workspace without uploading a private image, select **体验示例画布** on the opening screen. Its example QR-like pattern is decorative and **not scannable**.

## Two clear editing modes

1. **整体 (Whole layer):** Drag to move the layer. Drag a corner to resize the mask **and** its image together, preserving the chosen crop.
2. **裁切 (Crop):** Drag the image to reframe the contents; drag a corner to resize **only the mask**. Zoom the image independently.
3. Use the small contextual toolbar beside the selected image — `整体 | 裁切 | 图片 − 100% ＋` — or the right inspector to switch modes. The image zoom differs from the canvas viewport zoom.

The original uploaded image is shown outside the mask with a faint preview **only while crop-editing**; export always includes only the selected masked area.

For real QR codes, prefer a square mask, uncut locator patterns, and a white quiet zone. Circular masks are for photos, avatars, and decoration.

[Detailed transform behavior and test contract](docs/TRANSFORM_SPEC.md) · [Run geometry tests](tests/transform-contract.mjs)

## Features

| Feature | Availability |
| --- | --- |
| Local-only PNG / JPG / WebP uploads | ✅ |
| Multiple draggable and resizable image overlays | ✅ |
| Crop masks: rectangle, rounded rectangle and circle | ✅ |
| Independent crop-mask resize and image pan/zoom; whole-layer scaling | ✅ |
| Layer ordering, undo / redo, keyboard nudging | ✅ |
| Export PNG at background image pixel dimensions | ✅ |
| Automatic QR scan validation | Planned |
| Browser-based automated pointer drag regression test | Planned |

> **QR safety:** Keep QR symbols square with sufficient white quiet zone; do not circle-crop QR finder patterns. Circular masks are intended for photos, avatars and decorations. Export scanability is not yet automatically verified.

## Verification

QRPatch includes a real, self-running browser test suite that exercises the deployed editor with an in-memory QR fixture, pointer dragging, both editing modes and a PNG export.

**[Run the interactive browser QA](https://qrpatch-studio.onrender.com/tests/browser-qa.html)** — most recent observed result: **15 PASS · 0 FAIL · 1 SKIP**. All **841 / 841 QR modules** were preserved in the exported PNG. The skipped case is native QR decoding, which requires `BarcodeDetector` support or an external scanner.

The geometry transform contract also runs without dependencies:

```bash
node tests/transform-contract.mjs
```

See [release QA and remaining verification](docs/RELEASE_QA_20261011.md). Manual touch-device QA and independent scanning of the exported image are still pending.

## Preview

[Open the browser preview](https://qrpatch-studio.onrender.com)

The real browser has been exercised by the automated QA runner, but a **persistable page screenshot is still pending**. We will add `docs/assets/editor-preview.png` only after an actual browser screenshot can be exported. We intentionally do not use a fabricated design mock as a product screenshot.

## Run locally

This is currently a dependency-free static application:

```bash
git clone https://github.com/kevin-meng/QRPatch.git
cd QRPatch
python3 -m http.server 8080
```

Visit http://localhost:8080.

No account, AI API, build step, or image upload server is required.

## Documentation

- [Product requirements](docs/PRD.md)
- [Product principles](docs/PRODUCT_PRINCIPLES.md)
- [Technical architecture](docs/TECHNICAL_DESIGN.md)
- [Roadmap](docs/ROADMAP.md)
- [Implementation status](docs/IMPLEMENTATION_STATUS.md)
- [Release QA and blockers](docs/RELEASE_QA_20261011.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)

## Open source

MIT licensed — see [LICENSE](LICENSE).

**Privacy by design:** The editor processes your images directly in the browser without sending them to a remote image-processing service.
