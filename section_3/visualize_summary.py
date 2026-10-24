"""
Section 3: AI Prompting & Charting Challenge
Device Average Temperature Visualization Module

Loads the aggregated JSON output from Section 2 and produces a polished bar chart
comparing the average temperature per device using matplotlib.
Includes enhancements for readability (rotated labels, value annotations,
threshold line, proper layout margin, and empty data handling).
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_summary_data(json_filepath: str) -> List[Dict[str, Any]]:

    path = Path(json_filepath)
    if not path.exists():
        print(f"[ERROR] JSON file not found at: '{json_filepath}'", file=sys.stderr)
        return []

    try:
        with open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"[ERROR] Expected JSON root to be a list, found {type(data)}", file=sys.stderr)
            return []

        return data
    except json.JSONDecodeError as e:
        print(f"[ERROR] Malformed JSON in '{json_filepath}': {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"[ERROR] Unable to read '{json_filepath}': {e}", file=sys.stderr)
        return []


def generate_temperature_bar_chart(
    devices_data: List[Dict[str, Any]],
    output_image_path: str = "avg_temp_chart.png",
    threshold_temp: float = 80.0,
) -> bool:

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if not devices_data:
        print("[WARNING] No device data to plot. Skipping chart generation.")
        return False

    # Extract device IDs and temperatures
    device_ids = [str(item.get("device_id", f"Unknown_{i}")) for i, item in enumerate(devices_data)]
    avg_temps = [float(item.get("avg_temperature", 0.0)) for item in devices_data]

    # Initialize figure and axes with comfortable dimensions
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)

    # Distinct color palette: cooler blue for normal, amber/red for near-threshold
    colors = [
        "#2b5c8f" if temp < 75.0 else "#d97706"
        for temp in avg_temps
    ]

    bars = ax.bar(device_ids, avg_temps, color=colors, width=0.55, edgecolor="#1e293b", linewidth=1.2)

    # Add numeric value labels on top of each bar for immediate readability
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}°C",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),  # vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#1e293b",
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9),
        )

    # Reference line for the 80.0°C filtering threshold
    ax.axhline(
        y=threshold_temp,
        color="#dc2626",
        linestyle="--",
        linewidth=1.5,
        label=f"Max Allowed Threshold ({threshold_temp:.0f}°C)",
    )

    # Titles and axis labels
    ax.set_title("Average Temperature per Device (Post-Filtering)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Device ID", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Average Temperature (°C)", fontsize=11, fontweight="bold", labelpad=8)

    # Y-axis scaling: ensure headroom for bar value labels
    max_val = max(avg_temps + [threshold_temp])
    ax.set_ylim(0, max_val * 1.15)

    # Rotate x-axis labels to prevent overlap with long device names
    ax.set_xticks(range(len(device_ids)))
    ax.set_xticklabels(device_ids, rotation=30, ha="right", fontsize=10)

    # Grid lines for ease of comparison
    ax.grid(axis="y", linestyle=":", alpha=0.6, color="#94a3b8")
    ax.set_axisbelow(True)

    # Legend
    ax.legend(loc="upper right", framealpha=0.9)

    # Prevent layout clipping
    plt.tight_layout()

    out_path = Path(output_image_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close(fig)

    print(f"[+] Chart successfully generated and saved to '{output_image_path}'.")
    return True


def main() -> int:
    """CLI entry point for chart generation."""
    parser = argparse.ArgumentParser(
        description="Generates a bar chart comparing average device temperatures from JSON summary."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="summary_output.json",
        help="Path to input JSON summary (default: summary_output.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="avg_temp_chart.png",
        help="Path to output PNG chart (default: avg_temp_chart.png)",
    )
    args = parser.parse_args()

    data = load_summary_data(args.input)
    if not data:
        print("[FATAL] Could not proceed with visualization due to empty or missing data.", file=sys.stderr)
        return 1

    success = generate_temperature_bar_chart(data, output_image_path=args.output)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
