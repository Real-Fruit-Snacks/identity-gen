# Changelog

## Unreleased
- Fixed clearing Full name and refreshing the page replacing the whole identity, password, site and notes included, with a new one that never reached Recent identities.
- Fixed the JSON export's `seed` holding only the identity half, which Load rejected. It's the full seed now, in the same place.
- Fixed a refresh after Load bringing back the previous avatar seed and a different avatar.
- Fixed two open tabs erasing each other's Recent identities and used-names memory. Each reads the saved copy before changing it, and Recent identities and Undo follow changes made in another tab.
- New identities now go in the used-names memory and skip names, usernames and email handles this device has already given out; before, only a reroll of one of those fields did (12 repeated names in 1,500 new identities, now none). A seed still gives back the same identity.
- Fixed the service worker caching error responses, so one 503 or 404 for the page replaced the offline copy with the error page. Only successful responses are cached, and for an error the cached page is shown when there is one.
- Fixed a `|` in a custom field name or security question breaking its row of the Markdown table.
- Random-character passwords always keep one character type ticked: unticking the last one ticks it again and says why. Before, with none ticked, the password quietly came out all lowercase.
- Rerolling City, State, Location or Address now rewrites a bio that names the city.
- Fixed the reroll button on a row that isn't marked as next needing two clicks in Chromium and Firefox (the first only moved the mark).
- Fixed a ZIP reroll giving a Portland, ME identity Oregon's 972 prefix.
- No change to what a seed produces: every seed gives the same identity and avatar as in 1.13.0. The exports change only where noted above (the JSON `seed`, and `|` in Markdown labels).
- Browser checks cover each of these.

## 1.13.0
- New page layout built around filling in a sign-up form. The fields are listed in the order forms usually ask for them (account, basics, address, profile, extra fields, security questions), one row is marked as next, and <kbd>Enter</kbd> copies it and moves to the next one. Copied rows say "ok · copied" until their value changes, and the bar at the top counts them ("6 of 21 copied", with the site if you entered one).
- New keys: <kbd>J</kbd> and <kbd>K</kbd> move the marked row, <kbd>R</kbd> gives it a new value, <kbd>E</kbd> edits it. Tabbing to a row's Copy button and pressing Enter copies it and moves focus to the next row's button.
- The portrait, name and seed stay in view on wide screens. Username, password and avatar rules, Recent identities and Stored on this device are in one Rules section below the list; the Rules link on the username, email handle and password rows jumps to theirs.
- Basics and Address now have their own Reroll.
- Colours match the RFS brand values exactly (Dayshift Ember, control borders, Raspberry for errors).
- No change to what a seed produces or to the exports: every seed gives the same identity and avatar as in 1.12.0, and the text, Markdown and JSON keep their order.

## 1.12.0
- The `index.html` attached to each release now has the IBM Plex fonts and the icon built in, so the one file opened from disk looks like the website, with no network. Before, it fell back to system fonts and had no icon. The repo's `index.html` is unchanged.
- Each release also has `identity-gen-1.12.0-dev-windows-x64.zip`, a dev kit for working on the page with no network on Windows x64: the source, the Python packages and the Chromium the checks use, and `offline/setup.ps1`. It needs Python 3.12; see "Developing offline" in `CONTRIBUTING.md`.
- `SHA256SUMS.txt` on each release lists a SHA-256 for every file.
- No change to how the page works: every seed gives the same identity and avatar as in 1.11.1.

## 1.11.1
- No change to how the page works: every seed gives the same identity and avatar as in 1.11.0.
- New README, led by a deck of six identities the page drew from the seeds printed on them, with a worked example of restoring one.
- The README now spells out two limits: a seed's birth year counts back from today, so it comes out a year later after each 1 January; and the used-name memory only applies when you reroll a single name, username or email handle, not to New identity or a restored seed.

