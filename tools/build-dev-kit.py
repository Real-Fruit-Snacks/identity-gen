"""Build the offline dev kit: identity-gen-<version>-dev-windows-x64.zip.

It unzips to one folder, identity-gen-<version>-dev/: the repo at a commit (git archive, so no .git) plus
offline/, which holds what the checks would otherwise download:

    offline/python/       wheels for tests/requirements.txt and docs/art/requirements.txt, for CPython
                          (the version in .python-version) on Windows x64
    offline/files/ms-playwright/
                          Playwright's Chromium headless shell, the build p.chromium.launch() runs, laid out
                          the way PLAYWRIGHT_BROWSERS_PATH expects
    offline/licences/     the licence and notice files of all of the above
    offline/setup.ps1     sets the kit up with no network (from tools/dev-kit/setup.ps1)
    offline/README.md     what's in it, the toolchain, the steps (from tools/dev-kit/README.md)

Run it on Windows x64, from a Python with tests/requirements.txt installed (the Playwright it runs has to
be the pinned one, since it fetches that version's browser). It needs the network; the kit doesn't.

    python tools/build-dev-kit.py                     # HEAD into dist/
    python tools/build-dev-kit.py --ref v1.12.0 --out DIR
"""
import argparse
import importlib.metadata
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

import playwright as pw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "identity-gen"
REQUIREMENTS = ["tests/requirements.txt", "docs/art/requirements.txt"]
LICENCE_FILE = re.compile(r"(^|/)(licen[cs]e|notice|copying|thirdpartynotices)[^/]*$", re.I)


def run(cmd, **kw):
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def pinned(req_path, package):
    for line in read(req_path).splitlines():
        m = re.match(r"\s*%s\s*==\s*([^\s#;]+)" % re.escape(package), line, re.I)
        if m:
            return m.group(1)
    sys.exit("%s doesn't pin %s" % (req_path, package))


