# QRPatch — Product Requirements Document

- Version: 0.1 (draft)
- Date: 2026-10-11
- Status: Ready for MVP implementation planning
- Product: Free, privacy-first browser QR replacement editor

## 1. Problem and product promise

Generative image models often draw QR-code-shaped patterns that are not valid scannable QR codes. Users need to replace such regions with existing, real QR images **without recreating the entire poster**.

**Promise:** Upload a poster, place one or multiple real QR codes precisely, verify scannability where possible, and export at the source image's original pixel dimensions.

The product does not claim to reconstruct obscured background pixels, guarantee scanning in every external camera app, or guarantee scanability of extremely small or perspective-distorted QR symbols.

## 2. Users and scenarios

1. Creators: replace AI poster QR graphics with a real website/event code.
2. Community organizers: put group, registration, or event QR codes into one poster.
3. Small businesses: prepare promotional graphics with multiple campaign QR codes.
4. Future: batch-personalize one poster with an individual's QR.

## 3. Core workflow

1. Open the web app; no account or onboarding required.
2. Upload / drag and drop / paste a background PNG, JPEG, or WebP.
3. Upload one or more QR images (PNG, JPEG, WebP; SVG deferred until sanitized handling is implemented).
4. For each code: add a new layer, position it by dragging, scale using handles, optionally select a target rectangle as a guide.
5. Fine-tune dimensions, padding, background and stacking order using accessible controls.
6. Inspect the composite; optionally run QR scan checks.
7. Export at source resolution as PNG; image processing remains local.

An uploaded QR image is treated as an **image overlay**; the application must not regenerate or rewrite its encoded destination.

## 4. MVP functional requirements (P0)

| ID | Requirement | Acceptance |
| --- | --- | --- |
| P0-01 | Upload one background image | PNG/JPEG/WebP via picker or drop; dimensions shown; unsupported/corrupt format gets meaningful error |
| P0-02 | Add multiple independent QR image layers | At least 5 layers can be added; selection, editing and deletion affect only active layer |
| P0-03 | On-canvas positioning | Drag and resize via handles; preview coordinates map accurately to export pixels |
| P0-04 | Area replacement | User draws a rectangular target region or places an overlay directly; old visual is concealed by an opaque backing as needed |
| P0-05 | QR safety controls | Default preserve full symbol, no cropping, square geometry and adequate quiet zone; optional opaque white backing and padding |
| P0-06 | Basic styling | Rectangular and rounded *background container*; code pixels themselves remain unmasked; aspect lock enabled by default |
| P0-07 | Layer operations | Select, hide/show, delete, bring forward/send backward; displayed in layers panel |
| P0-08 | Undo/redo | Undo/redo layer operations in the current session; bounded history |
| P0-09 | Export | Full-resolution PNG export respecting exact source canvas size; no forced thumbnail output |
| P0-10 | Responsive and keyboard | Desktop editing, mobile touch drag and resize, keyboard nudging and accessible input labels |
| P0-11 | Privacy | No server-side upload, image telemetry, mandatory sign-in or third-party image-host dependency |
| P0-12 | Chinese/English | Initial UI supports zh-CN and en; English README for open-source discoverability |

## 5. Important UX decisions

### 5.1 Crop modes: code vs decoration

**Never circular-crop a QR symbol by default.** A QR code may become unscannable if the finder patterns or quiet zone are removed. The user originally requested square/circular cropping, so expose:

- **QR-safe mode (default):** complete QR image in a square code area, with a white quiet-zone/backing layer. May use a rounded *outer* background without touching QR pixels.
- **Decorative image mode (later):** circle, rounded rectangle or custom image mask for avatar/logo/non-QR images.
- **Advanced unsafe mode (later, explicit warning):** custom QR crop/mask, not represented as scan-safe.

### 5.2 Covering the old AI QR

Adding a new QR is not the same as repairing the underlying image. MVP covers the original incorrect QR with an opaque rectangle under the replacement code. User can adjust the cover region and background color; results may be visible if the original region has a complex texture. Background-aware inpainting is out of scope.

### 5.3 Scanning status

- MVP may provide optional local decode for imported QR and exported composite using a browser QR decoder library.
- A decoder success is a **positive check, not a universal guarantee**; warn about small QR dimensions, low contrast, incomplete quiet zones, overlays, and compression.
- If local decoding fails, allow export with a clear warning; never claim "100% scannable."

## 6. Initial page layout

Single-page editor:
- Header: product name, language toggle, privacy note and GitHub link.
- Left panel (desktop): background import and QR asset/layer list.
- Center: zoomable, pan-able editing canvas with selection handles.
- Right panel: selected overlay properties (position, size, backing, padding, layer order).
- Footer/bottom bar: zoom/reset, undo/redo, verification and export.
- Mobile: canvas first; asset and properties panels collapse into bottom sheets/tabs.

Avoid lengthy marketing/onboarding flows. Offer one realistic local sample graphic only if it can ship without remote requests.

## 7. Non-functional requirements

- No backend or database in MVP; static hosting.
- Original image aspect ratio and pixel dimensions preserved by default.
- Editing preview may be downscaled for speed; export must render to full original dimensions.
- Sensible limits and memory warnings for very large images; never silently reduce export quality/resolution.
- Do not log user image content or encoded QR data.
- All object URLs, canvas buffers, and decode resources released when no longer needed.
- Mobile Safari and Chrome supported in QA alongside desktop Chrome, Safari, and Firefox.
- The UI should be visually polished but lightweight: clear hierarchy, subtle colors and consistent control states, no exaggerated gradients.

## 8. Deferred scope

**P1:** save/load project locally, QR auto-detection as suggested rectangles (manual confirmation), stronger local decode diagnostics, copy/paste overlays, faster alignment tools.

**P2:** four-point perspective transform (requires warp rendering and post-warp scanning warnings); batch personalization via CSV and ZIP; template reuse; API/SDK or embeddable mode.

**Not planned for MVP:** AI inpainting, cloud image storage, remote OCR/vision API, payment, registration, analytics tied to images, animated QR artwork, circular cropping of QR modules.

## 9. Success and measurement

For MVP, measure through manual reproducible QA, not user tracking:

- Users can produce a correct PNG with 1 or 3 independent QR overlays.
- Preview/export alignment has no visible drift at common zoom levels.
- QR imported with clean padding can be decoded locally in representative sample tests.
- Editing operates with mouse and touch; undo/redo restores the correct layer state.
- Browser network inspection shows no image or QR payload egress.

## 10. Open-source release requirements

Include an OSI-approved license (decision pending), CONTRIBUTING.md, issue templates and basic security/privacy documentation before announcing the project externally. No contribution/license claims until the actual license is committed.
