# Contributing

Bug reports and pull requests are welcome.

- Keep it one file with no build step and no runtime dependencies. Anything that needs the network stays opt-in and says so in the UI.
- Same seed, same identity and same avatar. Don't change generation in a way that alters what an existing seed produces unless the change says so in `CHANGELOG.md`. The README deck is drawn from six seeds, and the `art` check fails when they change; if that's intended, redraw it with `python docs/art/make-deck.py` (setup in the README) and commit the two SVGs.
- Bump the version in all three places (`const VERSION` in `index.html`, `sw.js`, the top of `CHANGELOG.md`) for any change that ships.
- Run the checks before opening a PR, and add one for new behaviour:

```sh
pip install playwright
playwright install chromium
python tests/test_page.py
```
