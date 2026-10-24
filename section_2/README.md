# Section 2: Core Data Processing Task

## Problem Statement
Ingest a CSV telemetry log (`device_telemetry.csv`), aggregate metrics per device, filter out devices whose average temperature exceeds `80.0°C`, export the results to `summary_output.json`, and print an aligned terminal summary table.

## Aggregations Computed
- **Total Records**: Count of records per device.
- **Average Temperature**: Mean temperature per device rounded to 2 decimal places.
- **Error Count**: Total records where `status == "ERROR"`.

## Robustness Features
- Handles missing or unreadable files gracefully without unhandled exceptions.
- Skips malformed rows (non-float temperatures, missing columns, empty IDs) with an informative warning count.
- Filters out devices with average temperature $> 80.0^\circ\text{C}$.

## How to Run

### Run Summarizer CLI:
```bash
python log_summarizer.py
```

### With Custom Arguments:
```bash
python log_summarizer.py --input device_telemetry.csv --output summary_output.json --threshold 80.0
```

### Run Unit Tests:
```bash
python -m unittest test_section_2.py -v
```
