Weekly running mileage planner with natural language workout entry, drag-and-drop rearrangement, and week-over-week stats. Optionally exports workouts as Garmin-compatible FIT files.

## Spec

- **Data model**: State stored as `{ weeks: { [isoWeekKey]: { [dayISO]: Workout } }, settings: { unit } }` where Workout has `distance`, `type`, and `notes` fields.
- **Week keys**: ISO 8601 week format (`2026-W15`), weeks start Monday.
- **Natural language parser**: Extracts distance (mi/km/k/marathon/half) and workout type (easy, tempo, intervals, long run, race, cross-train, rest) from free-text input. Unrecognized text preserved as notes.
- **Workout types**: Easy, Tempo, Intervals, Long Run, Race, Cross-Train, Rest, Other — each color-coded.
- **Persistence**: localStorage with debounced save (300ms). JSON export/import for backup.
- **Stats**: Weekly total, type breakdown with colored pills, week-over-week % change with >10% injury risk warning.
- **Drag and drop**: HTML5 DnD API swaps workouts between day cells.
- **Month overview**: 5-week compact view centered on current week; click a row to navigate.
- **FIT export**: Minimal binary FIT encoder generates workout files (distance-based steps, sport=running) importable into Garmin Connect.
- **Units**: Toggle between miles and kilometers; converts all existing data on switch.

## Backlog

- Structured interval step encoding in FIT files (e.g., 5×1km with recovery)
- Training plan templates (16-week marathon, couch-to-5K, etc.)
- Strava API integration to overlay completed activities vs. planned
- Mobile long-press drag fallback
- Undo/redo
- Weekly goal setting with progress bar
- Copy week / repeat week pattern
