---
name: identity-gen
description: Offline generator for throwaway signup identities, built on the RFS brand (Nightshift and Dayshift).
colors:
  nightshift-bg: "#0C0D10"
  nightshift-surface: "#13151A"
  nightshift-raised: "#1A1D24"
  nightshift-line: "#262A33"
  nightshift-line-strong: "#636872"
  nightshift-text: "#E8E6E1"
  nightshift-mute: "#8A8F99"
  nightshift-ember: "#FF6A3D"
  nightshift-ember-hover: "#FC7951"
  nightshift-ember-press: "#F98864"
  nightshift-on-ember: "#0C0D10"
  nightshift-amber: "#FFC247"
  nightshift-mint: "#3DDC97"
  nightshift-raspberry: "#F06292"
  nightshift-hover-wash: "rgba(232, 230, 225, 0.065)"
  nightshift-selection: "rgba(255, 106, 61, 0.3)"
  nightshift-scrim: "rgba(7, 8, 9, 0.72)"
  dayshift-bg: "#F6F5F2"
  dayshift-surface: "#FFFFFF"
  dayshift-raised: "#ECEAE4"
  dayshift-line: "#D6D3CB"
  dayshift-line-strong: "#89867F"
  dayshift-text: "#1A1B1E"
  dayshift-mute: "#666A73"
  dayshift-ember: "#C03B0A"
  dayshift-ember-hover: "#AC370C"
  dayshift-ember-press: "#98330F"
  dayshift-on-ember: "#FFFFFF"
  dayshift-amber: "#925F00"
  dayshift-mint: "#15794D"
  dayshift-raspberry: "#B0306A"
  dayshift-hover-wash: "rgba(26, 27, 30, 0.05)"
  dayshift-selection: "rgba(192, 59, 10, 0.2)"
  dayshift-scrim: "rgba(26, 27, 30, 0.45)"
typography:
  display:
    fontFamily: "IBM Plex Sans, Inter, system-ui, Segoe UI, sans-serif"
    fontSize: "40px"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "IBM Plex Sans, Inter, system-ui, Segoe UI, sans-serif"
    fontSize: "22px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  title:
    fontFamily: "IBM Plex Sans, Inter, system-ui, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "IBM Plex Sans, Inter, system-ui, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  body-small:
    fontFamily: "IBM Plex Sans, Inter, system-ui, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  control:
    fontFamily: "IBM Plex Sans, Inter, system-ui, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1
  value:
    fontFamily: "IBM Plex Mono, JetBrains Mono, ui-monospace, Consolas, monospace"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.4
  mono-small:
    fontFamily: "IBM Plex Mono, JetBrains Mono, ui-monospace, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.2
  wordmark:
    fontFamily: "IBM Plex Mono, JetBrains Mono, ui-monospace, Consolas, monospace"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.05em"
  label:
    fontFamily: "IBM Plex Mono, JetBrains Mono, ui-monospace, Consolas, monospace"
    fontSize: "11px"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.08em"
rounded:
  s: "4px"
  m: "6px"
  l: "8px"
spacing:
  s1: "4px"
  s2: "8px"
  s3: "12px"
  s4: "16px"
  s5: "24px"
  s6: "32px"
  s7: "48px"
  s8: "64px"
