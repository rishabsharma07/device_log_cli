# Section 1: Coding Logic & Sanitization

## Problem Statement
Clean and normalize sensor readings from a list containing mixed inputs (floats, integers, numeric strings, `None` nulls, non-numeric strings, negative error flags, and booleans).

## Rules Applied
1. **Type Conversion & Filtering**:
   - Converts valid numeric entries to `float`.
   - Drops `None`, non-numeric strings, `NaN`, `Inf`, and boolean types (`True`/`False`).
   - Drops negative numbers (`< 0.0`).
2. **Clipping**:
   - Caps any valid reading exceeding `500.0` to `500.0`.
3. **Edge Case Handling**:
   - Gracefully handles empty lists, non-iterables, and lists with completely invalid entries returning `[]` without unhandled exceptions.

## How to Run

### Run Built-in Verification:
```bash
python sensor_sanitizer.py
```

### Run Unit Tests:
```bash
python -m unittest test_section_1.py -v
```
