"""
Section 1: Coding Logic & Sanitization
Sensor Reading Normalizer and Cleaner

Requirements:
1. Type Conversion & Filtering: Convert elements to floats where possible.
   Drop values that cannot be converted, are None, or are negative (< 0).
2. Clipping: If any valid number exceeds 500.0, cap/limit it to 500.0.
3. Edge Case Handling: Handle empty lists or lists with entirely invalid entries
   gracefully without throwing an unhandled exception.
"""

from typing import Any, List
import math


def clean_sensor_readings(readings: Any) -> List[float]:
    if not readings or not hasattr(readings, "__iter__"):
        return []

    cleaned: List[float] = []

    for item in readings:
        if item is None:
            continue

        if isinstance(item, bool):
            continue

        try:
            val = float(item)
        except (ValueError, TypeError):
            continue

        if math.isnan(val) or math.isinf(val):
            continue

        if val < 0.0:
            continue

        if val > 500.0:
            val = 500.0

        cleaned.append(val)

    return cleaned


def run_simple_tests() -> None:

    test_cases = [
        {
            "name": "Standard mixed inputs with strings, negatives, and None",
            "input": [12.5, "45.0", -999, None, "error", 150.2, -1.0],
            "expected": [12.5, 45.0, 150.2],
        },
        {
            "name": "Values exceeding 500.0 (clipping check)",
            "input": [50.0, 500.0, 500.1, 1200.5, "999.9"],
            "expected": [50.0, 500.0, 500.0, 500.0, 500.0],
        },
        {
            "name": "Empty list and all invalid/null entries",
            "input": [None, "invalid", -50, "N/A", False, True],
            "expected": [],
        },
        {
            "name": "Empty list edge case",
            "input": [],
            "expected": [],
        },
    ]

    print("=" * 60)
    print("Section 1: Sensor Readings Sanitizer Verification")
    print("=" * 60)
    all_passed = True
    for idx, tc in enumerate(test_cases, 1):
        result = clean_sensor_readings(tc["input"])
        passed = result == tc["expected"]
        status = "PASSED" if passed else "FAILED"
        print(f"Test {idx}: {tc['name']}")
        print(f"  Input:    {tc['input']}")
        print(f"  Output:   {result}")
        print(f"  Expected: {tc['expected']}")
        print(f"  Status:   [{status}]\n")
        if not passed:
            all_passed = False

    if all_passed:
        print("All Section 1 test cases PASSED successfully.")
    else:
        print("Some Section 1 test cases FAILED.")


if __name__ == "__main__":
    run_simple_tests()
