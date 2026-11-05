"""Draw the README's animated deck: docs/assets/deck-dark.svg and deck-light.svg.

Six identities, made by the real page (index.html) from the seeds printed on them. The script
opens the page in headless Chromium, loads each seed with the page's own "Paste a seed to restore"
box, downloads the page's own .txt export and copies the avatar SVG the page drew. Nothing on the
cards is typed in by hand. The SVGs then show the six as a deck that steps one card left every
2.8 s, the way "New identity" (N) brings in the next person.

Two things are pinned so the output only changes when the page does:
- The date. The page counts a birth year back from today, so the clock is frozen at DATE.
- The settings. A fresh browser profile gets the page's defaults (passphrases, 45 % character kits).

Text is converted to paths from the fonts in docs/art/fonts, because an SVG shown through <img>
can't load fonts. Pixel, Duck and House avatars are the page's own 48 x 48 grid of rects, merged
into one path per colour (same pixels, a quarter of the bytes). Run from the repo root:

    python -m pip install -r docs/art/requirements.txt
    python -m playwright install chromium
    python docs/art/make-deck.py

CI runs it and fails if the committed SVGs differ, so a change that alters what a seed produces
shows up there (see CONTRIBUTING.md).
"""
import os
import re
import sys
from collections import OrderedDict

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(ROOT, "docs", "assets")
PAGE = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/").lstrip("/")
DATE = "2026-11-05T12:00:00Z"

# (avatar style, seed). The deck, left to right; the third is in front in the still frame.
# Picked by browsing a few dozen seeds for avatars that show the range.
CARDS = [
    ("bauhaus", "e8e25d940ed90475-0cb1e29c658cda14"),
    ("house", "1600a35a099950d8-a170b33839263059"),
    ("pixel", "881ed162ae2eb154-c7a2ea20b2f14c94"),
    ("duck", "8f6d05584ef8aa38-18f135d25f557203"),
    ("pixel", "b2715945795e8229-4f426dcbb394fb36"),
    ("house", "12bd4acefaecbd38-9531985d5d9dc9f8"),
]
STYLE_NAMES = {"pixel": "PIXEL", "duck": "DUCK", "house": "HOUSE", "bauhaus": "BAUHAUS", "sunset": "SUNSET",
               "marble": "MARBLE", "terrain": "TERRAIN", "rings": "RINGS", "bloom": "BLOOM", "initials": "INITIALS"}

# RFS Nightshift and Dayshift
THEMES = {
    "dark": dict(plate="#0C0D10", card="#13151A", raised="#1A1D24", line="#262A33", strong="#636872", ink="#E8E6E1",
                 mute="#8A8F99", ember="#FF6A3D", on_ember="#0C0D10", amber="#FFC247", dim=(0.42, 0.68), shadow=0.55, glow=0.16),
    "light": dict(plate="#F6F5F2", card="#FFFFFF", raised="#ECEAE4", line="#D6D3CB", strong="#89867F", ink="#1A1B1E",
                  mute="#666A73", ember="#C03B0A", on_ember="#FFFFFF", amber="#925F00", dim=(0.40, 0.66), shadow=0.16, glow=0.10),
}

W, H = 1000, 600
CW, CH = 296, 540            # card, drawn around its own centre
CY = H / 2
# slot -> (centre x, scale). 0 is the front card; +-3 sit just off the deck, invisible.
SLOTS = {0: (500, 1.0), 1: (718, 0.84), -1: (282, 0.84), 2: (874, 0.70), -2: (126, 0.70), 3: (1000, 0.60), -3: (0, 0.60)}
STEP, MOVE = 2.8, 0.7         # seconds a card holds the front, and how long a step takes
CYCLE = STEP * len(CARDS)

NEXT_M, NEXT_X = "atkinson-hyperlegible-next-latin-500-normal.woff2", "atkinson-hyperlegible-next-latin-800-normal.woff2"
MONO, MONO_M, MONO_S = ("atkinson-hyperlegible-mono-latin-400-normal.woff2", "atkinson-hyperlegible-mono-latin-500-normal.woff2",
                        "atkinson-hyperlegible-mono-latin-600-normal.woff2")


# ---------- the page ----------