def tool_version(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None


def check_url(url):
    """The kit's README names an installer for each tool; make sure it's really there."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60) as r:
            if r.status == 200:
                return
    except OSError as e:
        sys.exit("can't reach %s (%s); the kit's README would point at nothing" % (url, e))
    sys.exit("%s answered %s" % (url, r.status))


def export(ref, dest):
    """The repo at ref, with the line endings as committed whatever this machine's git config says."""
    with tempfile.TemporaryDirectory() as tmp:
        archive = os.path.join(tmp, "src.zip")
        run(["git", "-C", ROOT, "-c", "core.autocrlf=false", "archive", "--format=zip", "-o", archive, ref])
        with zipfile.ZipFile(archive) as z:
            z.extractall(dest)


def wheel_licences(wheels, out):
    rows = []
    for whl in sorted(os.listdir(wheels)):
        if not whl.endswith(".whl"):
            continue
        dist, version = whl.split("-")[:2]
        target = os.path.join(out, "python", "%s-%s" % (dist, version))
        found = 0
        with zipfile.ZipFile(os.path.join(wheels, whl)) as z:
            for member in z.namelist():
                if not member.endswith("/") and LICENCE_FILE.search(member):
                    path = os.path.join(target, *member.split("/"))
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with z.open(member) as src, open(path, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    found += 1
        if not found:
            sys.exit("no licence file in %s; can't bundle it" % whl)
        rows.append((dist.replace("_", "-"), version, whl))
    return rows


def zip_tree(folder, zip_path):
    base = os.path.dirname(folder)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for here, dirs, files in os.walk(folder):
            dirs.sort()
            for name in sorted(files):
                path = os.path.join(here, name)
                z.write(path, os.path.relpath(path, base).replace(os.sep, "/"))


def main():
    ap = argparse.ArgumentParser(description="Build identity-gen's offline dev kit (Windows x64).")
    ap.add_argument("--ref", default="HEAD", help="commit or tag to package (default HEAD)")
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"), help="folder for the zip (default dist/)")
    ap.add_argument("--keep", action="store_true", help="keep the unzipped kit folder next to the zip")
    args = ap.parse_args()

    if sys.platform != "win32" or platform.machine().upper() not in ("AMD64", "X86_64"):
        sys.exit("build the kit on Windows x64: Playwright fetches the browser for the machine it runs on")

    os.makedirs(args.out, exist_ok=True)
    stage = tempfile.mkdtemp(prefix="dev-kit-", dir=args.out)
    try:
        src = os.path.join(stage, "src")
        export(args.ref, src)
        version = re.search(r'const VERSION = "([^"]+)"', read(os.path.join(src, "index.html"))).group(1)
        kit = os.path.join(stage, "%s-%s-dev" % (NAME, version))
        os.rename(src, kit)
        offline = os.path.join(kit, "offline")
        wheels = os.path.join(offline, "python")
        browsers = os.path.join(offline, "files", "ms-playwright")
        licences = os.path.join(offline, "licences")
        for d in (wheels, browsers, licences):
            os.makedirs(d)

        python = read(os.path.join(kit, ".python-version")).strip()
        if not re.fullmatch(r"3\.\d+\.\d+", python):
            sys.exit(".python-version should be an exact version like 3.12.10, not %r" % python)
        minor = "".join(python.split(".")[:2])
        playwright = pinned(os.path.join(kit, "tests", "requirements.txt"), "playwright")
        have = importlib.metadata.version("playwright")
        if have != playwright:
            sys.exit("this Python has playwright %s; tests/requirements.txt pins %s" % (have, playwright))

        # Wheels: CPython <minor> on win_amd64, whatever this machine is running.
        reqs = []
        for r in REQUIREMENTS:
            reqs += ["-r", os.path.join(kit, *r.split("/"))]
        run([sys.executable, "-m", "pip", "download", "--disable-pip-version-check", "--only-binary=:all:",
             "--platform", "win_amd64", "--implementation", "cp", "--python-version", python.rsplit(".", 1)[0],
             "--abi", "cp" + minor, "-d", wheels] + reqs)
        wheel_rows = wheel_licences(wheels, licences)

        # Browser: the headless shell only. Playwright also fetches FFmpeg, which only records video; the
        # checks don't, so it stays out. The full "Chrome for Testing" build isn't used headless either.
        env = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=browsers)
        run([sys.executable, "-m", "playwright", "install", "--only-shell", "chromium"], env=env)
        for d in os.listdir(browsers):
            if d.startswith("ffmpeg-") or d == ".links":
                shutil.rmtree(os.path.join(browsers, d))
        info = json.loads(read(os.path.join(os.path.dirname(pw.__file__), "driver", "package", "browsers.json")))
        shell = next(b for b in info["browsers"] if b["name"] == "chromium-headless-shell")
        winldd = next(b for b in info["browsers"] if b["name"] == "winldd")
        shell_dir = "chromium_headless_shell-%s" % shell["revision"]
        installed = sorted(os.listdir(browsers))
        if shell_dir not in installed:
            sys.exit("expected %s in %s, found %s" % (shell_dir, browsers, installed))
        exe_dir = os.path.join(browsers, shell_dir, "chrome-headless-shell-win64")
        for log in ("debug.log", "chrome_debug.log"):
            if os.path.exists(os.path.join(exe_dir, log)):
                os.remove(os.path.join(exe_dir, log))
        notice = os.path.join(licences, "chromium-headless-shell-%s" % shell["browserVersion"])
        os.makedirs(notice)
        shutil.copy(os.path.join(exe_dir, "LICENSE.headless_shell"), notice)
        with open(os.path.join(notice, "SOURCE.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("Chrome Headless Shell %s (Playwright chromium-headless-shell revision %s), built from Chromium.\n"
                    "LICENSE.headless_shell is the licence and third-party notice file that comes with it.\n"
                    "Source: https://chromium.googlesource.com/chromium/src/+/refs/tags/%s\n"
                    % (shell["browserVersion"], shell["revision"], shell["browserVersion"]))
        if "winldd-%s" % winldd["revision"] in installed:
            playwright_licences = os.path.join(licences, "python", "playwright-%s" % playwright)
            target = os.path.join(licences, "winldd-%s" % winldd["revision"])
            os.makedirs(target)
            for f in ("LICENSE", "NOTICE"):
                shutil.copy(os.path.join(playwright_licences, "playwright", "driver", "package", f), target)
            with open(os.path.join(target, "SOURCE.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("winldd (PrintDeps.exe) is part of Playwright, under Playwright's licence (LICENSE, NOTICE).\n"
                        "Source: https://github.com/microsoft/playwright/tree/v%s/browser_patches/winldd\n" % playwright)

        # setup.ps1 and README.md, from the same commit as the rest.
        shutil.copy(os.path.join(kit, "tools", "dev-kit", "setup.ps1"), offline)
        pwsh = tool_version(["pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"])
        python_url = "https://www.python.org/ftp/python/%s/python-%s-amd64.exe" % (python, python)
        pwsh_url = ("https://github.com/PowerShell/PowerShell/releases/download/v%s/PowerShell-%s-win-x64.msi" % (pwsh, pwsh)
                    if pwsh else "https://github.com/PowerShell/PowerShell/releases/latest")
        for url in (python_url, pwsh_url):
            check_url(url)
        values = {
            "version": version,
            "python": python,
            "python_minor": python.rsplit(".", 1)[0],
            "python_installer": "[%s](%s)" % (python_url.rsplit("/", 1)[1], python_url),
            "playwright": playwright,
            "chromium": shell["browserVersion"],
            "chromium_dir": shell_dir,
            "wheels": "\n  ".join("| %s | %s | `%s` |" % r for r in wheel_rows),
            "pwsh": "[%s](%s)" % (pwsh_url.rsplit("/", 1)[1], pwsh_url) if pwsh else "[PowerShell 7 releases](%s), x64 MSI" % pwsh_url,
        }
        readme = read(os.path.join(kit, "tools", "dev-kit", "README.md"))
        readme = re.sub(r"\A<!--.*?-->\n", "", readme, flags=re.S)
        readme = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], readme)
        with open(os.path.join(offline, "README.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(readme)

        zip_path = os.path.join(args.out, "%s-%s-dev-windows-x64.zip" % (NAME, version))
        if os.path.exists(zip_path):
            os.remove(zip_path)
        print("zipping %s" % zip_path, flush=True)
        zip_tree(kit, zip_path)
        if args.keep:
            dest = os.path.join(args.out, os.path.basename(kit))
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(kit, dest)
        print("wrote %s (%.1f MB)" % (zip_path, os.path.getsize(zip_path) / 1e6))
    finally:
        shutil.rmtree(stage, ignore_errors=True)


if __name__ == "__main__":
    main()
