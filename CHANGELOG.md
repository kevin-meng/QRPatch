# Changelog

## [Unreleased] — Alpha candidate (2026-10-11)

### Added
- Local-first AI-generated poster and QR replacement workspace, multi-layer editing and full-resolution PNG export.
- Square, rounded and circular masks for ordinary images; square with padding recommended for QR.
- Floating contextual toolbar: `整体` (scale/move image and mask together) and `裁切` (move/zoom image independently, or resize mask).
- Local synthetic poster demo and real QR fixture for repeatable testing.
- Online browser regression runner at [tests/browser-qa.html](tests/browser-qa.html).
- Geometry contract suite at [tests/transform-contract.mjs](tests/transform-contract.mjs).

### Fixed
- Whole-layer resize now preserves the selected crop by proportionally transforming the underlying image.
- Initial QR crop preview uses contain-fit and safe padding instead of aggressive cover-fit.
- Image and mask have distinct drag/scale interactions; source preview is translucent outside the crop only during editing.
- Reset and poster replacement release stale in-browser image asset URLs.
- Undo restores editing mode along with layer geometry.

### Verification
- Live Render browser suite: **15 passed, 0 failed, 1 skipped** (native `BarcodeDetector` not supported).
- Exported PNG kept background's **1000 × 700** pixels and matched **841 / 841** QR fixture modules.
- This is an alpha candidate, **not a tagged stable release**.

### Remaining
- Independent scan of the exported real QR on mobile or by an external decoder.
- Real browser screenshot committed under `docs/assets` and referenced in README.
- Cross-browser/touch testing and creation of `v0.1.0-alpha.1` Git tag.

See [release QA](docs/RELEASE_QA_20261011.md).
