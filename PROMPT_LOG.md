# AI Collaboration & Prompt Log (`PROMPT_LOG.md`)

This document records the interaction with the AI assistant to create the visualization module for Section 3 of the **Software Engineering Intern Technical Assessment**.

---

## 1. Initial Prompt to AI Assistant

```text
Write a Python script using matplotlib that reads 'summary_output.json' (which contains device_id, total_records, avg_temperature, and error_count) and generates a bar chart comparing the average temperature per device. Save the resulting plot as 'avg_temp_chart.png'.
```

### Initial Code Produced by the AI:
```python
import json
import matplotlib.pyplot as plt

with open('summary_output.json') as f:
    data = json.load(f)

devices = [d['device_id'] for d in data]
temps = [d['avg_temperature'] for d in data]

plt.bar(devices, temps)
plt.title('Average Temperature')
plt.xlabel('Device')
plt.ylabel('Temperature')
plt.savefig('avg_temp_chart.png')
plt.show()
```

---

## 2. Issues & Formatting Mistakes Identified in First Attempt

Upon code inspection and trial run, several layout, formatting, and robustness defects were identified:

1. **Overlapping and Truncated X-Axis Labels**:
   - The device identifiers were plotted horizontally without rotation or spacing adjustments (`plt.bar(devices, temps)`). For longer device IDs or larger datasets, labels collide and become unreadable.
   - `plt.tight_layout()` was omitted, causing x-axis labels to be clipped at the bottom boundary of the image.

2. **Missing Quantitative Value Callouts & Ambiguous Scale**:
   - There were no value annotations on the bars. Readers had to visually guess whether a device was at 76°C vs 78°C.
   - The y-axis had no explicit headroom above the tallest bar, meaning any added labels would collide with the plot's top border.
   - Missing unit symbols (°C) on the y-axis label and title.

3. **No Visual Reference for Assessment Threshold**:
   - Section 2 defines an 80.0°C filter boundary, but the chart provided no visual indicator showing how close retained devices were to this critical limit.

4. **Environment and Robustness Vulnerabilities**:
   - `plt.show()` triggers GUI display errors on headless environments or automated servers without an active display backend.
   - No error handling for missing files, empty lists, or malformed JSON keys.

---

## 3. Follow-Up Prompt to AI Assistant

```text
The initial script works as a minimal prototype, but has several formatting, layout, and robustness issues:
1. When multiple or long device IDs are present, the x-axis labels overlap and get clipped at the bottom margin. Please rotate the tick labels by 30-45 degrees, align them to the right, and call plt.tight_layout().
2. Add text annotations directly above each bar displaying the exact average temperature formatted to 1 decimal place with a '°C' unit, and increase the y-axis limit by ~15% to provide headroom.
3. Draw a horizontal dashed red reference line at y = 80.0°C indicating the filtering threshold, along with a legend entry.
4. Use a headless matplotlib backend ('Agg') so it safely renders without a GUI, and wrap file loading in proper error checks for empty or missing JSON files.
5. Provide a CLI interface with argparse for --input and --output flags.
```

---

## 4. Resolution & Polished Implementation

The resulting refined script was incorporated into `visualize_summary.py`:
- Added `matplotlib.use('Agg')` for headless execution.
- Configured dynamic bar coloring, text labels (`ax.annotate` with `zorder=5` and white background badge), and a dashed 80°C threshold line.
- Added rotated x-ticks with right alignment and `tight_layout()`.
- Implemented file existence and JSON schema validation with informative error messages.
- Added CLI argument parsing (`--input`, `--output`) with sensible defaults.
- Successfully generated `avg_temp_chart.png` with clean, publication-ready aesthetics.
