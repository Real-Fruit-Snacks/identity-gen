"""Checks the release's index.html opened straight from disk (file://) with the network blocked.

Build it first with python tools/build-standalone.py, then:

    python tests/test_download.py                         # dist/index.html in Chromium and Firefox
    python tests/test_download.py PATH --browsers chromium

Each browser gets a dead proxy, offline mode and a request log, and the check fails if the page asks for
anything that isn't file:, data: or blob:. It then checks the six IBM Plex faces actually loaded (not
just that nothing errored), the icon decodes, the page makes and rerolls identities and avatars, the
service worker stays unregistered, and nothing errors or shows the update notice.
"""
import argparse
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = ("file:", "data:", "blob:", "about:")
FACES = {("IBM Plex Sans", w) for w in ("400", "600", "700")} | {("IBM Plex Mono", w) for w in ("400", "500", "600")}

ap = argparse.ArgumentParser(description="Check the standalone index.html from file:// with no network.")
ap.add_argument("path", nargs="?", default=os.path.join(ROOT, "dist", "index.html"))
ap.add_argument("--browsers", default="chromium,firefox", help="comma-separated: chromium, firefox")
ap.add_argument("--shots", help="folder to save a screenshot per browser into")
args = ap.parse_args()

path = Path(args.path).resolve()
if not path.is_file():
    sys.exit("no file at %s (run python tools/build-standalone.py first)" % path)
URL = path.as_uri()
failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


with sync_playwright() as p:
    for name in [b.strip() for b in args.browsers.split(",") if b.strip()]:
        browser = getattr(p, name).launch(proxy={"server": "http://127.0.0.1:9"})
        ctx = browser.new_context(offline=True, viewport={"width": 900, "height": 1200})
        remote, errors, console = [], [], []
        ctx.on("request", lambda r: None if r.url.startswith(LOCAL) else remote.append(r.url))
        ctx.route("**/*", lambda route: route.continue_() if route.request.url.startswith(LOCAL) else route.abort())
        page = ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
        page.goto(URL)
        page.wait_for_timeout(500)
        tag = "[%s] " % name

        faces = page.evaluate("""async () => {
            await document.fonts.ready;
            const faces = [...document.fonts].filter(f => f.family.replace(/["']/g, "").startsWith("IBM Plex"));
            await Promise.allSettled(faces.map(f => f.load()));
            return faces.map(f => [f.family.replace(/["']/g, ""), String(f.weight), f.status]);
        }""")
        loaded = {(fam, w) for fam, w, status in faces if status == "loaded"}
        check(tag + "all six IBM Plex faces load from the file", loaded == FACES)
        check(tag + "body and labels render in IBM Plex",
              page.evaluate("""() => document.fonts.check('400 15px "IBM Plex Sans"') && document.fonts.check('500 10.5px "IBM Plex Mono"')
                  && getComputedStyle(document.body).fontFamily.startsWith('"IBM Plex Sans"')"""))
        check(tag + "icon is built in and decodes", page.evaluate("""() => new Promise(done => {
            const link = document.querySelector('link[rel="apple-touch-icon"]');
            if (!link) return done(false);
            const img = new Image();
            img.onload = () => done(img.naturalWidth === 192);
            img.onerror = () => done(false);
            img.src = link.href;
        })"""))

        first = (page.text_content("#name") or "").strip()
        check(tag + "identity renders", bool(first))
        names = set()
        for _ in range(5):
            page.click("#new")
            names.add((page.text_content("#name") or "").strip())
        check(tag + "New identity makes new people", len(names - {"", first}) >= 4)
        for style in ["pixel", "duck", "house"]:
            page.select_option("#astyle", style)
            page.click("#newphoto")
            page.wait_for_timeout(80)
            check(tag + "avatar renders: " + style, page.locator("#photo svg").count() == 1)
        check(tag + "seed shown", bool((page.text_content("#seedview") or "").strip()))
        check(tag + "footer shows the version", (page.text_content("#ver") or "").startswith("v"))

        check(tag + "no service worker", page.evaluate("() => !navigator.serviceWorker || !navigator.serviceWorker.controller"))
        check(tag + "no update notice", not page.locator("#update.show").count())
        check(tag + "no page errors", not errors)
        check(tag + "no console errors", not console)
        check(tag + "no requests beyond the file", not remote)
        for line in errors + console:
            print("    " + line)
        for url in sorted(set(remote)):
            print("    request: " + url)
        if args.shots:
            os.makedirs(args.shots, exist_ok=True)
            page.screenshot(path=os.path.join(args.shots, name + ".png"), full_page=True)
        browser.close()

if failures:
    print(f"\n{len(failures)} failure(s): " + ", ".join(failures))
    sys.exit(1)
print("\nall checks passed")
