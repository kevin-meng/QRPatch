# Contributing to QRPatch

QRPatch has one job: replace incorrect QR codes in AI-generated artwork **faster and more reliably than generating the image again**.

## Quick start

Open `index.html` locally, or run `python3 -m http.server 8080` and navigate to http://localhost:8080.

## Pull requests

1. Explain the user problem and how the change reduces steps in the QR replacement workflow.
2. Keep each pull request focused. Reference an issue for larger changes.
3. Test with a real poster and at least two different QR images: import → select → move → resize → preview → full-resolution PNG export.
4. Include before/after screenshots for UI changes, and describe desktop/mobile checks.
5. Do not add image uploads, background tracking, or remote QR decoding. Processing must remain local.
6. Do not break QR quiet zones or crop QR finder patterns. Circular crops are for decorative pictures only.

## Project philosophy

**Fast, focused, private, reliable.** Resist feature bloat: this is not a general Photoshop clone.

## Security

Report suspected vulnerabilities privately to the maintainer instead of posting private QR contents or tokens to a public issue.

## License

MIT. See LICENSE.
