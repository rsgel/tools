FIT file viewer and workout creator. Open FIT activity files from Garmin, Wahoo, and other devices to view workout summaries, lap splits with key averages, interactive charts, and message tables with CSV export. Download a markdown report of any workout. Also create structured workouts from natural language descriptions and download them as FIT files compatible with Garmin Connect.

## Spec

- **Two tabs**: Viewer and Creator.
- **Viewer**: Drag-and-drop or click to open `.fit` files. Binary FIT parser decodes file header, definition messages, and data messages. Groups records by message type.
  - **Workout Summary**: Extracts overall stats from session and record messages — distance, elapsed time, avg pace, heart rate (avg/min/max), cadence, elevation gain/loss, power, calories. Displayed as a stat card grid.
  - **Splits/Laps**: Prominent table showing per-lap breakdown with distance, time, pace (fastest/slowest highlighted), avg/max heart rate, cadence, elevation gain/loss, and power.
  - **Markdown Summary Download**: Generates a markdown report with overall metrics table and per-split table. Downloads as `.md` file.
  - **Chart**: Canvas-based line chart with grid, axis labels, hover tooltip, drag-to-zoom, and reset. Supports heart_rate, speed, cadence, power, altitude, temperature, distance fields.
  - **Message Tables**: Clickable message headers with record counts; expanding shows a data table. CSV download button per table.
- **Creator**: Natural language input parsed into FIT workout steps. Supports time durations (`10 minutes`, `30s`), distance (`3 miles`, `800m`, `5 km`), intensity (`warmup`, `cooldown`, `rest`, `hard`), pace targets (`at 7:30 pace`), HR zones (`zone 3`), repeats (`4x800m with 400m recovery`), and lap button. Preview shows step cards with duration, target, and intensity type. Downloads a binary `.fit` workout file.
- **FIT encoder**: Minimal binary encoder producing valid FIT files with file_id, workout, and workout_step messages. CRC-16 checksums on header and data.
- **FIT parser**: Reads FIT file header, definition records, and data records. Handles little-endian and big-endian architectures, compressed timestamps, and developer fields. Decodes known message types (file_id, session, lap, record, event, device_info, workout, workout_step, activity) with human-readable field names.

## Backlog

- Support for more FIT message types and field decodings (e.g., sport names, event types)
- Structured interval encoding with repeat steps in the FIT file itself
- Import/export workout as JSON for sharing
- Power zone targets
- Cadence targets
- Multi-sport workouts (triathlon)
- Upload FIT file to Garmin Connect directly via API
- Dark mode
- Pace displayed in both /mi and /km with unit toggle
- Power curve / critical power chart
