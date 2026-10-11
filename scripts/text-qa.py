#!/usr/bin/env python3
"""Local-only browser tests for QRPatch P0 text annotations. Never deploys."""
from __future__ import annotations

import functools
import http.server
from pathlib import Path
import struct
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

def png_dimensions(raw: bytes):
    assert raw.startswith(b"\x89PNG\r\n\x1a\n"),"Export must be PNG"
    return struct.unpack(">II",raw[16:24])

def snapshot(page):
    return page.evaluate("() => window.QRPatchQA.snapshot()")

def selected_text(page):
    s=snapshot(page)
    return next(x for x in s["layers"] if x["id"]==s["selected"] and x["kind"]=="text")

def start_poster(page):
    page.goto(page._qr_url+"?qa=1",wait_until="load")
    page.locator("#demo").click()
    page.wait_for_function("() => window.QRPatchQA?.snapshot().layers.length === 1")

def create_text(page, content, style, color):
    page.locator("#textContent").fill(content)
    page.locator("#textColor").fill(color)
    page.locator(f'#textStyles [data-text-style="{style}"]').click()
    page.locator("#addText").click()
    page.wait_for_function("() => window.QRPatchQA.snapshot().layers.some(x => x.kind === 'text')")
    return selected_text(page)

def verify_desktop(browser, url):
    p=browser.new_page(viewport={"width":1510,"height":900},accept_downloads=True)
    p._qr_url=url
    start_poster(p)
    before_layer_count=len(snapshot(p)["layers"])
    assert before_layer_count==1
    # Prevent silent truncation: five input lines must be rejected, never partially rendered.
    p.locator("#textContent").fill("第一行\n第二行\n第三行\n第四行\n第五行")
    p.locator("#addText").click()
    assert len(snapshot(p)["layers"])==1,"A fifth line was silently added/truncated"
    assert "最多支持 4 行" in p.locator("#status").inner_text()
    with p.expect_download(timeout=10000) as baseline_dl:
        p.locator("#export").click()
    baseline=Path(baseline_dl.value.path()).read_bytes()
    content="扫码报名\n加入头马"
    item=create_text(p,content,"white-card","#ec3341")
    assert item["text"]==content and item["textStyle"]=="white-card"
    assert item["color"]=="#ec3341"
    assert item["w"]>30 and item["h"]>30
    assert item["lock"] is True
    out=ROOT/"tests"/"out"
    out.mkdir(parents=True,exist_ok=True)
    p.screenshot(path=str(out/"text-layer-desktop.png"),full_page=True,animations="disabled")
    assert len(snapshot(p)["layers"])==2
    assert p.locator("#textInspector").is_visible()
    assert p.locator("#imageInspector").is_hidden()
    assert p.locator("#quickTools").evaluate("(e)=>e.classList.contains('text-layer-selected')")
    assert not p.locator("#quickCrop").is_visible()
    assert not p.locator("#quickShape").is_visible()
    assert p.locator(".text-thumb").count()==1
    assert p.locator("#textStyles small").count()==0, "Text presets should have no helper captions"
    assert p.locator("#quickTextEdit").is_visible()
    assert p.locator("#quickTextStyle").is_visible()
    assert p.locator("#quickTextColor").is_visible()
    assert p.locator("#quickMore").is_visible()
    assert not p.locator("#quickMove").is_visible()
    # Precise geometry, aspect lock and undo/redo on a text object.
    width=item["w"]
    p.locator("#propW").fill(str(round(width*1.3)))
    p.locator("#propW").press("Tab")
    new_item=selected_text(p)
    assert new_item["w"]>width*1.2,("failed text width resize",new_item)
    assert abs(new_item["w"]/item["w"]-new_item["h"]/item["h"])<0.03
    p.locator("#undo").click()
    assert abs(selected_text(p)["w"]-width)<1.1
    p.locator("#redo").click()
    assert selected_text(p)["w"]>width
    # Edit wording without losing scale or styling.
    p.locator("#textEditContent").fill("立即扫码报名")
    p.locator("#textEditContent").press("Tab")
    assert selected_text(p)["text"]=="立即扫码报名"
    assert selected_text(p)["color"]=="#ec3341"
    # Contextual editor: invalid text does not silently truncate or mutate the layer.
    original = selected_text(p)
    p.locator("#quickTextEdit").click()
    assert p.locator("#textEditPopover").is_visible()
    assert p.locator("#quickTextValue").input_value()=="立即扫码报名"
    p.locator("#quickTextValue").fill("一\\n二\\n三\\n四\\n五".replace("\\\\n","\\n"))
    p.locator("#quickTextApply").click()
    assert p.locator("#textEditPopover").is_visible(), "Validation failure must keep editor open"
    assert "最多支持 4 行" in p.locator("#textEditFeedback").inner_text()
    assert selected_text(p)["text"] == original["text"]
    p.locator("#quickTextValue").fill("扫码立即加入")
    p.locator("#quickTextApply").click()
    changed=selected_text(p)
    assert changed["text"]=="扫码立即加入"
    assert p.locator("#textEditPopover").is_hidden()
    assert abs((changed["x"]+changed["w"]/2)-(original["x"]+original["w"]/2))<1.5
    assert abs((changed["y"]+changed["h"]/2)-(original["y"]+original["h"]/2))<1.5
    # Style changes must preserve user positioning, not put text back in canvas center.
    original=selected_text(p)
    p.locator("#quickTextStyle").click()
    assert p.locator("#textStylePopover").is_visible()
    p.locator('#quickTextStyles [data-quick-text-style="pill"]').click()
    changed=selected_text(p)
    assert changed["textStyle"]=="pill"
    assert abs((changed["x"]+changed["w"]/2)-(original["x"]+original["w"]/2))<1.5
    assert abs((changed["y"]+changed["h"]/2)-(original["y"]+original["h"]/2))<1.5
    assert p.locator("#textStylePopover").is_hidden()
    p.locator("#quickTextStyle").click()
    p.locator('#quickTextStyles [data-quick-text-style="white-card"]').click()
    assert selected_text(p)["textStyle"]=="white-card"
    p.locator("#quickTextColor").click()
    assert p.locator("#textColorPopover").is_visible()
    p.locator('#textColorPopover [data-quick-color="#1964ee"]').click()
    assert selected_text(p)["color"]=="#1964ee"
    assert p.locator("#textColorPopover").is_hidden()
    p.locator("#undo").click()
    assert selected_text(p)["color"]=="#ec3341"
    p.locator("#redo").click()
    assert selected_text(p)["color"]=="#1964ee"
    p.locator("#quickTextColor").click()
    p.locator('#textColorPopover [data-quick-color="#ec3341"]').click()
    assert selected_text(p)["color"]=="#ec3341"
    # Dragging text must move geometry, not force crop/image mode.
    previous=selected_text(p)
    box=p.locator("#canvas").bounding_box()
    width_px=p.evaluate("() => window.QRPatchQA.snapshot().background.width")
    scale=box["width"]/width_px
    x=box["x"]+(previous["x"]+previous["w"]/2)*scale
    y=box["y"]+(previous["y"]+previous["h"]/2)*scale
    p.mouse.move(x,y);p.mouse.down()
    p.mouse.move(x+17,y+12,steps=4);p.mouse.up()
    moved=selected_text(p)
    assert moved["x"]>previous["x"] and moved["y"]>previous["y"],("drag failed",previous,moved)
    # Adding text must change exported pixels, not just the editor selection.
    with p.expect_download(timeout=10000) as dl:
        p.locator("#export").click()
    d=dl.value
    raw=Path(d.path()).read_bytes()
    assert png_dimensions(raw)==(1000,700),png_dimensions(raw)
    assert raw!=baseline,"Adding text did not change exported PNG"
    # Layer order, duplication, removal and undo are inherited from layer system.
    p.locator("#duplicate").click()
    assert len([x for x in snapshot(p)["layers"] if x["kind"]=="text"])==2
    p.locator("#delete").click()
    assert len([x for x in snapshot(p)["layers"] if x["kind"]=="text"])==1
    p.locator("#undo").click()
    assert len([x for x in snapshot(p)["layers"] if x["kind"]=="text"])==2
    p.locator("#redo").click()
    assert len([x for x in snapshot(p)["layers"] if x["kind"]=="text"])==1
    print("Desktop text: add, presets, color, resize, undo/redo, edit, drag, copy/delete, PNG PASS")
    p.close()

