# Changelog

## [Unreleased]

### Added
- Dependency-free responsive QRPatch Studio UI.
- Local image upload, multiple overlays, dragging, resizing, ordering, undo/redo, and PNG export.
- Square, rounded and circle masks for overlays.
- Contain/Cover fitting and adjustable white safety padding.
- Crop focal offsets for Cover mode.

### Known limitations
- No automatic QR decoder or proof of scannability.
- QR-specific scan-safe operations are recommendations rather than hard enforced rules.
- No production deployment or reproducible automated browser E2E test suite.
- Independent canvas drag-to-pan inside crop mask is not implemented.

A version tag should only be cut after a reproducible release check.
