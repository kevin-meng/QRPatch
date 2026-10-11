#!/usr/bin/env python3
"""Mobile regression: responsive contextual toolbar and an actually savable PNG.

Run after: pip install playwright && python -m playwright install chromium
"""
from __future__ import annotations

import functools
import http.server
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def verify_mobile(browser, url: str, width: int, height: int) -> None:
    context = browser.new_context(
        viewport={"width": width, "height": height},
        screen={"width": width, "height": height},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        accept_downloads=True,
    )
    page = context.new_page()
    page.goto(url + "?qa=1", wait_until="load")
    page.locator("#demo").click()
    page.locator("#quickTools:visible").wait_for(timeout=15000)

    def check_toolbar(toolbar_id: str) -> None:
        bar = page.locator(toolbar_id)
        rect = bar.bounding_box()
        assert rect is not None, f"{toolbar_id}: no bounding box"
        assert rect["x"] >= -1, f"{toolbar_id}: left edge off screen {rect}"
        assert rect["x"] + rect["width"] <= width + 1, (
            f"{toolbar_id}: right edge off screen {rect}"
        )
        assert rect["y"] >= -1, f"{toolbar_id}: top edge off screen {rect}"
        assert rect["y"] + rect["height"] <= height + 1, (
            f"{toolbar_id}: bottom edge off screen {rect}"
        )
        host = page.locator(toolbar_id).evaluate("(el) => el.parentElement.id")
        assert host == "canvasArea", f"{toolbar_id}: toolbar remains in scaled stage"

    check_toolbar("#quickTools")
    page.locator("#quickShape").click()
    page.locator("#shapePopover:visible").wait_for()
    page.locator("#shapePopover [data-shape=circle]").click()
    assert page.locator("#quickShape").inner_text().startswith("◯")
    page.locator("#quickMove").click()

    # Check the background toolbar and its popover.
    page.locator("#canvas").click(position={"x": 12, "y": 12})
    page.locator("#bgTools:visible").wait_for()
    check_toolbar("#bgTools")
    page.locator("#bgAdjust").click()
    page.locator("#bgPopover:visible").wait_for()
    page.locator("#bgContrast").evaluate(
        """(el) => {el.value='118'; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));}"""
    )
    page.locator("#bgAdjust").click()

    # Mobile export should open a full-resolution image preview with
    # system-share fallback AND an actual browser-download action.
    page.locator("#export").click()
    page.locator("#saveSheet:visible").wait_for(timeout=20000)
    page.wait_for_function(
        "() => { const i=document.getElementById('savePreview'); return i.complete && i.naturalWidth>0; }"
    )
    size = page.locator("#savePreview").evaluate(
        "(el) => [el.naturalWidth, el.naturalHeight]"
    )
    assert size == [1000, 700], f"PNG preview lost original resolution: {size}"
    assert page.locator("#saveShare").count() == 0, "shared-to-WeChat/Photos button must be removed"
    assert page.locator("#saveDownload").is_visible()
    assert page.locator(".save-actions button").count() == 1, "mobile export must show only Download PNG"
    assert page.locator("#saveHelp").inner_text().find("下载 PNG") >= 0

    with page.expect_download(timeout=12000) as dl:
        page.locator("#saveDownload").click()
    download = dl.value
    assert download.suggested_filename.endswith(".png"), "download is not PNG"
    page.locator("#saveClose").click()
    assert page.locator("#saveSheet").is_hidden()

    print(f"Mobile {width}×{height}: toolbar/docking, crop shape, background, PNG preview/download PASS")
    context.close()


def main():
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0),
        functools.partial(QuietHandler, directory=str(ROOT)),
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            base = f"http://127.0.0.1:{server.server_port}/index.html"
            for width, height in [(390, 844), (320, 720)]:
                verify_mobile(browser, base, width, height)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
