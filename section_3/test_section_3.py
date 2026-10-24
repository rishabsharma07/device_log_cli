"""
Unit tests for Section 3: AI Prompting & Charting Challenge.
"""

import tempfile
import unittest
from pathlib import Path

from visualize_summary import load_summary_data, generate_temperature_bar_chart


class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_chart_generation(self):
        sample_data = [
            {"device_id": "DEV_A", "avg_temperature": 68.5, "total_records": 4, "error_count": 0},
            {"device_id": "DEV_B", "avg_temperature": 76.0, "total_records": 4, "error_count": 1},
        ]
        out_chart = self.test_dir_path / "test_chart.png"
        success = generate_temperature_bar_chart(sample_data, str(out_chart))
        self.assertTrue(success)
        self.assertTrue(out_chart.exists())
        self.assertGreater(out_chart.stat().st_size, 1000)

    def test_empty_chart_handling(self):
        out_chart = self.test_dir_path / "empty_chart.png"
        success = generate_temperature_bar_chart([], str(out_chart))
        self.assertFalse(success)
        self.assertFalse(out_chart.exists())


if __name__ == "__main__":
    unittest.main()
