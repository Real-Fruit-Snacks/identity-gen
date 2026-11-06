<!-- Template for the kit's offline/README.md: tools/build-dev-kit.py fills in the values in double braces. -->
# identity-gen {{version}} dev kit, Windows x64

Everything needed to change identity-gen and run its checks on a Windows PC with no network, except Python itself.

## What's in it

- The repo at v{{version}}, without `.git`.
- `offline/python/`: wheels for CPython {{python_minor}} on Windows x64, for `tests/requirements.txt` and `docs/art/requirements.txt` and what they depend on:

  | Package | Version | Wheel |
  |---|---|---|
  {{wheels}}

- `offline/files/ms-playwright/`: Chrome Headless Shell {{chromium}} (`{{chromium_dir}}`), the Chromium build Playwright {{playwright}} runs for `p.chromium.launch()`, and Playwright's winldd, laid out the way `PLAYWRIGHT_BROWSERS_PATH` expects.
- `offline/licences/`: the licence and notice files of every wheel and of the browser, with where to find the source.
- `offline/setup.ps1`: sets the kit up without the network.

Not included: Python; Firefox (`tests/test_download.py` also checks the release file in Firefox, so here run it with `--browsers chromium`); Playwright's full "Chrome for Testing" build and its FFmpeg, which only headed runs and video recording use; and Git, which nothing here needs.

## Toolchain

| Tool | Version | Installer that works offline |
|---|---|---|
| Python, 64-bit | {{python}}, the version CI uses (`.python-version`); any {{python_minor}}.x works | {{python_installer}} (the full installer, not the web one) |
| PowerShell, to run `setup.ps1` | Windows PowerShell 5.1, part of Windows 10 and 11; or PowerShell 7. CI runs it in both | {{pwsh}} |

## Steps

1. Unzip it with `tar -xf identity-gen-{{version}}-dev-windows-x64.zip` (built into Windows 10 and 11), or Extract All in Explorer.
2. `cd identity-gen-{{version}}-dev`
3. `powershell -ExecutionPolicy Bypass -File offline\setup.ps1`

   It finds Python {{python_minor}} (on PATH, or through the `py` launcher; pass `-Python C:\path\to\python.exe` otherwise) and says plainly if it's missing. It makes `.venv` here, installs the wheels from `offline\python` with `pip install --no-index --find-links offline\python`, leaves a `pip.ini` in `.venv` so later installs there only look in the kit too, and points Playwright in `.venv` at `offline\files\ms-playwright`. It starts the bundled Chromium once, then prints the commands to run next:

   ```powershell
   .venv\Scripts\python.exe tests\test_page.py
   .venv\Scripts\python.exe tools\build-standalone.py
   .venv\Scripts\python.exe tests\test_download.py --browsers chromium
   .venv\Scripts\python.exe docs\art\make-deck.py
   ```

   The first is the page checks. The next two build the release `index.html` into `dist\` and open it from disk with the network blocked. The last redraws the README deck from six seeds; `docs\assets\deck-*.svg` come out byte-for-byte the same (compare `Get-FileHash` before and after) unless a change altered what those seeds produce.

To make another kit from a changed copy, see `tools/build-dev-kit.py`; that one needs the network.
