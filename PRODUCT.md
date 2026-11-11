# Product

## Platform

web

## Users

People signing up for a site they don't trust with their real details. The primary scene (confirmed): a desktop browser tab open beside a sign-up form, copying one field at a time into the form, then saving the result to a password manager. The maintainer uses it this way.

Open: whether the page serves mainly the maintainer or also strangers arriving from the README. Neither was confirmed as the priority.

## Product Purpose

One key press makes a complete stand-in identity: name, birthdate, gender, location, username, display name, email handle, passphrase, PIN, phone, address, occupation, company, language, favourite colour, hobby, a short bio and an avatar. No two of a person's accounts then share details. Success: the form gets filled fast and the identity can be brought back later from its seed or from the exported text.

## Positioning

- One seed brings back the whole identity, fields and avatar alike, on any copy of the page with the same settings. The README deck is drawn from six real seeds, and CI checks it.
- One HTML file with no server and no build step. It works offline once installed (PWA) or opened from disk (the release `index.html` has fonts and icon built in).
- Sends nothing by default. Only two opt-in features use the network, and the UI says so: the DiceBear Illustrated styles and Photo mode.
- Its own avatar generators (Pixel people with fourteen character kits, Duck with eight collections, House with fifteen building types, six abstract styles) are drawn in the page.

## Operating Context

- The page sits beside a sign-up form. Values are copied one by one, or the whole identity is exported as plain text, Markdown or JSON (clipboard or `.txt` / `.md`) with the site, notes and seed.
- The email field is a handle only (the part before `@`), meant for the user's own alias service or domain.
- Keyboard: N new identity, P new avatar, U undo (last ten).
- State lives in this browser's local storage only: settings, the current identity, the last ten identities (Recent and Undo) and the used-name memory.

## Capabilities and Constraints

- Every value can be edited in place, and every field, section or the whole identity can be rerolled. Custom fields and security questions (with generated answers) can be added.
- Passwords are passphrases (word count, separator, capitals, number) or random characters (length, classes, avoid look-alikes).
- Avatar styles: Initials, Pixel, Duck, House, Marble, Bauhaus, Sunset, Terrain, Rings, Bloom, three DiceBear styles (network), or Photo (network). Save as a 512px PNG or copy.
- Hard constraints (CONTRIBUTING.md): one file, no build step, no runtime dependencies; anything that needs the network stays opt-in and says so in the UI. The same seed gives the same identity and avatar; generation changes that alter a seed's output are called out in CHANGELOG.md. The version is set in three places (`index.html`, `sw.js`, `CHANGELOG.md`).
- The checks (`tests/test_page.py`, `tests/test_download.py`) and `docs/art/make-deck.py` drive the page through element IDs (`#new`, `#undo`, `#name`, `#tagline`, `#seedview`, `#seedin`, `#loadseed`, `#account dd`, `#addsec`, `#security dt`, `#addcustom`, `#custom dt`, `#dltext`, `#astyle`, `#newphoto`, `#photo svg`, `#saveimg`, `#recent li`, `#kitrate`, `#kitratev`, `#pwModeChars`, `#themebtn`, `#reset`, `#confirm`, `#ver`, `#update`). `#photo` must hold exactly one `svg`, the avatar.
- Limits stated in the README: addresses are a random number and street in a real city; phones are `(555) 01X-XXXX`; generated details are not for financial, government, medical or employment services.

## Brand Commitments

The RFS brand guide is binding: https://github.com/Real-Fruit-Snacks/rfs-brand/blob/main/BRAND.md (confirmed for this redesign). It sets the Nightshift (dark, default) and Dayshift (light) tokens, Ember as the one primary per screen, Amber, Mint and Raspberry roles, IBM Plex Sans and Mono with its type scale, the 4px space steps, focus, state and motion rules, no gradients, and the voice: plain, specific, dry, honest; sentence case; no emoji or exclamation marks; first person singular. The theme names Auto, Dayshift and Nightshift are part of the product.

## Evidence on Hand

- Real seeds and their output: the README deck (`docs/assets/deck-{dark,light}.svg`) and the worked example for seed `881ed162ae2eb154-c7a2ea20b2f14c94` (Wren Elliott).
- Repo cover and social art in `docs/assets/`.
- No user counts, testimonials or press exist. None may be invented.

## Product Principles

1. The identity is the product. Everything on the page serves making, checking and carrying one stand-in person.
2. Copying a value has to be fast and certain while the user is switching between this tab and a form.
3. Honest about the network and storage: say what leaves the browser and what stays.
4. Seeds are a promise. Nothing in the interface may change what a seed produces.
5. One file, offline, no build.

## Accessibility & Inclusion

WCAG AA contrast for every text colour in both themes, a visible Ember focus ring on every focusable element, and status carried by a word as well as a colour (BRAND.md §1). Full keyboard use, with the N/P/U shortcuts. Motion only under `prefers-reduced-motion: no-preference`.
