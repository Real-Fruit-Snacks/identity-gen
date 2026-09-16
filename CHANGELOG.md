# Changelog

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
