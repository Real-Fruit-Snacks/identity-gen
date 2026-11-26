# AGENTS.md — Repository Guardrails (identity-gen)

This repository is part of **Real-Fruit-Snacks** (**RFS**) and follows the **Cyclorama Dawn `v2.1.0` — Steel & Beacon Orange + Signal Crimson Fault** brand system (`Real-Fruit-Snacks/rfs-brand`).

## Core Commitments
1. **Single-file offline web app:** Keep `index.html` self-contained with inline CSS/JS, no build step, and zero runtime third-party dependencies. Network features (DiceBear Illustrated styles, Photo URLs) remain opt-in and labeled in the UI.
2. **Deterministic seeds:** Never change identity or avatar PRNG output for an existing seed unless explicitly called out in `CHANGELOG.md` and reflected in regenerated `docs/assets/deck-{dark,light}.svg`.
3. **Version parity:** Keep `const VERSION` in `index.html`, `const VERSION` in `sw.js`, and the top version heading in `CHANGELOG.md` identical.
4. **Plain, specific, honest voice:** No emoji, no hype copy, no exclamation marks in headings or descriptions.

## Brand & UI Rules (`rfs-brand` v2.1.0)
- **Theme & Motion:** Matte Dark (`#050507`, `LX 263 DARK`) is the explicit default (`<meta name="color-scheme" content="dark">`); Alabaster Day (`#F5F7F9`, `LX 512 LIGHT`) is an opt-in toggle synchronized via `rfs-theme` (`localStorage`) with a radial View Transition under `prefers-reduced-motion: no-preference`.
- **Palette:** Glacial Steel (`#1F547A` / `#74B8E8` / `#164669`), Maritime Beacon Orange (`#F06E2B` / `#BD4811` / `#FF9254` / `#AD3D0A`), Signal Crimson Fault (`#FF5C6C` / `#C92438` / `#E02E44` dark, `#B91C2E` / `#991525` light, `#FFFFFF` on-fault), Amber (`#FFC247` / `#885800`), Mint (`#3DDC97` / `#127247`). Always interpolate gradients in Cartesian `in oklab` (never `in oklch`).
- **Typography:** Six self-hosted variable `.woff2` files in `fonts/` (`Big Shoulders Stencil`, `Albert Sans`, `Azeret Mono`, latin + latin-ext) plus `fonts/OFL.txt` so `tools/build-standalone.py` inlines all 6 `@font-face` rules into the release `index.html`.
- **Scrollbars:** Use `.rfs-shell` (`body`) + pinned `<header class="bar">` + `<div class="rfs-scroll-region" id="page-scroll">` so the scrollbar never extends into the top header row. Never animate `scrollbar-color`.
- **Destructive Dialogs:** Never use `window.alert()`, `window.confirm()`, or `window.prompt()`. Use `<dialog id="confirm" class="rfs-dialog is-destructive">` with `autofocus` on **Cancel** and solid Signal Crimson styling on **Reset**.
- **README & Docs (`BRAND.md` §14):** Keep `README.md` ultra-minimal (40–60 lines); put seed examples, feature tables, settings, known issues, and development steps in `docs/USAGE.md` (never GitHub Wiki).
- **Verification:** Run `python tools/build-standalone.py`, `python docs/art/make-deck.py`, `python tests/test_page.py`, and `python tests/test_download.py dist/index.html` before pushing.
