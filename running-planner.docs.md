Weekly running mileage planner with natural language workout entry, drag-and-drop rearrangement, and week-over-week stats. Optionally exports workouts as Garmin-compatible FIT files.

## Spec

- **Data model**: State stored as `{ weeks: { [isoWeekKey]: { [dayISO]: Workout } }, settings: { unit, runPace, xtRatio } }` where Workout has `distance`, `type`, `notes`, and optionally `timeMinutes` and `isCrossTrain` fields.
- **Week keys**: ISO 8601 week format (`2026-W15`), weeks start Monday.
- **Natural language parser**: Extracts distance (mi/km/k/marathon/half), time (min/hr), and workout type (easy, tempo, intervals, long run, race, cross-train, rest) from free-text input. Unrecognized text preserved as notes.
- **Time-based entry**: Inputs like "45min easy" or "1hr 30min long run" are converted to distance using the configured running pace (default 10:00/mi). Cross-training time (e.g. "45min bike") is converted at a reduced rate (default 33%) to running-equivalent mileage.
- **Pace settings**: Configurable running pace (mm:ss per mile) and cross-training equivalence ratio (0–100%). Changing settings recalculates all time-based workouts.
- **Workout types**: Easy, Tempo, Intervals, Long Run, Race, Cross-Train, Rest, Other — each color-coded.
- **Long run volume bubble**: Long Run workouts display a badge showing what percentage of weekly volume they represent.
- **Cross-training display**: Cross-training workouts show an equivalence badge (e.g. "≈ 1.5 mi eq.") and are displayed separately in the stats bar.
- **Persistence**: localStorage with debounced save (300ms). JSON export/import for backup.
- **Stats**: Weekly total (running + xt shown separately when cross-training present), type breakdown with colored pills, week-over-week % change with >10% injury risk warning.
- **Drag and drop**: HTML5 DnD API swaps workouts between day cells.
- **Month overview**: 5-week compact view centered on current week; click a row to navigate.
- **FIT export**: Minimal binary FIT encoder generates workout files (distance-based steps, sport=running) importable into Garmin Connect.
- **Units**: Toggle between miles and kilometers; converts all existing data on switch.
- **Mobile**: Responsive single-column layout with larger touch targets, visible delete buttons, 16px inputs (prevents iOS zoom), and Tab key navigation between days.

## Backlog

- Structured interval step encoding in FIT files (e.g., 5×1km with recovery)
- Training plan templates (16-week marathon, couch-to-5K, etc.)
- Strava API integration to overlay completed activities vs. planned
- Mobile long-press drag fallback
- Undo/redo
- Weekly goal setting with progress bar
- Copy week / repeat week pattern