def capture():
    """Load every seed in the real page; return the export fields and avatar SVG for each card."""
    out = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(accept_downloads=True)
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.clock.set_fixed_time(DATE)
        page.goto(PAGE)
        page.wait_for_selector("#name:not(:empty)")
        for style, seed in CARDS:
            page.select_option("#astyle", style)
            page.fill("#seedin", seed)
            page.click("#loadseed")
            if page.text_content("#seedview") != seed:
                sys.exit(f"the page did not load seed {seed}")
            with page.expect_download() as d:
                page.click("#dltext")
            with open(d.value.path(), encoding="utf-8") as f:
                text = f.read()
            fields = {}
            for line in text.splitlines():
                m = re.match(r"^  ([^:]+): (.*)$", line)
                if m:
                    fields[m.group(1)] = m.group(2)
            fields["Name"] = text.splitlines()[0]
            fields["Tagline"] = page.text_content("#tagline")
            svg = page.eval_on_selector("#photo svg", "e => e.outerHTML")
            out.append(dict(style=style, seed=seed, fields=fields, svg=svg, text=text))
        browser.close()
    if errors:
        sys.exit("page errors: " + "; ".join(errors))
    return out


# ---------- text as paths ----------

_fonts = {}
_glyphs = OrderedDict()   # (font, glyph name) -> (id, path in font units); drawn once in <defs>, reused by <use>


def font(name):
    if name not in _fonts:
        _fonts[name] = TTFont(os.path.join(FONTS, name))
    return _fonts[name]


def advance(s, size, fname, ls=0.0):
    f = font(fname)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    return sum(gs[cmap[ord(ch)]].width for ch in s) * size / f["head"].unitsPerEm + ls * size * (len(s) - 1)


def fit(s, size, fname, width, ls=0.0):
    """The largest size up to `size` at which s fits in width."""
    w = advance(s, size, fname, ls)
    return size if w <= width else size * width / w


def text(s, x, y, size, fname, fill, ls=0.0, anchor="start"):
    """Path for s with its baseline at y. ls is letter spacing in em."""
    f = font(fname)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    k = size / upm
    names = []
    for ch in s:
        if ord(ch) not in cmap:
            sys.exit(f"{fname} has no glyph for {ch!r}")
        names.append(cmap[ord(ch)])
    width = advance(s, size, fname, ls)
    x0 = {"start": x, "middle": x - width / 2, "end": x - width}[anchor]
    uses, pen_x = [], 0.0
    for n in names:
        key = (fname, n)
        if key not in _glyphs:
            pen = SVGPathPen(gs, ntos=lambda v: "%g" % round(v))
            gs[n].draw(pen)
            _glyphs[key] = (f"t{len(_glyphs)}", pen.getCommands())
        gid, d = _glyphs[key]
        if d:
            uses.append(f'<use href="#{gid}" x="{round(pen_x)}"/>' if round(pen_x) else f'<use href="#{gid}"/>')
        pen_x += gs[n].width + ls * upm
    return f'<g fill="{fill}" transform="matrix({k:.5f} 0 0 {-k:.5f} {x0:.2f} {y:.2f})">{"".join(uses)}</g>'


def glyph_defs():
    return "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in _glyphs.values() if d)


# ---------- avatars ----------

def avatar(svg, prefix):
    """The page's avatar as (viewBox size, SVG content). Pixel-grid styles become one path per colour."""
    box = int(re.search(r'viewBox="0 0 (\d+) \d+"', svg).group(1))
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    grid = re.fullmatch(r'<g shape-rendering="crispEdges">(.*)</g>', inner.strip(), re.S)
    if grid:
        runs = re.findall(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="([^"]+)"></rect>', grid.group(1))
        if len(runs) != grid.group(1).count("<rect"):
            sys.exit("unexpected markup in a pixel avatar")
        by = OrderedDict()
        for x, y, w, h, fill in runs:
            by.setdefault(fill, []).append(f"M{x} {y}h{w}v{h}h-{w}z")
        return box, '<g shape-rendering="crispEdges">' + "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in by.items()) + "</g>"
    # Vector styles: keep as drawn, with ids made unique so several avatars can share one file.
    ids = re.findall(r'id="([^"]+)"', inner)
    for i in ids:
        inner = inner.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})").replace(f'href="#{i}"', f'href="#{prefix}{i}"')
    inner = re.sub(r">\s+<", "><", inner)
    return box, inner


# ---------- the card ----------

