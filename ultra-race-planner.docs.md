A race logistics planner for ultrarunners. Set up your race details, define aid stations with crew access and drop bag info, build a nutrition product inventory, and assign nutrition to each segment between aid stations. Review per-hour nutrition rates against your targets on the dashboard, then export as YAML (for re-import) or Markdown (for reading in a notes app).

## Spec

Six-tab UI: Race Setup, Aid Stations, Nutrition Inventory, Segment Planner, Dashboard, Export/Import.

**Data model**: Race (name, distance, goalTime, elevationGain/Loss) → Aid Stations (name, distance, elevation, cutoffTime, crewAccess, hasDropBag, dropBagContents, notes) → Products (name, carbs/sodium/caffeine/calories per serving, UUID id) → Segments (auto-generated from aid stations, each with plannedNutrition/carryItems/aidStationPickup arrays of {productId, quantity} and a free-text notes field for gear/reminders).

**GPX parsing**: DOMParser extracts `<trkpt>` lat/lon/ele, Haversine formula for cumulative distance (miles), elevation gain/loss in feet. Downsamples to ~500 points max. Auto-populates station elevation when distance is entered.

**Nutrition tracking**: Per-segment totals calculated from product inventory references. Per-hour rates derived from segment estimated time (even-pace split). Color-coded against user-defined targets (green ≥90%, yellow ≥70%, red <70%).

**Persistence**: localStorage auto-saves state on every change (debounced 300ms). YAML export (js-yaml v4 via CDN) for structured backup/restore. YAML import restores full state. Markdown export for human-readable race plan. "New Plan" button clears all data.

## Backlog

- Map visualization of GPX route
- Crew guide as a separate export view
- Print-to-PDF formatting
- Pacing adjustments based on elevation/terrain difficulty
- Multiple crew member coordination
- Timing of nutrient absorption windows
- Account system or cloud storage
