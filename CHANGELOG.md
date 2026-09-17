# Changelog

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
