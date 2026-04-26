Race-day cutoff tracker for crews, spectators, and ultrarunners. Enter aid station distances, cutoff times, and runner check-in times to see the current cutoff cushion plus recent-pace and overall-pace projections for upcoming stations.

## Spec

- **Timing modes**: elapsed race time by default, or clock time using a race start time. Clock entries infer overnight rollovers in aid-station order and also accept explicit `D+1 02:30` / `+1 02:30` prefixes.
- **Aid station model**: each row stores name, distance, cutoff time, and runner arrival/check-in time. Runner times stay editable directly in the table for race-day check-ins; station metadata and removal live behind the Aid Stations section's Edit Stations mode.
- **Predictions**: completed rows show actual margin and segment pace. Future rows show two ETAs and pace references: recent segment pace and overall average pace, each compared against that station's cutoff.
- **Visualization**: canvas chart plots minutes ahead/behind cutoff by distance with actual margins and projected future margins. Points are green when ahead and red when behind.
- **Persistence**: state is saved in localStorage so a crew can reopen the page during a race without losing entered check-ins.

## Backlog

- Export/import full tracker state as JSON
- Add optional departure times and aid-station dwell tracking
- Shareable crew read-only view
- Print-friendly pace and cutoff sheet
