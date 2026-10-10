# QRPatch — Roadmap and Acceptance Gate

Version: 0.1 draft · 2026-10-11

## Build philosophy

Ship one practical, dependable capability at a time. Use small focused commits; for each module document expected behavior, test against acceptance checks, and only then proceed. No CI service is required for early iteration, but local validation is mandatory.

## Phase 0 — Foundation

- [ ] Initialize Vite React TypeScript app; lint, typecheck, tests.
- [ ] Add responsive shell, design tokens, zh-CN and en copy.
- [ ] Add open-source license after selection, CONTRIBUTING and privacy statement.
- **Gate:** production build works, static deployment renders, no external image egress.

## Phase 1 — Editor MVP

- [ ] Background image importer with error/limit handling.
- [ ] Multiple QR asset importing and per-layer visibility, selection and deletion.
- [ ] Canvas drag, aspect-locked resize, zoom and mobile gestures.
- [ ] Rectangular target area/cover layer and adjustable opaque backing/quiet zone.
- [ ] Layer ordering, keyboard adjustments, undo/redo.
- [ ] Full-intrinsic-resolution PNG export.
- **Gate:** one poster with 3 distinct QR overlays exports at exact source dimensions; controls work across desktop and mobile.

## Phase 2 — Quality & initial public release

- [ ] Local decode verification (imported QR and exported result where practical), warnings with actionable fixes.
- [ ] Accessibility and low-contrast/cropping warnings.
- [ ] Automated geometry and browser E2E tests with generated known QR fixtures.
- [ ] GitHub README, screenshots, license, contribution guide and deployment.
- **Gate:** reproducible QA evidence, documented limitations, easy one-click web access.

## Phase 3 — Advanced capabilities (post-MVP)

- [ ] Auto-detect QR-like locations as user-confirmed suggestions.
- [ ] Perspective/four-corner warp with export parity and scan warnings.
- [ ] Local project drafts and template reuse.
- [ ] Bulk personalization, CSV mapping and ZIP export.
- **Gate:** evaluate actual user demand before implementing costly features.

## Definition of done for every item

1. Behavior matches written PRD and has no unexpected network upload.
2. Edge cases and failure states are clear.
3. Typecheck, lint, unit tests and relevant browser tests pass locally.
4. Tests or manual QA evidence noted in commit/PR.
5. Documentation updated when design or behavior changes.

## Current status

Requirements and technical design recorded. **No implementation, tests, or deployment have been completed yet.**
