# QRPatch — Development checkpoint (2026-10-11)

## Implemented in this iteration

- Added **Contain** (preserve source image aspect ratio, entire image visible) and **Cover** (center crop to fill) per overlay. Rendering uses the same logic for editor preview and full-resolution PNG export.
- Added adjustable **white padding percentage** (0–30%) around overlaid images; recommended for QR quiet zones. White padding takes effect when the background backing is enabled.
- Square / circle selection now creates a **1:1 bounding frame** and turns aspect lock on.
- Existing pointer positioning, resize handles, multiple layers, undo/redo and original-pixel-size export remain in the existing standalone app.

## How to use

1. Open `index.html` (or serve the repository root as static HTML).
2. Upload background; upload QR image / avatar image.
3. Drag or resize the layer on the canvas. Select a layer, then set its crop shape and fit method in the inspector.
4. For scannable QR images, use **square + contain + opaque white backing + 8% or more padding**; avoid circle cropping.
5. Use **circle + cover** for avatar/decorative images.
6. Export PNG.

## QA and limitations

**Remote code was committed and reviewed at the source level only. No interactive browser screenshot, mobile device pass or actual QR scan test has been completed.** A local runtime request for the GitHub raw file failed due to the environment's DNS access restriction. Do not advertise a guaranteed production-quality QR decoder or browser-tested release.

Remaining gaps:
- Cropping uses a centered contain/cover calculation; no independent panning of the image inside the mask or interactive crop mode yet.
- Geometry starts with the imported image's intrinsic aspect ratio even though the initial shape selector reads square. Explicitly clicking square normalizes to 1:1. This needs a consistent default.
- Circular masking is allowed for all image types and remains unsafe for many QR codes.
- The app does not validate QR decode success. There is no local QR decoder bundled yet.
- The padding backing is a white composited background, not automatic detection of an already-existing quiet zone.
- Layer state is browser-memory-only; no saved project format.
- No automated browser tests or screenshot comparison have been established.

## Next priorities

1. Resolve layer-type awareness and initial square defaults; protect QR-specific operations with explicit scan risk warnings.
2. Add separate crop-window drag/pan for avatars while preserving QR quiet zones.
3. Add a local, on-device decode library and readable verification results for the exported PNG.
4. Add Playwright E2E and visual regression tests before claiming cross-browser readiness.