components:
  button-primary:
    backgroundColor: "{colors.nightshift-ember}"
    textColor: "{colors.nightshift-on-ember}"
    typography: "{typography.control}"
    rounded: "{rounded.m}"
    padding: "0 16px"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.nightshift-ember-hover}"
    textColor: "{colors.nightshift-on-ember}"
  button-primary-press:
    backgroundColor: "{colors.nightshift-ember-press}"
    textColor: "{colors.nightshift-on-ember}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.nightshift-mute}"
    typography: "{typography.control}"
    rounded: "{rounded.m}"
    padding: "0 16px"
    height: "40px"
  button-secondary-hover:
    textColor: "{colors.nightshift-text}"
  button-small:
    textColor: "{colors.nightshift-mute}"
    rounded: "{rounded.m}"
    padding: "0 12px"
    height: "32px"
  button-copied:
    textColor: "{colors.nightshift-mint}"
  button-danger:
    backgroundColor: "transparent"
    textColor: "{colors.nightshift-raspberry}"
    rounded: "{rounded.m}"
    padding: "0 16px"
    height: "40px"
  icon-button:
    textColor: "{colors.nightshift-mute}"
    rounded: "{rounded.s}"
    size: "32px"
  input-field:
    backgroundColor: "{colors.nightshift-raised}"
    textColor: "{colors.nightshift-text}"
    typography: "{typography.mono-small}"
    rounded: "{rounded.m}"
    padding: "0 12px"
    height: "40px"
  segmented-control:
    textColor: "{colors.nightshift-mute}"
    rounded: "{rounded.m}"
    padding: "3px"
  segmented-control-pressed:
    backgroundColor: "{colors.nightshift-raised}"
    textColor: "{colors.nightshift-text}"
    rounded: "{rounded.s}"
    height: "32px"
  seed-chip:
    backgroundColor: "{colors.nightshift-raised}"
    textColor: "{colors.nightshift-amber}"
    typography: "{typography.mono-small}"
    rounded: "{rounded.s}"
    padding: "9px 10px"
  fill-list:
    backgroundColor: "{colors.nightshift-surface}"
    rounded: "{rounded.l}"
  fill-row:
    textColor: "{colors.nightshift-text}"
    typography: "{typography.value}"
    padding: "6px 24px"
    height: "52px"
  fill-row-next:
    backgroundColor: "{colors.nightshift-raised}"
    textColor: "{colors.nightshift-text}"
  group-header:
    backgroundColor: "{colors.nightshift-bg}"
    textColor: "{colors.nightshift-mute}"
    typography: "{typography.label}"
    padding: "8px 24px"
    height: "48px"
  keycap:
    textColor: "{colors.nightshift-text}"
    rounded: "{rounded.s}"
    padding: "3px 5px"
  dialog:
    backgroundColor: "{colors.nightshift-surface}"
    textColor: "{colors.nightshift-text}"
    rounded: "{rounded.l}"
    padding: "24px"
    width: "28rem"
---

# Design System: identity-gen

## Overview

**Creative North Star: "The Fill Sheet"**

identity-gen is a working sheet that sits in a tab beside someone else's sign-up form. Its tokens come from the RFS brand guide, not from this project: the Nightshift and Dayshift palettes, Ember, Amber, Mint and Raspberry roles, IBM Plex Sans and Mono, the 4px spacing steps, focus and motion all come from https://github.com/Real-Fruit-Snacks/rfs-brand/blob/main/BRAND.md. The guide is binding (PRODUCT.md). What this project adds is how those tokens are arranged: a person column on one side and an ordered fill list on the other, with one row marked next.

The surface is dense, quiet and flat. Panels are made from one-pixel borders on near-black (or warm paper in Dayshift). Nearly everything is muted grey until it matters. The value you are about to paste is full-strength text in a large mono face, and the next row carries the page's only accent apart from the primary button. Copied rows step back to muted and say "ok · copied" in Mint. The page reads at a glance from the side of the eye while the user's attention is on the other tab.

Two themes ship. Nightshift (dark) is the default; Dayshift (light) follows `prefers-color-scheme: light` or an explicit choice. `data-theme="dark"` or `data-theme="light"` on `<html>` pins one, and the Theme control cycles Auto, Dayshift and Nightshift.

**Key Characteristics:**
- RFS brand tokens at their published values, in two themes swapped through custom properties.
- One Ember per screen: the New identity button, plus the next-row cursor (chevron and Enter keycap).
- Status always comes as a word plus a colour: "ok · copied" in Mint, "fail · select it" in Raspberry.
- Borders and tonal steps carry all structure. There are no shadows and no gradients.
- Sans for people and controls; mono for anything you might copy or type.

## Colors

These are the RFS brand palettes, defined twice (Nightshift and Dayshift) under the same role names. The page uses the role names; the theme decides the hex.

