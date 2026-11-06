"""Build the release's index.html: the page with its fonts and icon built in, so the one file works from disk.

The repo's index.html loads fonts/*.woff2 and icons/icon-192.png by relative path, so a copy downloaded on
its own falls back to system fonts and has no icon. This writes the same page with those files inlined as
data: URLs, and drops the manifest link, which only matters for installing from the website (a file opened
from disk can't be installed, and there is no manifest.json next to it). Nothing else changes; the repo's
index.html stays as it is. The IBM Plex licence goes in with the fonts, as a comment above them.

    python tools/build-standalone.py            # writes dist/index.html
    python tools/build-standalone.py --out DIR  # writes DIR/index.html

tests/test_download.py checks the result opened from file:// with the network blocked.
"""
import argparse
import base64
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def data_url(path, mime):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode("ascii"))


def build(src):
    out, fonts = re.subn(
        r'url\("fonts/([A-Za-z0-9-]+\.woff2)"\)',
        lambda m: 'url("%s")' % data_url(os.path.join(ROOT, "fonts", m.group(1)), "font/woff2"),
        src)
    if fonts != 6:
        sys.exit("expected 6 font URLs in index.html, found %d" % fonts)

    icon = '<link rel="apple-touch-icon" href="icons/icon-192.png">'
    if out.count(icon) != 1:
        sys.exit("expected one apple-touch-icon link in index.html")
    out = out.replace(icon, '<link rel="apple-touch-icon" href="%s">'
                      % data_url(os.path.join(ROOT, "icons", "icon-192.png"), "image/png"))

    manifest = '<link rel="manifest" href="manifest.json">\n'
    if out.count(manifest) != 1:
        sys.exit("expected one manifest link in index.html")
    out = out.replace(manifest, "")

    with open(os.path.join(ROOT, "fonts", "OFL.txt"), encoding="utf-8") as f:
        ofl = f.read().strip()
    if "*/" in ofl:
        sys.exit("fonts/OFL.txt can't go in a CSS comment")
    first = out.index("  @font-face")
    out = (out[:first] + "  /* The six @font-face rules below carry the IBM Plex fonts from fonts/ as data: URLs.\n\n"
           + ofl + "\n  */\n" + out[first:])

    left = re.findall(r'(?:src|href)="(?!data:|https?:|#|mailto:)[^"]+"|url\("(?!data:|#)[^"]+"\)', out)
    if left:
        sys.exit("index.html still loads files by relative path: %s" % ", ".join(sorted(set(left))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"), help="folder to write index.html into")
    args = ap.parse_args()
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        src = f.read()
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "index.html")
    with open(path, "w", encoding="utf-8", newline="\n") as f:   # LF, as committed, whatever the checkout did
        f.write(build(src))
    print("wrote %s (%d bytes)" % (path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
