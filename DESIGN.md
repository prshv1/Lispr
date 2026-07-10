# Design System — Lispr Flow

## Product Context

- **What this is:** A lightweight Linux desktop dictation app inspired by the flow of speaking rather than typing.
- **Who it is for:** Linux users who want dependable voice-to-text without a distracting desktop app.
- **Space/industry:** Desktop productivity and voice transcription.
- **Project type:** Native Ubuntu-first desktop application, built with Python and PySide6.
- **Memorable thing:** Serious software that gets out of the user's way.

## Aesthetic Direction

- **Direction:** Quiet utility desk.
- **Decoration level:** Intentional but restrained. The layout carries the identity; decoration never competes with writing or speaking.
- **Mood:** Calm, capable, and tactile. It should feel like a well-made desktop tool, not a browser dashboard.
- **Reference:** The token system in `/home/prshv/dev/parshvagala_dotcom/style.css`.
- **Signature:** A lime recording rail and timer against an ink panel. The one high-contrast moment belongs to speaking.

## Typography

- **Display:** Fraunces, 600 weight — titles need a quiet editorial confidence without becoming ornamental.
- **Body/UI:** Afacad — open and legible in compact controls and settings forms.
- **Data:** IBM Plex Mono — timers and shortcuts only.
- **Fallbacks:** DejaVu Serif, Noto Sans, and DejaVu Sans Mono. These keep the app readable on a clean Ubuntu installation.
- **Shipping:** Bundle the OFL font files with the binary before the first release; do not depend on a user's installed fonts.
- **Scale:** eyebrow 11px, helper 12px, body 14px, labels 13px, section title 25px, page title 38px, metric 30px.

## Color

- **Approach:** Restrained. Color conveys state, not decoration.
- **Paper:** `#F4F1EA` — main workspace.
- **Surface:** `#FFFDF6` — cards and inputs.
- **Soft surface:** `#F2ECDC` — sidebar.
- **Muted surface:** `#E7DFCC` — selected and contextual regions.
- **Ink:** `#14130F` — text and the recording deck.
- **Muted ink:** `#706B5E` — helper text.
- **Recording lime:** `#D5F06F` — record action and active state.
- **Moss:** `#49614B` — supporting active/status color.
- **Focus blue:** `#2F6FED` — keyboard focus only.
- **Clay:** `#D65A31` — destructive actions and errors only.
- **Dark mode:** Deferred. Do not simply invert this system; define dedicated dark surfaces when it is introduced.

## Spacing

- **Base unit:** 4px.
- **Density:** Comfortable, with a compact sidebar.
- **Scale:** 2xs 4px, xs 8px, sm 12px, md 16px, lg 24px, xl 32px, 2xl 48px, 3xl 64px.

## Layout

- **Approach:** Grid-disciplined desktop layout.
- **Sidebar:** 244px fixed rail for primary navigation and one secondary action.
- **Main canvas:** 46px horizontal and 38px vertical inset at the initial desktop size.
- **Home:** Header, recording deck, then a 3:1 split between transcript history and concise statistics.
- **Settings:** 208px settings rail plus one calm control sheet.
- **Radius:** 6px for identity marks, 7px for controls, 8px for row states, 12px for panels.

## Motion

- **Approach:** Minimal-functional.
- **Durations:** 160ms for hover/focus, 220ms for state transitions.
- **Recording:** A restrained timer and state change. No decorative looping animation.

## Rules

- The record action is the only lime primary action on a screen.
- Never add gradients, glass effects, or a generic dark dashboard treatment.
- Prefer fewer, larger surfaces over many nested cards.
- Every keyboard-focusable control must expose a visible blue focus treatment.
- New visual work must follow this file unless the product direction changes deliberately.

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-07-10 | Quiet utility desk system | Fits an Ubuntu-first dictation tool that should feel serious and unobtrusive. |
