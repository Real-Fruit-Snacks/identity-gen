---
name: identity-gen
description: Offline generator for throwaway signup identities, built on RFS Cyclorama Dawn v2.1.0 (LX 263 Dark and LX 512 Light).
colors:
  dark-bg: "#050507"
  dark-surface: "#0C0C10"
  dark-raised: "#14141A"
  dark-line: "rgba(255, 255, 255, 0.14)"
  dark-line-strong: "#62646D"
  dark-text: "#F4F5F8"
  dark-mute: "#B3B5C0"
  dark-steel: "#1F547A"
  dark-steel-ink: "#74B8E8"
  dark-beacon: "#F06E2B"
  dark-beacon-fill: "#BD4811"
  dark-beacon-ink: "#FF9254"
  dark-amber: "#FFC247"
  dark-signal: "#3DDC97"
  dark-fault: "#FF5C6C"
  dark-fault-fill: "#C92438"
  dark-fault-fill-hover: "#E02E44"
  dark-on-fault: "#FFFFFF"
  dark-code-bg: "#08080B"
  light-bg: "#F5F7F9"
  light-surface: "#FFFFFF"
  light-raised: "#E3E8EE"
  light-line: "rgba(13, 16, 22, 0.16)"
  light-line-strong: "#6E7682"
  light-text: "#0D1016"
  light-mute: "#474D59"
  light-steel: "#1F547A"
  light-steel-ink: "#164669"
  light-beacon: "#F06E2B"
  light-beacon-ink: "#AD3D0A"
  light-amber: "#885800"
  light-signal: "#127247"
  light-fault: "#B91C2E"
  light-fault-fill: "#B91C2E"
  light-fault-fill-hover: "#991525"
  light-on-fault: "#FFFFFF"
  light-code-bg: "#EEF2F5"
typography:
  display:
    fontFamily: "Big Shoulders Stencil, Arial Narrow, sans-serif"
    fontSize: "46px"
    fontWeight: 700
    lineHeight: 0.96
    letterSpacing: "0.02em"
  headline:
    fontFamily: "Big Shoulders Stencil, Arial Narrow, sans-serif"
    fontSize: "28px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.03em"
  title:
    fontFamily: "Albert Sans, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Albert Sans, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  control:
    fontFamily: "Albert Sans, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1
  value:
    fontFamily: "Azeret Mono, ui-monospace, Cascadia Code, Consolas, monospace"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.4
  mono-small:
    fontFamily: "Azeret Mono, ui-monospace, Cascadia Code, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.2
  wordmark:
    fontFamily: "Big Shoulders Stencil, Arial Narrow, sans-serif"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.04em"
  label:
    fontFamily: "Azeret Mono, ui-monospace, Cascadia Code, Consolas, monospace"
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
---

# Design System: identity-gen

## Overview

**Creative North Star: "The Fill Sheet"**

`identity-gen` is a working sheet that sits in a tab beside a sign-up form. All tokens come from **RFS Cyclorama Dawn `v2.1.0`** (`Real-Fruit-Snacks/rfs-brand`): Matte Dark (`#050507`, `LX 263 DARK`) is the explicit default, and Alabaster Day (`#F5F7F9`, `LX 512 LIGHT`) is an opt-in toggle synchronized across RFS pages via `rfs-theme`.

The page uses a below-header `.rfs-shell` layout (`<header class="bar">` pinned above `<div class="rfs-scroll-region" id="page-scroll">`) so the scrollbar never enters the top header row. Panels rely on 1px borders and three flat tonal steps (`bg`, `surface`, `raised`), with subtle matte Glacial Steel and Beacon Orange atmospheric washes inside the scroll region.

## Colors

- **Glacial Steel (`#1F547A` / `#74B8E8` dark / `#164669` light):** structural accents, group headers, version metadata, and the left stop of the primary CTA and wordmark rule.
- **Maritime Beacon Orange (`#F06E2B` / `#BD4811` / `#FF9254` dark / `#AD3D0A` light):** primary action right stop (interpolated in Cartesian `in oklab`), focus rings, next-row cursor chevron, and active `Enter` keycap.
- **Amber (`#FFC247` dark / `#885800` light):** the deterministic seed chip.
- **Mint (`#3DDC97` dark / `#127247` light):** success states (`ok · copied`, filled copy-meter segments, `ok · all N copied`).
- **Signal Crimson (`#FF5C6C` / `#C92438` / `#E02E44` dark; `#B91C2E` / `#991525` light; `#FFFFFF` on-fault):** destructive actions (`Reset everything`, solid confirm `Reset` inside `<dialog id="confirm" class="rfs-dialog is-destructive">` with `autofocus` on **Cancel**) and copy failures (`fail · select it`).

## Typography

Six self-hosted variable `.woff2` files ship in `fonts/` (`Big Shoulders Stencil`, `Albert Sans`, `Azeret Mono`, latin + latin-ext) and are inlined by `tools/build-standalone.py` for offline single-file releases.

- **Big Shoulders Stencil (`700`):** wordmark (`IDENTITY-GEN`), person name, section titles (`FILL ORDER`, `RULES`), and dialog title.
- **Albert Sans (`400`–`600`):** field labels, controls, body copy, hints, and taglines.
- **Azeret Mono (`400`–`600`):** copyable fill-row values, seeds, keycaps, lux theme badge (`LX 263 DARK` / `LX 512 LIGHT`), row numbers (`tabular-nums`), and uppercase group headers.

## Motion & Accessibility

- Radial View Transition theme sweep (`520ms cubic-bezier(0.16, 1, 0.3, 1)`), cursor slide (`250ms`), and wordmark rule draw run only under `prefers-reduced-motion: no-preference`.
- Every text, border, control, and status color meets WCAG AA in both `LX 263 DARK` and `LX 512 LIGHT`, and every status state pairs color with explicit words (`ok · copied`, `fail · select it`).