def card(i, c, t):
    """One card drawn around (0, 0)."""
    f = c["fields"]
    x0, x1 = -CW / 2, CW / 2
    y0 = -CH / 2
    pad = 16
    left, inner_w = x0 + pad, CW - 2 * pad
    o = [f'<g id="card{i}">']
    o.append(f'<rect x="{x0 + 3}" y="{y0 + 10}" width="{CW - 6}" height="{CH - 6}" rx="16" fill="#000" opacity="{t["shadow"]}" filter="url(#soft)"/>')
    o.append(f'<rect x="{x0 + 0.5}" y="{y0 + 0.5}" width="{CW - 1}" height="{CH - 1}" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>')
    # header
    o.append(text("STAND-IN", left, y0 + 21, 10.5, MONO_S, t["mute"], ls=0.16))
    o.append(text(STYLE_NAMES[c["style"]], x1 - pad, y0 + 21, 10.5, MONO_S, t["mute"], ls=0.16, anchor="end"))
    # avatar
    ay, size = y0 + 30, inner_w
    o.append(f'<g clip-path="url(#avclip)"><rect x="{left}" y="{ay}" width="{size}" height="{size}" fill="{t["raised"]}"/>'
             f'<use href="#av{i}" transform="translate({left} {ay}) scale({size / c["box"]:.5f})"/></g>')
    o.append(f'<rect x="{left + 0.5}" y="{ay + 0.5}" width="{size - 1}" height="{size - 1}" rx="10" fill="none" stroke="#000" stroke-opacity=".12"/>')
    y = ay + size
    # name and tagline
    o.append(text(f["Name"], left, y + 36, fit(f["Name"], 28, NEXT_X, inner_w, -0.01), NEXT_X, t["ink"], ls=-0.01))
    o.append(text(f["Tagline"], left, y + 59, fit(f["Tagline"], 16, NEXT_M, inner_w), NEXT_M, t["amber"]))
    o.append(f'<rect x="{left}" y="{y + 74}" width="{inner_w}" height="1" fill="{t["line"]}"/>')

    def field(label, value, x, y, width):
        return (text(label, x, y, 9.5, MONO_S, t["mute"], ls=0.14) +
                text(value, x, y + 18, fit(value, 14, MONO, width), MONO, t["ink"]))
    born = f["Birthdate"].split(" (")[0]
    o.append(field("USERNAME", f["Username"], left, y + 92, inner_w))
    o.append(field("PASSWORD", f["Password"], left, y + 132, inner_w))
    o.append(field("BIRTHDATE", born, left, y + 172, 120))
    o.append(field("PHONE", f["Phone"], left + 134, y + 172, inner_w - 134))
    # seed
    o.append(f'<rect x="{left}" y="{y + 206}" width="{inner_w}" height="1" fill="{t["line"]}"/>')
    o.append(text(c["seed"], 0, y + 230, fit(c["seed"], 11.5, MONO_M, inner_w), MONO_M, t["ember"], anchor="middle"))
    o.append("</g>")
    return "".join(o)


# ---------- motion ----------

def pct(s):
    return f"{s / CYCLE * 100:.3f}%"


def slot_at(r, k):
    """Slot of the card at ring position r after k steps: -3 (just left the deck) to +2."""
    n = len(CARDS)
    return (r - 2 - k + 3) % n - 3


def depth(slot):
    return min(abs(slot), 2)


