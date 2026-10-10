#!/usr/bin/env python3
"""Capture a real, local QRPatch editor screenshot and add it to README.

One-time setup:
    python -m pip install playwright
    python -m playwright install chromium
Then:
    python scripts/capture-preview.py

The screenshot is captured from the actual index.html at this checkout,
with an interactive demo canvas; not an AI mockup.
"""
from __future__ import annotations

import functools
import http.server
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "editor-preview.png"
README = ROOT / "README.md"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def main():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/index.html"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={"width": 1560, "height": 940},
                device_scale_factor=1,
                color_scheme="light",
            )
            page.goto(url, wait_until="load")
            page.get_by_role("button", name="体验示例画布").click()
            page.locator("#stage").wait_for(state="visible")
            page.locator("#quickTools").wait_for(state="visible")
            page.wait_for_function(
                "() => document.getElementById('layerCount').textContent === '1'"
            )
            OUT.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(OUT), full_page=True, animations="disabled")
            print(f"Captured actual editor: {OUT} ({OUT.stat().st_size} bytes)")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    text = README.read_text(encoding="utf-8")
    image = "![QRPatch Studio — real editor screenshot](docs/assets/editor-preview.png)"
    preview_link = "[Open the browser preview](https://qrpatch-studio.onrender.com)"
    if image not in text:
        assert preview_link in text, "README preview section changed; update manually"
        text = text.replace(preview_link, preview_link + "\n\n" + image, 1)
        text = text.replace(
            "The real browser has been exercised by the automated QA runner, but a **persistable page screenshot is still pending**. We will add `docs/assets/editor-preview.png` only after an actual browser screenshot can be exported. We intentionally do not use a fabricated design mock as a product screenshot.",
            "Screenshot generated from the actual QRPatch editor, with its demo canvas active. The demo's QR-like illustration is not scannable.",
        )
        README.write_text(text, encoding="utf-8")
        print("README updated to reference actual screenshot.")
    print("Review the image before committing; no screenshot is fabricated or committed automatically.")


if __name__ == "__main__":
    main()
