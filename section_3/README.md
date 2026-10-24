# Section 3: AI Prompting & Charting Challenge

## Problem Statement
Prompt an AI assistant to generate a bar chart script in Python using `matplotlib` comparing average temperature per device from `summary_output.json`. Review the initial code, identify and fix layout/formatting bugs, and run the corrected script to output `avg_temp_chart.png`.

## AI Collaboration Log
A complete log detailing the initial prompt, identified defects (overlapping tick labels, lack of value labels, missing threshold reference line), follow-up prompt, and resulting code is documented in [`PROMPT_LOG.md`](file:///PROMPT_LOG.md).

## Visualization Improvements
1. **Label Collision Prevention**: Rotates x-axis labels by 30° with right alignment and calls `tight_layout()`.
2. **Numeric Callouts**: Displays exact values (`xx.x°C`) on top of bars with clean badge containers.
3. **Threshold Reference**: Includes a dashed red reference line at `80.0°C` with an informative legend.
4. **Robust Headless Execution**: Employs `matplotlib.use('Agg')` for headless/server execution without GUI requirements.

## How to Run

### Generate Chart:
```bash
python visualize_summary.py --input summary_output.json --output avg_temp_chart.png
```

### Run Unit Tests:
```bash
python -m unittest test_section_3.py -v
```
