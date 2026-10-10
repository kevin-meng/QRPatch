# QRPatch — Alpha release verification (2026-10-11)

## Verified on the public Render deployment

**Editor:** https://qrpatch-studio.onrender.com

**Runnable browser QA:** https://qrpatch-studio.onrender.com/tests/browser-qa.html

**Observed result:** **15 PASS / 0 FAIL / 1 SKIP**, tested through a live remote Chromium browser after commit `ad3314629e11150be867982bef5679af103ca278` was deployed on Render with status `Live`.

| Test group | Observed result |
| --- | --- |
| Editor load, demo poster, floating toolbar | PASS |
| Upload a real QR PNG from an in-memory fixture | PASS |
| Enter crop mode without automatically clipping QR finder patterns / quiet zone | PASS |
| Zoom source image independently of the crop mask | PASS |
| Resize crop mask independently of source image | PASS |
| Drag source image inside the mask | PASS |
| Return to overall mode and scale image together with mask | PASS |
| Drag overall frame corners; move the whole layer with source image | PASS |
| Export original-size **1000 × 700** PNG | PASS |
| Compare exported QR pixels against fixture's **29 × 29 = 841** modules | **PASS: 841 / 841 matched** |
| Switch square, circle and rounded mask shapes | PASS |
| Reset project and revoke old object URLs | PASS |
| Decode the *exported* QR with native browser BarcodeDetector | **SKIP: unsupported in this browser** |

The fixture `QRPATCH-E2E-01` is a real QR image, not the decorative sample from the home-screen demo. Independent OpenCV decoding confirmed that the original generated fixture encodes `QRPATCH-E2E-01`. The online pixel-fidelity test confirms that exporting the unmodified QR overlay preserved **all sampled module centers**, but this is **not a substitute** for decoding the exported PNG with a camera or decoder.

## Implementation and design changes

- A contextual floating toolbar enables two clearly separated modes: **整体** scales/translates both source image and mask, **裁切** edits image pan/zoom and mask independently.
- Image zoom and frame resize preserve image aspect ratio and keep the selected crop composition when moving between modes.
- Normal QR overlays enter crop mode in **contain** fit with safety padding, rather than cover fit that may cut the QR.
- Previous file object URLs are revoked when replacing the poster or resetting the project.
- Test hooks are present only under `?qa=1`. Production UI remains local-only.

## Evidence and reproduction

1. Open [the browser test runner](https://qrpatch-studio.onrender.com/tests/browser-qa.html) and review the final PASS/FAIL/SKIP totals and individual assertions.
2. Run `node tests/transform-contract.mjs` to validate the transform geometry locally.
3. For manual checking, upload your own test poster and known-valid QR in the [editor](https://qrpatch-studio.onrender.com), crop, switch to whole-mode resize, export, and scan the result with a phone.

Browser QA dispatches pointer events to the actual editor canvas and reads the exported PNG. A human desktop mouse/touch-device visual acceptance pass has not been performed in every browser.

## Remaining pre-release work

- [x] Direct static deployment on Render.
- [x] Real browser canvas interaction tests and PNG pixel-resolution test.
- [x] Confirm the complete 29×29 QR fixture has been preserved in the exported PNG.
- [ ] Decode an exported PNG with a QR scanner across representative poster sizes; test mobile touch and Safari.
- [ ] Capture and commit the **real editor screenshot** to `docs/assets/editor-preview.png` (not yet done). A reproducible capture helper is now available: `python scripts/capture-preview.py` after installing Python Playwright and Chromium; the helper opens the actual local `index.html`, loads the demo, saves the real screenshot, and adds the README image reference. The available remote browser did not expose a persistable screenshot asset.
- [ ] Create a Git tag `v0.1.0-alpha.1` after the release artifacts are available. The connected GitHub actions here do not expose tag creation; a branch or documentation filename must not be passed off as a tag.

## Safety notes

The decorative QR-like illustration used by **体验示例画布** is intentionally non-scannable. Circle and rounded masks can impair QR decoding; QR content should normally remain complete and square, with a sufficiently large quiet zone. QR image edits stay inside the browser.