### Primary
- **Ember** (nightshift-ember / dayshift-ember): the action colour. The only filled button is New identity. Ember also marks the next fill row (the chevron cursor and the outlined Enter keycap), the 3px rule under the wordmark, link underline on hover, the text caret, the text-selection tint and every focus ring. Hover and press steps (ember-hover, ember-press) apply to the primary button only. Text on Ember uses on-ember.

### Secondary
- **Amber** (nightshift-amber / dayshift-amber): the seed. The seed string in its chip is the only Amber text on the page, which ties it visually to "this brings the person back".

### Tertiary
- **Mint** (nightshift-mint / dayshift-mint): success status. Copy buttons turn into "ok · copied", segments in the bar meter fill, and the meter reads "ok · all 21 copied" when it is complete.
- **Raspberry** (nightshift-raspberry / dayshift-raspberry): destructive and failed. It is used for Reset everything, the Reset button in the confirm dialog, and a copy that failed ("fail · select it").

### Neutral
- **Bg**: the page background, the sticky bar and the group-header bands inside the fill list.
- **Surface**: the fill-list panel, the rules and history panes, the dialog, and select menus.
- **Raised**: inputs, the seed chip, the portrait well, the pressed segment, the next-row cursor band, the lit rules pane and the update toast.
- **Line**: panel borders, row dividers and the bar's bottom border. Also used for empty meter segments.
- **Line-strong**: control outlines (buttons, inputs, selects, keycaps, segmented control), dialog and toast borders, resting link underline and the hover outline on editable values.
- **Text** and **Mute**: Text for names, values and the next row; Mute for labels, row numbers, secondary buttons at rest, hints and copied values.
- **Hover wash, Selection, Scrim**: translucent overlays for row hover, text selection and the dialog backdrop.

### Named Rules
**The One Ember Rule.** Ember fills one control per screen (New identity) and marks one row (the next one). Never use it for decoration, section headings, copied states or a second call to action.

**The Word-With-Colour Rule.** Mint and Raspberry never appear alone as status. Every state change writes a word: "ok · copied", "fail · select it", "ok · all N copied".

**The Theme-By-Role Rule.** Style with the role (`--rfs-primary`, `--rfs-line`), never a theme hex. Dayshift and Nightshift values exist only in the three theme blocks.

## Typography

**Body Font:** IBM Plex Sans (with Inter, system-ui, Segoe UI)
**Label/Mono Font:** IBM Plex Mono (with JetBrains Mono, ui-monospace, Consolas)

**Character:** The pairing splits the page into people and data. Sans carries the person's name, the field labels, prose and every control. Mono carries anything literal: values, seeds, keys, the wordmark and the small uppercase group labels.

### Hierarchy
- **Display** (700, 40px, 1.05): the identity's full name only. It steps down to 32px at 1199px and 26px at 639px, and is balanced and allowed to wrap anywhere.
- **Headline** (600, 22px, 1.2): section heads such as Fill order and Rules, and the dialog title.
- **Title** (600, 16px, 1.3): pane heads and Save it.
- **Body** (400, 16px, 1.6): base text and the tagline. Body-small (14px) is for field labels, hints and dialog copy; notes drop to 13px at line-height 1.55, capped at 62 to 64ch.
- **Control** (500, 14px): buttons and selects. Small buttons and segments use 13px. The primary button steps up to 600.
- **Value** (mono 400, 19px, 1.4): the fill-row value, which is what gets pasted. It is 17px at 639px. On the next row it goes to weight 500.
- **Mono-small** (mono 400, 13 to 14px): the seed chip, input text, range outputs and the handle under a recent identity.
- **Wordmark** (mono 600, 20px, -0.05em): "identity-gen" in the bar, 18px at 639px.
- **Label** (mono 500, 11px, 0.08em, uppercase): group names in the fill list (Account, Basics, Address), the Seed label and the version. Keycaps share the 11px mono size; row numbers are 12px mono with tabular figures.

### Named Rules
**The Copyable-Is-Mono Rule.** If a user could paste it, type it or press it, set it in Plex Mono. If it names a person, a field or an action, set it in Plex Sans.

**The Tabular Count Rule.** Counts and row numbers use `font-variant-numeric: tabular-nums` so the meter and the numbers don't jitter as they change.