def verify_presets_and_mobile(browser,url,w,h):
    ctx=browser.new_context(viewport={"width":w,"height":h},screen={"width":w,"height":h},is_mobile=True,has_touch=True,device_scale_factor=2,accept_downloads=True)
    p=ctx.new_page();p._qr_url=url;start_poster(p)
    for style in ("bold","outline","white-card","pill","caption"):
        # Each style must create a unique independent text layer.
        p.locator("#textContent").fill("扫码报名")
        p.locator(f'#textStyles [data-text-style="{style}"]').click()
        p.locator("#addText").click()
        p.wait_for_function("(style) => window.QRPatchQA.snapshot().layers.at(-1).textStyle===style",arg=style)
        assert selected_text(p)["textStyle"]==style
        assert not p.locator("#quickShape").is_visible()
    assert len([x for x in snapshot(p)["layers"] if x["kind"]=="text"])==5
    assert p.locator("#textStyles small").count()==0
    for button in ("quickTextEdit","quickTextStyle","quickTextColor","quickMore"):
        box=p.locator("#"+button).bounding_box()
        assert box and box["x"]>=0 and box["x"]+box["width"]<=w+1, (button,box)
    p.locator("#quickTextEdit").click()
    assert p.locator("#textEditPopover").is_visible()
    p.locator("#quickTextValue").fill("手机版修改文字")
    p.locator("#quickTextApply").click()
    assert selected_text(p)["text"]=="手机版修改文字"
    p.locator("#quickTextStyle").click()
    p.locator('#quickTextStyles [data-quick-text-style="pill"]').click()
    assert selected_text(p)["textStyle"]=="pill"
    p.locator("#quickTextColor").click()
    p.locator('#textColorPopover [data-quick-color="#ec3341"]').click()
    assert selected_text(p)["color"]=="#ec3341"
    (ROOT/"tests"/"out").mkdir(parents=True,exist_ok=True)
    p.screenshot(path=str(ROOT/"tests"/"out"/f"text-layer-mobile-{w}.png"),full_page=True,animations="disabled")
    # The text preview persists as a vector text layer in export.
    p.locator("#export").click()
    p.locator("#saveSheet:visible").wait_for(timeout=12000)
    wpx,hpx=p.locator("#savePreview").evaluate("(el)=>[el.naturalWidth,el.naturalHeight]")
    assert (wpx,hpx)==(1000,700)
    with p.expect_download(timeout=10000) as dl:p.locator("#saveDownload").click()
    assert dl.value.suggested_filename.endswith(".png")
    p.locator("#saveClose").click()
    print(f"Mobile {w}x{h}: 5 text presets, left composer, export PNG PASS")
    ctx.close()

def main():
    handler=functools.partial(QuietHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            url=f"http://127.0.0.1:{server.server_port}/index.html"
            verify_desktop(browser,url)
            for w,h in [(390,844),(320,720)]:
                verify_presets_and_mobile(browser,url,w,h)
            browser.close()
    finally:server.shutdown();server.server_close()
if __name__=="__main__":main()
