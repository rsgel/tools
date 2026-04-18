A simple tip calculator that computes tip amount, total bill, and per-person split. Enter the bill amount, select or enter a tip percentage, and specify how many people are splitting the bill to see live calculations.

## Spec

Core data model: bill amount (number), tip percentage (number), number of people (integer ≥ 1).

Live recalculation on any input change. Quick-pick buttons for common tip percentages (15%, 18%, 20%, 25%) update the tip percentage input and recalculate. Results display tip amount, total amount, and highlighted per-person amount.

Currency formatting uses two decimal places. Division by number of people never divides by zero (defaults to 1). No localStorage — stateless calculator.

## Backlog

- Currency selector (USD, EUR, GBP, etc.)
- Custom tip percentage presets (user-configurable)
- Rounding options (round up to nearest dollar)
- Tax calculation (separate from tip)
- Split unevenly (e.g., person A pays 40%, person B pays 60%)
