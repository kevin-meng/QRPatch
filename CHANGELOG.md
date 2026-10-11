# Changelog

## [Unreleased] — Mobile PNG download simplification (2026-10-11)

- Removed `分享 / 存到相册` from the mobile export sheet because WeChat can block system sharing.
- The preview now has a single **下载 PNG** button. Kept the original-resolution export and adjusted helper text to accurately describe browser download limitations.
- Removed Web Share API invocation and all share-to-Photos/WeChat guidance.
- Added a mobile regression assertion that only one export action is displayed and PNG download still works.


## [v0.1.0-alpha.3] — Mobile editing & export (2026-10-11)

### Fixed
- Mobile contextual toolbar no longer follows the small scaled poster image to narrow or clipped positions; it docks at the bottom of the editing area and wraps controls into two touch-friendly rows.
- Shape, background and more-action popovers open above the docked toolbar.
- Touch resize corners use a larger capture radius on phone-size screens.
- Mobile PNG export presents an image preview with native PNG file-share, long-press image save and browser-download fallbacks, plus clear iOS Photos and Android guidance.
- Desktop direct PNG download remains unchanged.

### Verified
- Both **390×844** and **320×720** Chromium mobile emulations: image toolbar, crop shape, background settings, 1000×700 PNG preview and actual PNG download passed.
- Original desktop geometry and E2E tests passed in the same alpha.3 release pipeline.
- Native iOS Safari/WeChat saving to Photos requires a device-side check: no webpage can universally save files directly to the Photos library.

## [Unreleased] — Contextual toolbar iteration (2026-10-11)

### Changed
- Moved overlay crop shape selection from the inspector into the floating image toolbar.
- Added More actions: white backing, duplicate, delete.
- Added a floating background toolbar: replace poster, brightness, contrast, reset grading.
- Same-size background replacement preserves overlays; mismatched sizes request confirmation.
- Background filters affect only the poster, never overlaid QR/image pixels.
- Expanded browser regression QA to 20 passing tests (1 native decoder test skipped).

[Contextual toolbar UX specification](docs/UX_CONTEXT_TOOLBAR_20261011.md).

## [v0.1.0-alpha.1] — Alpha candidate (2026-10-11)

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
