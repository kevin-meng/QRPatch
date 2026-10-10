# QRPatch — Technical Design

Version: 0.1 draft · 2026-10-11

## Architecture decision

Build a **static client-only web app**, without a server dependency for uploads, editing or export.

Suggested stack:
- Vite + React + TypeScript (smaller static footprint than a server-oriented framework for this use case).
- Tailwind CSS for UI primitives, with explicit design tokens.
- Konva + react-konva for interactive stage, transformer, touch support, selection and layers.
- Native Canvas 2D or an offscreen Konva stage for full-resolution export; ensure both use identical scene geometry.
- Optional local QR decode using a maintained browser-compatible library, e.g. jsQR or ZXing, after dependency and browser validation.
- Vitest + React Testing Library for logic/UI; Playwright for desktop/mobile E2E browser checks.

## Why Vite, not Next.js

No authentication, SSR, user API or server rendering is required. Static Vite minimizes operational complexity and is easy to publish on Cloudflare Pages, GitHub Pages, or Vercel. Reconsider only if substantial server features emerge.

## Source structure

```text
src/
  app/                 # shell, router-free entry, localization
  components/          # UI controls, panels, buttons
  editor/
    model/             # stage dimensions, layers, state/history
    canvas/            # Konva stage, selection, transformers
    export/            # full-resolution bitmap renderer
    qr/                # padding, warnings, local decode checks
  lib/                 # file validation, image load, utilities
  styles/              # tokens, global styles
tests/
  fixtures/            # generated/sample QR and backgrounds
docs/
```

## Proposed document and layer schema

```ts
type ImageDocument = {
  version: 1;
  width: number;   // intrinsic original pixels
  height: number;
  backgroundId: string;
  layers: QRLayer[];
};

type QRLayer = {
  id: string;
  assetId: string;
  x: number; y: number; width: number; height: number;
  rotation: number; // MVP: 0 by default; avoid scan-compromising rotation
  visible: boolean;
  zIndex: number;
  backing: {
    enabled: boolean;
    color: string;    // default #FFFFFF
    paddingPx: number;
    cornerRadiusPx: number; // affects backing only
  };
};
```

Use **intrinsic image coordinates** for all saved transforms. Stage scaling changes only the viewport, never geometry or output pixel positions. A separate cover rectangle may be added per QR to hide the original AI pattern before drawing the QR.

QR layers should remain separate from general-purpose decorative image layers. Asset registry holds decoded blob references scoped to the browser session, never external URLs.

## Rendering and export

1. Decode background and code assets to ImageBitmap or HTMLImageElement using local Blob URLs.
2. Fit the editing stage to viewport through a scalar zoom transform.
3. Render layers in intrinsic coordinates; apply stage zoom only at preview.
4. For export, render using original width/height and pixelRatio=1 (or equivalent exact-scale offscreen Canvas). Test for off-by-one pixel / devicePixelRatio mistakes.
5. PNG export via Blob, then trigger a file download.
6. Handle browser canvas dimension/memory limits with a visible warning and opt-in reduced-size fallback. Do not promise losslessness for arbitrary oversized files.

PNG preserves exported pixels without lossy JPEG compression, but an edit/overlay is **not** a byte-for-byte lossless copy of the source JPEG/WebP.

## Security / privacy

- Local file API only. No upload endpoints, remote img src, remote fonts, content analytics, CDN runtime dependencies or webhooks involving images.
- Reject unsupported MIME/extension and failed decoding; cap sizes safely and handle maliciously large images gracefully.
- SVG import deferred due to embedded content and sanitization concerns.
- Avoid persisting original images in localStorage. Persisting projects later needs quota-aware IndexedDB and explicit opt-in.
- Dependency pinning, build audit, CSP and security review before public release.

## Verification strategy

- Geometry unit tests: fit/contain, coordinate mapping, cover rect, quiet zone padding.
- E2E: upload background, upload 3 QR images, select/move/resize, reorder, undo, export.
- Export image size equals intrinsic source size.
- Synthetic known QR samples remain decodable when overlays are large enough and not clipped.
- Test complex original-background cover limitations with visible documentation.
- QA matrix: desktop Chrome/Safari/Firefox, mobile Chrome/Safari.

## Technical risks and mitigation

| Risk | Mitigation |
| --- | --- |
| Browser memory limits | Warn before very large raster operations; offer deliberate downsizing |
| Distorted QR codes | Aspect lock and contain by default, adequate quiet zone |
| Old QR peeking through | Independent opaque cover rectangle and explicit preview |
| Transform/export mismatch | One coordinate system, golden-image E2E tests |
| External data leakage | Static client-only deployment, network tests, no third-party image calls |
| QR decode false confidence | Label as local verification rather than guarantee |
