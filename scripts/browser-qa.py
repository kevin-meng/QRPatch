#!/usr/bin/env python3
"""Run the real QRPatch browser QA suite locally. Exits nonzero on any failed assertion."""
from __future__ import annotations

import functools
import http.server
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def main():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={"width": 1560, "height": 940},
                accept_downloads=True,
                device_scale_factor=1,
            )
            url = f"http://127.0.0.1:{server.server_port}/tests/browser-qa.html"
            page.goto(url, wait_until="load")
            page.locator("#summary[data-finished='true']").wait_for(timeout=60000)
            summary = page.locator("#summary").inner_text()
            failures = page.locator("#summary").get_attribute("data-failed")
            print("QRPatch browser test:", summary)
            for entry in page.locator("#log .entry").all_inner_texts():
                print(entry)
            browser.close()
            if failures != "0":
                raise SystemExit("QRPatch browser QA failed: " + summary)
            if "15 通过" not in summary:
                raise SystemExit("Browser QA unexpectedly skipped required test assertions: " + summary)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
