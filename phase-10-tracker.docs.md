A tracker for the card game Phase 10. Each player has a large, easy-to-read
phase number with simple +/− buttons to advance or correct their progress.
Score tracking is optional, players can be added or removed at any time, and
each card's color intensifies as the player approaches phase 10.

## Spec

Core data model: a list of players, each with `{id, name, phase, score}`.
Phase ranges from 1 to 10; once a player advances past 10 they are marked as
the winner. State is persisted in the URL hash so games can be shared or
resumed by reopening the link.

Key behaviors:
- Tap +/− to advance or undo a phase (the most common action — large hit area).
- Tap a player name to rename inline.
- A "Track scores" checkbox shows/hides a per-player score panel. Scores are
  tallied with quick-add buttons (+5 / +10 / +25) matching the common card
  penalty values, so you can tap as you count cards; tap the score value to
  set an exact total (for corrections).
- Interactive controls use `touch-action: manipulation` to suppress
  double-tap-to-zoom (pinch-zoom still works), since rapid phase/score
  tapping previously triggered zooms on mobile.
- "Keep screen on" uses the Wake Lock API to prevent the device from sleeping
  during a game; gracefully disabled on browsers without support and
  re-acquired automatically when the tab becomes visible again.
- "New Game" resets phases and scores but keeps player names.
- "Copy Results" copies a plain-text standings summary for sharing, headed
  with "Phase 10 — M/D/YY" (today's local date), ranked by phase (furthest
  first); when scores are tracked, ties break on the lower score (which wins
  in Phase 10) and "pts" are included per player.
- Phase reference panel lists all 10 phase goals plus card penalty values.

Visual design:
- Each card's background color is computed from the player's phase via HSL,
  shifting from pale cool blue at phase 1 through green/yellow/orange to a
  vivid red at phase 10. Text colour (dark hue-tinted ink vs white) is chosen
  by comparing actual WCAG relative-luminance contrast against the background
  rather than a raw HSL-lightness threshold — bright mid-scale hues like
  yellow/green read as far lighter than their lightness value, so the old
  threshold wrongly put white text on them. In practice phases 1–9 use dark
  ink and only phase 10 (red) uses white. An adaptive text-shadow "glow"
  (light halo under dark ink, dark halo under white) gives the phase number
  and goal text extra legibility on any hue.
- Mobile (≤600px) uses a 2-column grid so all players fit on one screen
  without scrolling for typical Phase 10 games (2–6 players).
- Animations: phase number bumps when changed (Web Animations API), new
  player cards slide in, and the winner card has a pulsing gold glow.

## Backlog

- Per-round history (track who completed each round, undo round)
- Sort players by phase or score
- Custom phase variants (House Rules / Phase 10 Masters)