## Layout

The layout is a full-width sticky bar over a two-column workspace, followed by a band of panes, all centred at a 1440px maximum with a 48px gutter. Spacing comes from the 4px steps s1 to s8. Component padding is mostly s3 to s5, and gaps between the major blocks are s6 to s7.

- **Bar** (72px, sticky, Bg with a bottom Line). A three-column grid: the wordmark on the left, the segmented copy meter and the site in the middle, and Theme, Undo and New identity on the right.
- **Walker.** On the left is a person column, `clamp(296px, 27vw, 400px)`, which sticks under the bar. It holds the square portrait, avatar tools, name, tagline, seed and seed restore. On the right the fill list takes the rest.
- **Fill rows.** A four-track grid: a 40px number, a 108 to 156px label, the value (1fr) and actions. Rows are 52px minimum with 24px side padding and a hairline divider. Group headers are 48px bands.
- **More band.** Rules sit in three panes (1fr 1fr 1.45fr). History and storage sit in two (2fr 1fr). Panes are divided by an inner Line.
- **≤1199px.** The gutter drops to 32px and the walker becomes one column. The person block becomes a 184px portrait beside name, seed, restore and tools. Panes stack, and the meter shrinks to 88px.
- **≤899px.** The bar wraps to two rows (wordmark and actions, then a full-width meter) at 116px.
- **≤639px.** The gutter is 16px and the bar is 104px. Actions spread across the bar grid, and keycap hints and the shortcut legend hide. The portrait drops to 112px. Rows restack to a number column with the label and actions above a full-width value. The Rules link and Enter keycap hide.
- **Touch** (`hover: none`). Row actions are always visible instead of appearing on hover.

## Elevation & Depth

The system is flat. Depth comes from three tonal steps (Bg, then Surface, then Raised) and one-pixel borders (Line for structure, Line-strong for controls). There are no drop shadows anywhere in the UI. The one `box-shadow` is a 1px inset ring of Line-strong on an editable value at hover, which is a hairline outline drawn without shifting layout, not elevation. The next fill row is "raised" literally: a Raised band slides behind it.

### Named Rules
**The Hairline Rule.** Separation is a 1px Line or a step in tone. Never add a drop shadow, glow or gradient to the UI. Gradients appear only inside generated avatar art, which is content.

## Shapes

The page uses gentle, small radii from the brand: 4px (s) for keycaps, icon buttons, the seed chip, editable value hover areas and pressed segments; 6px (m) for buttons, inputs, selects and the segmented control; 8px (l) for panels, the portrait, the dialog and the toast. Small one-offs are the 2px wordmark rule and 1px meter segments. Shapes are rectangles: no pills, no circles in the chrome. The select chevron is drawn from two borders rather than an icon glyph, and icons are 15 to 16px inline SVG strokes.

## Components

### Buttons
Outlined and quiet by default. The one filled button is the primary.
- **Shape:** gently rounded (rounded.m), 40px tall, 16px side padding, with a 15px icon and an optional keycap after the label.
- **Primary (New identity):** an Ember fill with on-ember text at weight 600. On hover it steps to ember-hover and lifts 1px; on press it goes to ember-press and settles.
- **Secondary (default):** transparent with a Line-strong border and Mute text. On hover the text becomes Text and the border becomes Mute. On press it moves down 1px. Disabled buttons use a Line border with dimmed keycaps.
- **Small:** 32px tall, 12px padding, 13px text. Used for Copy, Reroll, Add field, Reload and Later.
- **Copy (in a row):** a small button with a borderless rest state and a 100px minimum width. On the next row it gets a Mute border and Text label. Once copied it reads "ok · copied" in Mint; a failure reads "fail · select it" in Raspberry for 2.4s.
- **Danger:** Raspberry text and border, with the hover wash on hover.
- **Icon button:** a 32px square, borderless until hover, used for per-row reroll and remove.

