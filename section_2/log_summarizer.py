"""
Section 2: Core Data Processing Task
Device Log Summarizer CLI Tool

Requirements:
1. Ingestion: Read device telemetry CSV containing device_id, status, temperature.
   Robustly handles missing files, malformed rows, and bad values without crashing.
2. Aggregation: Group by device_id and compute:
   - Total number of records per device
   - Average (mean) temperature
   - Count of records where status is ERROR
3. Filtering: Filter out devices with average temperature > 80.0.
4. Export & Presentation: Save to clean JSON file and print a formatted summary table in terminal.
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_telemetry_csv(
    file_path: str,
) -> Tuple[Optional[List[Dict[str, Any]]], int, Optional[str]]:

    path = Path(file_path)
    if not path.exists():
        return None, 0, f"Error: File '{file_path}' does not exist."
    if not path.is_file():
        return None, 0, f"Error: '{file_path}' is not a regular file."

    valid_records: List[Dict[str, Any]] = []
    skipped_rows = 0

    try:
        with open(path, mode="r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file)
            try:
                raw_header = next(reader)
            except StopIteration:
                return None, 0, f"Error: File '{file_path}' is completely empty."

            # Normalize header column names
            header = [col.strip().lower() for col in raw_header]
            required_columns = {"device_id", "status", "temperature"}
            if not required_columns.issubset(set(header)):
                return (
                    None,
                    0,
                    f"Error: CSV header missing required columns. Required: {required_columns}, Found: {header}",
                )

            device_idx = header.index("device_id")
            status_idx = header.index("status")
            temp_idx = header.index("temperature")

            for row_num, row in enumerate(reader, start=2):
                if not row or all(c.strip() == "" for c in row):
                    continue  # skip blank lines

                if len(row) <= max(device_idx, status_idx, temp_idx):
                    skipped_rows += 1
                    continue

                raw_device = row[device_idx].strip()
                raw_status = row[status_idx].strip().upper()
                raw_temp = row[temp_idx].strip()

                if not raw_device:
                    skipped_rows += 1
                    continue

                try:
                    temperature = float(raw_temp)
                except ValueError:
                    # Skip corrupt temperature readings
                    skipped_rows += 1
                    continue

                valid_records.append(
                    {
                        "device_id": raw_device,
                        "status": raw_status,
                        "temperature": temperature,
                    }
                )

    except Exception as e:
        return None, 0, f"Unexpected error reading '{file_path}': {e}"

    return valid_records, skipped_rows, None


def aggregate_telemetry(
    records: List[Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}

    for record in records:
        dev_id = record["device_id"]
        if dev_id not in grouped:
            grouped[dev_id] = {
                "total_records": 0,
                "temp_sum": 0.0,
                "error_count": 0,
            }

        grouped[dev_id]["total_records"] += 1
        grouped[dev_id]["temp_sum"] += record["temperature"]
        if record["status"] == "ERROR":
            grouped[dev_id]["error_count"] += 1

    summary: Dict[str, Dict[str, Any]] = {}
    for dev_id, stats in grouped.items():
        total = stats["total_records"]
        avg_temp = round(stats["temp_sum"] / total, 2) if total > 0 else 0.0
        summary[dev_id] = {
            "device_id": dev_id,
            "total_records": total,
            "avg_temperature": avg_temp,
            "error_count": stats["error_count"],
        }

    return summary


def filter_devices_by_max_temp(
    summary: Dict[str, Dict[str, Any]], max_temp_threshold: float = 80.0
) -> Dict[str, Dict[str, Any]]:
    return {
        dev_id: stats
        for dev_id, stats in summary.items()
        if stats["avg_temperature"] <= max_temp_threshold
    }


def export_to_json(
    filtered_data: Dict[str, Dict[str, Any]], output_filepath: str
) -> None:

    output_path = Path(output_filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export as list of records sorted by device_id
    records_list = sorted(filtered_data.values(), key=lambda x: x["device_id"])

    with open(output_path, mode="w", encoding="utf-8") as f:
        json.dump(records_list, f, indent=2)


def print_summary_table(
    filtered_data: Dict[str, Dict[str, Any]],
    total_devices_before_filter: int,
    skipped_rows: int = 0,
) -> None:

    print("\n" + "=" * 65)
    print("           DEVICE TELEMETRY SUMMARY REPORT           ")
    print("=" * 65)

    if skipped_rows > 0:
        print(f"[!] Warning: {skipped_rows} corrupted/invalid row(s) were skipped.")

    if not filtered_data:
        print("No devices qualified after applying temperature filter (<= 80.0°C).")
        print("=" * 65 + "\n")
        return

    # Header
    col_dev = "Device ID"
    col_records = "Total Records"
    col_avg_temp = "Avg Temp (C)"
    col_errors = "Error Count"

    header_line = f"{col_dev:<15} | {col_records:>14} | {col_avg_temp:>14} | {col_errors:>12}"
    divider = "-" * len(header_line)

    print(header_line)
    print(divider)

    sorted_devices = sorted(filtered_data.values(), key=lambda x: x["device_id"])
    for dev in sorted_devices:
        print(
            f"{dev['device_id']:<15} | "
            f"{dev['total_records']:>14} | "
            f"{dev['avg_temperature']:>14.2f} | "
            f"{dev['error_count']:>12}"
        )

    print(divider)
    filtered_out_count = total_devices_before_filter - len(filtered_data)
    print(f"Devices retained: {len(filtered_data)} | Filtered out (> 80.0C): {filtered_out_count}")
    print("=" * 65 + "\n")


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Device Log Summarizer CLI - Aggregates and filters device telemetry logs."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="device_telemetry.csv",
        help="Path to input CSV file (default: device_telemetry.csv)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="summary_output.json",
        help="Path to output JSON file (default: summary_output.json)",
    )
    parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=80.0,
        help="Maximum allowed average temperature in Celsius (default: 80.0)",
    )
    return parser.parse_args()


def main() -> int:
    """Main execution flow for Device Log Summarizer."""
    args = parse_arguments()

    records, skipped, error_msg = read_telemetry_csv(args.input)
    if error_msg:
        print(f"[FATAL] {error_msg}", file=sys.stderr)
        return 1

    if not records:
        print(f"[WARNING] No valid data records found in '{args.input}'.", file=sys.stderr)
        export_to_json({}, args.output)
        print_summary_table({}, 0, skipped)
        return 0

    # Aggregate
    aggregated = aggregate_telemetry(records)
    total_devices_before = len(aggregated)

    # Filter
    filtered = filter_devices_by_max_temp(aggregated, max_temp_threshold=args.threshold)

    # Export JSON
    try:
        export_to_json(filtered, args.output)
        print(f"[+] Aggregated summary successfully saved to '{args.output}'.")
    except Exception as e:
        print(f"[FATAL] Failed to export JSON to '{args.output}': {e}", file=sys.stderr)
        return 1

    # Print summary table
    print_summary_table(filtered, total_devices_before, skipped_rows=skipped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
