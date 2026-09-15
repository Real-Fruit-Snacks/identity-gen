# identity-gen

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/cover-dark.svg">
  <img src="docs/cover-light.svg" alt="identity-gen: a fresh identity for every signup" width="100%">
</picture>

A single-page, offline generator for throwaway signup identities. One click
produces a name, username, email handle, password, birthdate, address,
occupation and an avatar, so no two of your accounts share the same details.

**Live:** https://real-fruit-snacks.github.io/identity-gen/

## Features

- Everything is generated in the browser. No server, no analytics, no fonts
  or scripts fetched unless you opt into an online photo source.
- Reroll any single field, a whole section, or the entire identity.
- Click any value to edit it. Add custom fields and security questions only
  when a site asks for them.
- Username and email-handle rules (max length, separators, digits) and
  password rules (length, character classes, look-alike avoidance).
- Seven offline abstract avatar styles, plus optional illustrated styles
  from DiceBear (CC0 only) and an optional photo source.
- Export as plain text, Markdown or JSON, or download `.txt` / `.md`,
  ready to paste into a password manager.
- Names, usernames and handles already generated on your device are
  remembered so new identities never repeat them.
- The current identity survives a refresh; Undo restores the last ten.
- Keyboard shortcuts: `N` new identity, `P` new photo, `U` undo.
- Dark and light modes, styled with the
  [Terminal Workbench](https://github.com/Real-Fruit-Snacks/terminal-workbench-suite)
  design tokens.

## Usage

Open `index.html` in any modern browser, or use the hosted copy above.
Nothing needs to be installed or built.

Email addresses are shown as `handle@` so you can pair them with your own
alias service or domain.

## Privacy

The page makes no network requests by default. Two optional features do:

- **Illustrated avatars** load the DiceBear library from jsDelivr.
- **Photo mode** fetches a face from the configured image source.

Both are off until you pick them, and the abstract avatars are used when
they are unavailable. All state (settings, current identity, undo history,
used-name memory) lives in your browser's local storage and can be cleared
with the reset button under Photo settings.

## Intended use

This is for ordinary sites that ask for more personal detail than they
need. Do not use generated details where you are required to give accurate
information, such as financial, government, medical or employment services.

## Credits

- Design tokens: [Terminal Workbench Suite](https://github.com/Real-Fruit-Snacks/terminal-workbench-suite) (MIT)
- Illustrated avatars: [DiceBear](https://www.dicebear.com) Lorelei, Notionists and Open Peeps styles (CC0)

## License

MIT. See [LICENSE](LICENSE).
