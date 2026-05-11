A tracker for the card game Phase 10. Each player has a large, easy-to-read
phase number with simple +/− buttons to advance or correct their progress.
Score tracking is optional, and players can be added or removed at any time.

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
- "New Game" resets phases and scores but keeps player names.
- Phase reference panel lists all 10 phase goals plus card penalty values.

## Backlog

- Quick-add buttons for common card values (5/10/15/25)
- Per-round history (track who completed each round, undo round)
- Sort players by phase or score
- Custom phase variants (House Rules / Phase 10 Masters)