## 1.11.0
- RFS look: Nightshift (dark) and Dayshift (light) colours with the Ember accent, IBM Plex Sans and IBM Plex Mono (bundled, so it still works offline). The theme button names them: Auto, Dayshift, Nightshift. Your saved theme choice carries over.
- New app icon and favicon.

## 1.10.2
- House doors always end level with the bottom of the wall (beach huts on stilts, treehouses, lighthouses).

## 1.10.1
- House windows are always placed on a wall, clear of edges, roof and door; doors are centred with a window either side.

## 1.10.0
- Removed the white sticker outline from the Pixel, Duck and House styles; parts keep their own dark outlines.

## 1.9.1
- Pixel people: astronaut visors now show the face; long hair under hats no longer drapes as side locks; natural hair colours are weighted higher and always contrast with skin; aliens and robots never get glasses.
- Ducks: wizard beard; bolder mummy wrapping; cloud duck on a blue body; ice-cream cone the right way up; football face guard clears the beak; accessories no longer stack on hats or on themed heads.

## 1.9.0
- New House avatar style under a Places group: fifteen building types with materials, seasons, day and night, and garden details.

## 1.8.0
- New Duck avatar style: front-facing rubber ducks with 57 designs across eight themed collections, body colours, patterns, expressions and accessories.
- The character-kit slider also controls how often ducks belong to a collection.

## 1.7.0
- Version number shown in the footer.
- Installed copies show an "update available" notice with a Reload button when a new version is ready.

## 1.6.3
- Fixed the character-kit slider not responding.
- Tests now cover the kit slider and password mode switch.

## 1.6.2
- Ninja kit now wears a full hood instead of showing hair.
- Backdrops are chosen at random for every avatar rather than matched to kits.

## 1.6.1
- Fixed the sticker halo being drawn inside characters on the new backdrops.

## 1.6.0
- Ten designed pixel-art backdrops, some matched to character kits (stars for astronauts and wizards, sea for pirates, night for vampires).

## 1.5.1
- Removed the braids hair style.

## 1.5.0
- Removed the pigtails hair style.
- Recent identities are ordered by creation time.

## 1.4.0
- Installable as an app: web manifest, icons and a service worker for offline use.
- Recent identities panel with one-click restore.
- Passphrases are the default password style, with word count, separator, capitalisation and number options; random characters remain available.
- Theme toggle in the header: automatic, light or dark.
- Five new pixel character kits (pirate, ninja, chef, alien, cat) and a slider for how often kits appear.
- Browser test script (tests/test_page.py) and a GitHub Actions workflow that runs it on every push.

## 1.3.1
- Email is now a plain handle with no trailing @ in the display or exports.

## 1.3.0
- "Stored on this device" panel with a visible reset button and a themed confirmation dialog.
- Pixel avatars rebuilt at 48x48: egg-shaped heads, curved shading, big eyes, strand-cut hair, rounded shoulders and a sticker halo.
- Nine character kits: knight, wizard, robot, astronaut, elf, vampire, royal, detective, punk.
- Hats now replace hair: hair is clipped under any headwear and limited to styles that read clearly beneath a brim.
- Clothing colours are chosen to contrast with hair colours.
- Illustrated styles (DiceBear Lorelei, Notionists, Open Peeps) restored as an opt-in group that loads only when selected, with an offline fallback to Initials.
- README cover images for dark and light mode.

## 1.2.0
- Pixel style upgraded to 32x32 shaded busts with per-part outlines and sloped shoulders.
- Avatar stays square on narrow screens.

## 1.1.0
- New Pixel avatar style: an offline pixel-art person generator.

## 1.0.1
- Seed restore now reproduces an identity exactly regardless of the used-names memory.
- Fixed editing in Firefox versions without plaintext-only contenteditable support.
- Identities saved by earlier builds no longer break "+ Add" for custom fields and security questions.
- Initials avatar escapes and upper-cases its text.

## 1.0.0
- First release.
