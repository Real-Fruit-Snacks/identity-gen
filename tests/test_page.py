"""Browser checks for identity-gen. Run: pip install playwright && playwright install chromium && python tests/test_page.py"""
import json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "file://" + os.path.join(ROOT, "index.html")
failures = []

def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(accept_downloads=True, viewport={"width": 900, "height": 1200})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    page.wait_for_timeout(300)

    name = page.text_content("#name")
    check("identity renders", bool(name and name.strip()))
    check("password defaults to a passphrase", "-" in page.locator("#account dd").nth(3).text_content())

    seed = page.text_content("#seedview")
    for _ in range(5):
        page.click("#new")
    page.fill("#seedin", seed)
    page.click("#loadseed")
    page.wait_for_timeout(200)
    check("seed restores the same identity", page.text_content("#name") == name)

    page.click("#new")
    check("undo enabled after new identity", not page.is_disabled("#undo"))
    page.click("h1")
    page.keyboard.press("u")
    page.wait_for_timeout(200)
    check("undo shortcut restores previous identity", page.text_content("#name") == name)

    page.click("#addsec")
    page.keyboard.type("What was your first car?")
    page.keyboard.press("Enter")
    check("security question added", page.locator("#security dt").count() == 1)
    page.click("#addcustom")
    page.keyboard.type("Referral code")
    page.keyboard.press("Enter")
    check("custom field added", page.locator("#custom dt").count() == 1)

    with page.expect_download() as d:
        page.click("#dltext")
    text = open(d.value.path()).read()
    check("text export includes security question", "What was your first car?" in text)
    check("text export includes custom field", "Referral code" in text)
    check("email handle has no trailing @", "@" not in [l for l in text.splitlines() if "Email handle" in l][0])

    for style in ["initials", "pixel", "duck", "house", "marble", "bauhaus", "sunset", "terrain", "rings", "bloom"]:
        page.select_option("#astyle", style)
        page.click("#newphoto")
        page.wait_for_timeout(80)
        check(f"offline style renders: {style}", page.locator("#photo svg").count() == 1)

    page.select_option("#astyle", "pixel")
    for _ in range(100):
        page.click("#newphoto")
    check("100 pixel renders without errors", not errors)
    page.select_option("#astyle", "duck")
    for _ in range(100):
        page.click("#newphoto")
    check("100 duck renders without errors", not errors)
    page.select_option("#astyle", "house")
    for _ in range(100):
        page.click("#newphoto")
    check("100 house renders without errors", not errors)

    with page.expect_download() as d:
        page.click("#saveimg")
    check("avatar PNG download", d.value.suggested_filename.endswith(".png"))

    page.reload()
    page.wait_for_timeout(300)
    check("identity survives reload", page.text_content("#name") == name)
    check("recent list populated", page.locator("#recent li").count() >= 1)

    page.evaluate("() => { const r = document.getElementById('kitrate'); r.value = 80; r.dispatchEvent(new Event('input', { bubbles: true })); }")
    check("kit slider updates its label", page.text_content("#kitratev") == "80%")
    page.click("#pwModeChars")
    check("random-character mode changes the password", len(page.locator("#account dd").nth(3).text_content()) == 20)

    page.click("#themebtn")
    try:   # the switch runs inside a view transition, so it can land a frame after the click
        page.wait_for_function("document.documentElement.getAttribute('data-theme') === 'light'", timeout=2000)
    except Exception:
        pass
    check("theme toggle sets data-theme", page.evaluate("document.documentElement.getAttribute('data-theme')") == "light")

    page.click("#reset")
    page.click("#confirm button[value=ok]")
    page.wait_for_timeout(500)
    check("reset produces a fresh identity", page.text_content("#name") != name)

    import re
    v_page = re.search(r'const VERSION = "([^"]+)"', open(os.path.join(ROOT, "index.html")).read()).group(1)
    v_sw = re.search(r'const VERSION = "([^"]+)"', open(os.path.join(ROOT, "sw.js")).read()).group(1)
    v_log = re.search(r"## ([0-9.]+)", open(os.path.join(ROOT, "CHANGELOG.md")).read()).group(1)
    check("version matches between page, service worker and changelog", v_page == v_sw == v_log)
    check("footer shows the version", page.text_content("#ver") == "v" + v_page)

    # Each check below starts from an empty browser profile.
    def fresh(c=None):
        pg = (c or browser.new_context(accept_downloads=True, viewport={"width": 900, "height": 1200})).new_page()
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(300)
        return pg

    def val(pg, label):   # the value shown on the row with this label
        return pg.evaluate("""l => { const r = [...document.querySelectorAll('.r')].find(r => r.querySelector('dt').textContent === l);
            return r ? [...r.querySelector('dd').childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('') : null; }""", label)

    def edit(pg, label, text):
        pg.locator(".r", has=pg.locator(f'dt:text-is("{label}")')).locator("dd").click()
        pg.keyboard.press("ControlOrMeta+A")
        if text:
            pg.keyboard.type(text)
        else:
            pg.keyboard.press("Delete")
        pg.keyboard.press("Enter")

    pg = fresh()
    pg.fill("#notes", "keep these notes")
    pw = val(pg, "Password")
    edit(pg, "Full name", "")
    pg.reload()
    pg.wait_for_timeout(300)
    check("identity with an empty name survives reload", val(pg, "Password") == pw and pg.input_value("#notes") == "keep these notes")
    pg.context.close()

    def clip(pg, button):   # what an export button puts on the clipboard
        pg.evaluate("navigator.clipboard.writeText = async t => { window.__clip = t; }")
        pg.click(button)
        pg.wait_for_function("window.__clip !== undefined")
        return pg.evaluate("window.__clip")

    pg = fresh()
    exported = json.loads(clip(pg, "#copyjson"))
    check("JSON export carries the full seed", exported["seed"] == pg.text_content("#seedview"))
    check("JSON export keeps site, notes and seed first", list(exported)[:3] == ["site", "notes", "seed"])
    pg.click("#new")
    pg.fill("#seedin", exported["seed"])
    pg.click("#loadseed")
    check("a seed from the JSON export loads", pg.text_content("#seedview") == exported["seed"])
    pg.context.close()

    pg = fresh()
    pg.fill("#seedin", "0123456789abcdef-fedcba9876543210")
    pg.click("#loadseed")
    avatar = pg.inner_html("#photo svg")
    pg.reload()
    pg.wait_for_timeout(300)
    check("a loaded seed survives reload", pg.text_content("#seedview") == "0123456789abcdef-fedcba9876543210")
    check("a loaded seed's avatar survives reload", pg.inner_html("#photo svg") == avatar)
    pg.context.close()

    stored = lambda pg, key, empty: json.loads(pg.evaluate(f"localStorage.getItem('{key}') || '{empty}'"))
    pg = fresh()
    tab = fresh(pg.context)
    made = [pg.text_content("#name")]
    for _ in range(3):
        pg.click("#new")
        made.append(pg.text_content("#name"))
    tab.click("#new")
    kept = {s["current"]["fullName"] for s in stored(pg, "identityHistory", "[]")}
    check("a second tab keeps the first tab's Recent identities", set(made[:-1]) <= kept)
    pg.wait_for_timeout(100)
    check("Recent identities in the other tab follow along", pg.locator("#recent li").count() == len(stored(pg, "identityHistory", "[]")))
    names = []
    for _ in range(3):
        pg.locator('[aria-label="New full name"]').dispatch_event("click")
        names.append(pg.text_content("#name"))
    tab.locator('[aria-label="New full name"]').dispatch_event("click")
    check("a second tab keeps the first tab's used names", set(names) <= set(stored(pg, "usedValues", "{}").get("name", [])))
    pg.locator("#recent button", has_text="Restore").first.click()
    check("Restore brings back a Recent identity", pg.text_content("#name") in made[:-1])
    pg.context.close()

    pg = fresh()
    made = [(pg.text_content("#name"), val(pg, "Username"), val(pg, "Email handle"))]
    for _ in range(5):
        pg.click("#new")
        made.append((pg.text_content("#name"), val(pg, "Username"), val(pg, "Email handle")))
    used = stored(pg, "usedValues", "{}")
    check("new identities go in the used-names memory",
          all(n in used.get("name", []) and u in used.get("username", []) and e in used.get("email", []) for n, u, e in made))
    pg.context.close()

    # The service worker needs http: serve the repo, answer the page with a 503 once, then go away.
    import threading, time
    from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
    failing = {"page": False}
    class Site(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=ROOT, **k)
        def log_message(self, *a):
            pass
        def do_GET(self):
            if failing["page"] and self.path.split("?")[0] in ("/", "/index.html"):
                self.send_response(503)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Service Unavailable</h1>")
                return
            super().do_GET()
    site = ThreadingHTTPServer(("127.0.0.1", 0), Site)
    threading.Thread(target=site.serve_forever, daemon=True).start()
    pg = browser.new_context().new_page()
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(f"http://127.0.0.1:{site.server_address[1]}/index.html")
    for _ in range(100):   # the page reloads itself once the worker takes over
        try:
            if pg.evaluate("navigator.serviceWorker.controller !== null"):
                break
        except Exception:
            pass
        time.sleep(0.1)
    pg.wait_for_timeout(500)
    failing["page"] = True
    pg.reload()
    pg.wait_for_timeout(500)
    site.shutdown()
    site.server_close()
    pg.reload()
    pg.wait_for_timeout(300)
    check("offline after a server error, the service worker still has the page", pg.locator("#name").count() == 1)
    pg.context.close()

    pg = fresh()
    pg.click("#addcustom")
    pg.keyboard.type("Code | PIN")
    pg.keyboard.press("Enter")
    pg.click("#addsec")
    pg.keyboard.type("Pet | first name?")
    pg.keyboard.press("Enter")
    rows = [l for l in clip(pg, "#copymd").splitlines() if l.startswith("|")]
    check("a | in a label or question stays inside its Markdown table cell",
          all(len(re.split(r"(?<!\\)\|", l)) == 4 for l in rows) and any("Code \\| PIN" in l for l in rows))
    pg.context.close()

    pg = fresh()
    pg.click("#pwModeChars")
    classes = {"#pwUpper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "#pwLower": "abcdefghijklmnopqrstuvwxyz", "#pwDigits": "0123456789", "#pwSymbols": "!?#$%&*-_+=@"}
    for box in classes:
        pg.click(box)
    ticked = "".join(chars for box, chars in classes.items() if pg.is_checked(box))
    pw = val(pg, "Password")
    check("the last character type can't be unticked, and the password uses only ticked types", ticked != "" and all(c in ticked for c in pw))
    pg.reload()
    pg.wait_for_timeout(300)
    check("the character type kept ticked is saved", any(pg.is_checked(box) for box in classes))
    pg.evaluate("""() => { const s = JSON.parse(localStorage.getItem('pwSettings'));
        Object.assign(s, { upper: false, lower: false, digits: false, symbols: false }); localStorage.setItem('pwSettings', JSON.stringify(s)); }""")
    pg.reload()
    pg.wait_for_timeout(300)
    check("settings saved with no character type show Lowercase ticked", pg.is_checked("#pwLower"))
    pg.context.close()

    pg = fresh()
    for _ in range(100):   # two bios in ten name the city
        if val(pg, "City") in val(pg, "Bio"):
            break
        pg.click("#new")
    old_city, seed = val(pg, "City"), pg.text_content("#seedview")
    while val(pg, "City") == old_city:
        pg.locator('[aria-label="New city"]').dispatch_event("click")
    check("rerolling City updates the bio", val(pg, "City") in val(pg, "Bio") and old_city not in val(pg, "Bio"))
    pg.click("#new")
    pg.fill("#seedin", seed)
    pg.click("#loadseed")
    check("the seed still gives the bio as first made", old_city in val(pg, "Bio"))
    pg.context.close()

    check("no page errors overall", not errors)
    browser.close()

if failures:
    print(f"\n{len(failures)} failure(s): " + ", ".join(failures))
    sys.exit(1)
print("\nall checks passed")
