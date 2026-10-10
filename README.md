# QRPatch

**Fix broken QR codes in AI-generated images.**  
修复 AI 生成图片中的无效二维码，并精准叠加真实、可扫描的二维码。

QRPatch is an open-source, privacy-first browser image editor. Images stay on your device.

## Product goals

- Upload a background image and one or more QR code images.
- Select replacement regions; drag, resize and arrange QR overlays.
- Preserve QR quiet zones and original image dimensions in export.
- Export a high-quality PNG without uploading image data to a server.
- Work on desktop and mobile browsers.

## Status

**Planning / requirements stage.** No application implementation has been shipped yet.

## Documents

- [Product requirements (PRD)](docs/PRD.md)
- [Technical design](docs/TECHNICAL_DESIGN.md)
- [Roadmap and acceptance criteria](docs/ROADMAP.md)

## Scope

The initial release focuses on reliable *flat/axis-aligned* overlays. Perspective warp, automatic QR detection, batch generation, and user accounts are explicitly deferred.

## License

A license has not yet been selected. Public visibility alone is not an open-source license; choose an OSI-approved license before inviting reuse or external contributions.
