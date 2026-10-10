<div align="center">

# QRPatch

**AI creates the art. QRPatch fixes the QR.**

Replace broken QR codes in AI-generated images. Fast, precise, private.

[Try the editor](https://htmlpreview.github.io/?https://github.com/kevin-meng/QRPatch/blob/main/index.html) · [Product principles](docs/PRODUCT_PRINCIPLES.md) · [Report an issue](https://github.com/kevin-meng/QRPatch/issues)

</div>

---

## Why QRPatch?

AI image generators can produce beautiful posters, but the QR codes they draw are often unscannable. Instead of repeatedly asking AI to regenerate the entire image, **upload the poster and replace the QR with a real one in seconds.**

**创意交给 AI，二维码由你掌控。** 无需重新生成整张海报，只需上传底图、覆盖错误二维码、拖动缩放真实二维码并导出。

## Quick workflow

**1. Upload** an AI-generated poster → **2. Replace** incorrect QR graphics with your real QR image → **3. Export** as PNG at the original image resolution.

To explore the workspace without uploading a private image, select **体验示例画布** on the opening screen. Its example QR-like pattern is decorative and **not scannable**.

## Editor workflow (current build)

1. Upload the poster and the replacement image.
2. Select the overlay on the poster, choose **square / circle / rounded** from the right panel. This activates **in-canvas crop mode**; the separate source-image crop dialog has been removed.
3. Drag inside the selected overlay to reposition the image under its shape, and drag corner handles to resize the visible shape. Adjust **image zoom** independently in the inspector.
4. Select **完成裁切，返回移动模式** to move the complete overlay around the poster, then export the PNG.

For QR codes, prefer a square, complete image with a quiet zone; circle masks can destroy scanability. The crop mode currently requires interactive browser testing across mouse and touch devices.

## Features

| Feature | Availability |
| --- | --- |
| Local-only PNG / JPG / WebP uploads | ✅ |
| Multiple draggable and resizable image overlays | ✅ |
| Crop masks: rectangle, rounded rectangle and circle | ✅ |
| Contain / cover fit, adjustable backing / padding, crop offsets | ✅ |
| Layer ordering, undo / redo, keyboard nudging | ✅ |
| Export PNG at background image pixel dimensions | ✅ |
| Automatic QR scan validation | Planned |
| Interactive crop-content drag, QR auto detection | Planned |

> **QR safety:** Keep QR symbols square with sufficient white quiet zone; do not circle-crop QR finder patterns. Circular masks are intended for photos, avatars and decorations. Export scanability is not yet automatically verified.

## Preview

[Open the browser preview](https://htmlpreview.github.io/?https://github.com/kevin-meng/QRPatch/blob/main/index.html)

A verified, downloadable screenshot of the actual editor has **not yet been captured**. We will add `docs/assets/editor-preview.png` only after an actual browser screenshot can be exported. We intentionally do not use a fabricated design mock as a product screenshot.

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
