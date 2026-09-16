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

    for style in ["initials", "pixel", "marble", "bauhaus", "sunset", "terrain", "rings", "bloom"]:
        page.select_option("#astyle", style)
        page.click("#newphoto")
        page.wait_for_timeout(80)
        check(f"offline style renders: {style}", page.locator("#photo svg").count() == 1)

    page.select_option("#astyle", "pixel")
    for _ in range(100):
        page.click("#newphoto")
    check("100 pixel renders without errors", not errors)

    with page.expect_download() as d:
        page.click("#saveimg")
    check("avatar PNG download", d.value.suggested_filename.endswith(".png"))

    page.reload()
    page.wait_for_timeout(300)
    check("identity survives reload", page.text_content("#name") == name)
    check("recent list populated", page.locator("#recent li").count() >= 1)

    page.click("#themebtn")
    check("theme toggle sets data-theme", page.evaluate("document.documentElement.getAttribute('data-theme')") == "light")

    page.click("#reset")
    page.click("#confirm button[value=ok]")
    page.wait_for_timeout(500)
    check("reset produces a fresh identity", page.text_content("#name") != name)

    check("no page errors overall", not errors)
    browser.close()

if failures:
    print(f"\n{len(failures)} failure(s): " + ", ".join(failures))
    sys.exit(1)
print("\nall checks passed")