def build(theme, cards):
    t = THEMES[theme]
    _glyphs.clear()
    n = len(CARDS)
    bodies = [card(i, c, t) for i, c in enumerate(cards)]
    corner_l = text("IDENTITY-GEN", 32, H - 26, 11, MONO_S, t["mute"], ls=0.18)
    corner_r = text("NEW IDENTITY", W - 32 - 34 - 12, H - 26, 11, MONO_S, t["mute"], ls=0.18, anchor="end")
    keycap = text("N", W - 32 - 17, H - 25, 15, MONO_S, t["on_ember"], anchor="middle")

    def state(slot):
        x, s = SLOTS[slot]
        return f"transform:translate({x}px,{CY}px) scale({s});opacity:{0 if abs(slot) == 3 else 1}"

    def dim(slot):
        return 0 if slot == 0 else t["dim"][0] if abs(slot) == 1 else t["dim"][1]

    css, base = [], []
    for i in range(n):
        pos, dimk, lay = [], [], {0: [], 1: [], 2: []}
        for k in range(n):
            a, b = slot_at(i, k), slot_at(i, k + 1)
            t0, t1, t2 = k * STEP, k * STEP + STEP - MOVE, (k + 1) * STEP
            src = 3 if a == -3 else a                 # a card that left on the left comes back in from the right
            pos += [f"{pct(t0)}{{{state(a)}}}", f"{pct(t1 - 0.001)}{{{state(a)}}}", f"{pct(t1)}{{{state(src)}}}"]
            dimk += [f"{pct(t0)}{{opacity:{dim(a)}}}", f"{pct(t1)}{{opacity:{dim(src)}}}"]
            # which layer the card paints in: its depth, switching halfway through a move
            mid = t1 + MOVE / 2
            for L in lay:
                lay[L] += [(t0, depth(a) == L), (mid, depth(b) == L)]
        a0 = slot_at(i, 0)
        pos.append(f"100%{{{state(a0)}}}")
        dimk.append(f"100%{{opacity:{dim(a0)}}}")
        css.append(f"@keyframes p{i}{{{''.join(pos)}}}")
        css.append(f"@keyframes d{i}{{{''.join(dimk)}}}")
        for L, pts in lay.items():
            body = "".join(f"{pct(s)}{{opacity:{int(v)}}}" for s, v in pts)
            css.append(f"@keyframes l{i}{L}{{{body}100%{{opacity:{int(depth(a0) == L)}}}}}")
        base.append(f".p{i}{{{state(a0)}}}.d{i}{{opacity:{dim(a0)}}}")
        base.append("".join(f".l{i}{L}{{opacity:{int(depth(a0) == L)}}}" for L in lay))
    ease = "cubic-bezier(.65,0,.3,1)"
    rules = "".join(f".p{i}{{animation:p{i} {CYCLE}s {ease} infinite}}.d{i}{{animation:d{i} {CYCLE}s {ease} infinite}}"
                    + "".join(f".l{i}{L}{{animation:l{i}{L} {CYCLE}s step-end infinite}}" for L in range(3)) for i in range(n))
    # the N key goes down as each step starts
    press = []
    for k in range(n):
        t1 = k * STEP + STEP - MOVE
        press += [f"{pct(t1 - 0.12)}{{transform:translateY(0)}}", f"{pct(t1 - 0.04)}{{transform:translateY(2.5px)}}", f"{pct(t1 + 0.14)}{{transform:translateY(0)}}"]
    css.append("@keyframes key{0%{transform:translateY(0)}" + "".join(press) + "100%{transform:translateY(0)}}")
    rules += f".key{{animation:key {CYCLE}s linear infinite}}"

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">']
    o.append(f"<style>{''.join(base)}@media (prefers-reduced-motion:no-preference){{{''.join(css)}{rules}}}</style>")
    defs = ['<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>',
            f'<radialGradient id="glow"><stop offset="0" stop-color="{t["ember"]}" stop-opacity="{t["glow"]}"/>'
            f'<stop offset="1" stop-color="{t["ember"]}" stop-opacity="0"/></radialGradient>']
    inner_w = CW - 32
    defs.append(f'<clipPath id="avclip"><rect x="{-CW / 2 + 16}" y="{-CH / 2 + 30}" width="{inner_w}" height="{inner_w}" rx="10"/></clipPath>')
    for i, c in enumerate(cards):
        defs.append(f'<g id="av{i}">{c["content"]}</g>')
    defs += bodies
    o.append(f"<defs>{glyph_defs()}{''.join(defs)}</defs>")
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="22" fill="{t["plate"]}" stroke="{t["line"]}"/>')
    o.append(f'<ellipse cx="500" cy="{H - 40}" rx="460" ry="300" fill="url(#glow)"/>')
    o.append(corner_l + corner_r)
    kx, ky = W - 32 - 34, H - 26 - 23
    o.append(f'<g class="key"><rect x="{kx}" y="{ky + 3}" width="34" height="32" rx="7" fill="{t["strong"]}" opacity=".5"/>'
             f'<rect x="{kx}" y="{ky}" width="34" height="32" rx="7" fill="{t["ember"]}"/>{keycap}</g>')
    for L in (2, 1, 0):
        for i in range(n):
            o.append(f'<g class="p{i}"><g class="l{i}{L}"><use href="#card{i}"/>'
                     f'<rect class="d{i}" x="{-CW / 2}" y="{-CH / 2}" width="{CW}" height="{CH}" rx="16" fill="{t["plate"]}"/></g></g>')
    o.append("</svg>")
    return "".join(o)


def main():
    cards = capture()
    for i, c in enumerate(cards):
        c["box"], c["content"] = avatar(c["svg"], f"a{i}")
    os.makedirs(OUT, exist_ok=True)
    for theme in THEMES:
        svg = build(theme, cards)
        path = os.path.join(OUT, f"deck-{theme}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg + "\n")
        print(f"{os.path.relpath(path, ROOT)}: {len(svg.encode()) / 1024:.0f} KB")
    if "--print" in sys.argv:
        for c in cards:
            print(f"\n--- {c['style']} {c['seed']}\n{c['text']}")


if __name__ == "__main__":
    main()
