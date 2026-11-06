# Contributing

Bug reports and pull requests are welcome.

- Keep it one file with no build step and no runtime dependencies. Anything that needs the network stays opt-in and says so in the UI.
- Same seed, same identity and same avatar. Don't change generation in a way that alters what an existing seed produces unless the change says so in `CHANGELOG.md`. The README deck is drawn from six seeds, and the `art` check fails when they change; if that's intended, redraw it with `python docs/art/make-deck.py` (setup in the README) and commit the two SVGs.
- Bump the version in all three places (`const VERSION` in `index.html`, `sw.js`, the top of `CHANGELOG.md`) for any change that ships. To release, push the tag `vX.Y.Z` from `main`: `.github/workflows/release.yml` checks the changelog has that section, builds the release `index.html` and the dev kit, runs the checks below against both with the network cut off, and publishes them with `SHA256SUMS.txt`.
- Versions are pinned in one place each, and CI, the dev kit and the release all read them: Python in `.python-version`, Playwright in `tests/requirements.txt`, the art tools in `docs/art/requirements.txt` (keep its Playwright the same as the tests').
- Run the checks before opening a PR, and add one for new behaviour:

```sh
pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_page.py
```

`tests/test_download.py` checks the file a release attaches: build it with `python tools/build-standalone.py`, then run the test (it wants `python -m playwright install chromium firefox`, or pass `--browsers chromium`).

## Developing offline

Each release has `identity-gen-<version>-dev-windows-x64.zip`, for working on the page on Windows x64 with no network. It unzips to `identity-gen-<version>-dev/`: the repo at that tag (without `.git`) plus `offline/`, which holds the Python wheels for `tests/requirements.txt` and `docs/art/requirements.txt`, the Chromium headless shell Playwright runs, their licences, and `setup.ps1`. `offline/README.md` in the kit lists every version.

It doesn't include Python. Install it first:

| Tool | Version | Installer that works offline |
|---|---|---|
| Python, 64-bit | 3.12.10, as in `.python-version` (any 3.12.x works) | [python-3.12.10-amd64.exe](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe) |
| PowerShell | Windows PowerShell 5.1, part of Windows 10 and 11, or PowerShell 7 | [PowerShell 7 releases](https://github.com/PowerShell/PowerShell/releases), x64 MSI |

Then:

```powershell
tar -xf identity-gen-<version>-dev-windows-x64.zip
cd identity-gen-<version>-dev
powershell -ExecutionPolicy Bypass -File offline\setup.ps1
```

`setup.ps1` checks for Python 3.12 and says what's missing if it isn't there. It makes `.venv` in the kit, installs the wheels from `offline\python` without asking any package index, points Playwright in `.venv` at the bundled Chromium, starts it once, and prints the commands that run the page checks, the release-file check (Chromium only, since Firefox isn't in the kit) and the art check.

`tools/build-dev-kit.py` builds the kit, from `tools/dev-kit/setup.ps1` and `tools/dev-kit/README.md`. The release workflow builds it on Windows, unzips it on a clean runner, cuts off package registries and the internet, and runs `setup.ps1` (in Windows PowerShell 5.1 and in PowerShell 7) and every check from the unzipped kit before it publishes anything.