### Inputs / Fields
- **Style:** a Raised fill, Line-strong border and rounded.m, 40px tall, with 14px mono text and a Mute placeholder. The textarea is at least 112px and resizes vertically. Selects use the same box in Sans (mono inside the rules panes) with a drawn chevron. Checkboxes, radios and ranges use `accent-color` Text, not Ember.
- **Focus:** the global Ember ring (see Focus below). There is no border colour shift.

### Segmented control
A 3px-padded outline (Line-strong, rounded.m) holding 32px segments. The pressed segment (`aria-pressed="true"`) gets a Raised fill and Text label. Used for Illustrated or Photo.

### Seed chip
The Seed label, followed by the seed in Amber mono-small on a Raised chip with a Line border (rounded.s), then a small Copy button. The string breaks anywhere.

### Fill list (signature)
The fill list is a Surface panel (rounded.l, Line border) that walks a sign-up form in order.
- **Rows:** a mono row number, a Sans Mute label and a 19px mono value with an action cluster on the right. Hover adds the hover wash. Row actions (reroll, Rules link) fade in on hover, on focus within, or on the next row.
- **Next row:** a single Raised cursor band slides behind it. An Ember chevron sits in the number column (the number hides), the label and value go to Text (value weight 500), and an Ember-outlined Enter keycap appears beside Copy.
- **Copied row:** the value goes to Mute and the button reads "ok · copied".
- **Group headers:** 48px Bg bands with the uppercase mono label and small Reroll and Add buttons, ruled top and bottom.
- **Keys:** Enter copies and advances, J and K move, R rerolls, E edits. The legend in the list head shows them as keycaps.

### Bar meter
A row of 2px-gapped segments (6px tall, 200px wide on desktop), one per field. Empty segments are Line and copied ones Mint. Next to it the count reads "**n** of 21 copied", turns to "ok · all 21 copied" when complete, and shows "for site" when a site is entered.

### Keycap
A Mono 500 11px key with a Line-strong border, rounded.s. Inside buttons the border drops to Line, and on the primary it is 45% of the label colour.

### Panes, dialog and toast
Panes are Surface panels split by inner Lines. A rules pane briefly lights to Raised when a row's Rules link sends you there. The confirm dialog is a Surface box at most 28rem wide with a Line-strong border over the Scrim, and its actions are right-aligned. The update toast is a Raised bar fixed at the bottom centre.

### Focus
Every focusable element gets a 2px solid Ember outline at a 3px offset (`:focus-visible`). It is the same in both themes.

### Motion
Motion follows the brand and runs only under `prefers-reduced-motion: no-preference`. It uses one easing (`cubic-bezier(.2,.7,.2,1)`) and three durations: 150ms for colour, border and opacity; 250ms for the cursor slide and meter fill; 600ms for the wordmark rule and theme sweep. The Ember rule draws in under the wordmark once on load. The next-row cursor slides between rows. Switching theme sweeps the new theme in as a circle growing out from the Theme button (a view transition). With reduced motion, all of it is instant.

## Do's and Don'ts

### Do:
- **Do** take every colour, type size, space step, radius and duration from the RFS brand guide's tokens, through the `--rfs-*` custom properties.
- **Do** keep Ember to the one primary action and the next-row cursor. Use it for focus rings everywhere (2px, 3px offset).
- **Do** write a status word next to every Mint or Raspberry state ("ok · copied", "fail · select it").
- **Do** set values, seeds, keys, the wordmark and uppercase group labels in Plex Mono, and names, labels and controls in Plex Sans.
- **Do** build structure from 1px Line borders and the Bg, Surface and Raised steps.
- **Do** check every new surface in both Nightshift and Dayshift, and at 1199, 899 and 639px.
- **Do** gate every animation behind `prefers-reduced-motion: no-preference`.

### Don't:
- **Don't** add a second filled or Ember button, or use Ember to mark copied rows or decorate headings.
- **Don't** use colour alone for status.
- **Don't** add drop shadows, glows or gradients to the interface.
- **Don't** hard-code a theme hex in a component. Use the role variable so Dayshift follows.
- **Don't** use Amber for anything but the seed, or Raspberry for anything but destructive and failed states.
- **Don't** step off the 4px spacing scale or the 4, 6 and 8px radii.
