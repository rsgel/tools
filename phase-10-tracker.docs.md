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
- A "Track scores" checkbox shows/hides per-player score inputs; the "+" next
  to a score prompts for a delta to add to the current total.
- "Keep screen on" uses the Wake Lock API to prevent the device from sleeping
  during a game; gracefully disabled on browsers without support and
  re-acquired automatically when the tab becomes visible again.
- "New Game" resets phases and scores but keeps player names.
- Phase reference panel lists all 10 phase goals plus card penalty values.

Visual design:
- Each card's background color is computed from the player's phase via HSL,
  shifting from pale cool blue at phase 1 through green/yellow/orange to a
  vivid red at phase 10. The phase-number text colour switches to white when
  the background lightness drops below ~70% so the number stays legible.
- Mobile (≤600px) uses a 2-column grid so all players fit on one screen
  without scrolling for typical Phase 10 games (2–6 players).
- Animations: phase number bumps when changed (Web Animations API), new
  player cards slide in, and the winner card has a pulsing gold glow.

## Backlog

- Quick-add buttons for common card values (5/10/15/25)
- Per-round history (track who completed each round, undo round)
- Sort players by phase or score
- Custom phase variants (House Rules / Phase 10 Masters)
