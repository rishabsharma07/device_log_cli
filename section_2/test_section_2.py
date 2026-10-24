import json
import tempfile
import unittest
from pathlib import Path

from log_summarizer import (
    read_telemetry_csv,
    aggregate_telemetry,
    filter_devices_by_max_temp,
    export_to_json,
)


class TestLogSummarizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_csv_reading_and_malformed_handling(self):
        csv_file = self.test_dir_path / "test_data.csv"
        csv_content = (
            "device_id,status,temperature\n"
            "DEV_A,ACTIVE,25.5\n"
            "DEV_A,ERROR,27.5\n"
            "DEV_B,WARNING,invalid_temp\n"  # corrupt row, should skip
            ",ACTIVE,30.0\n"               # empty device id, should skip
            "DEV_C,ERROR,95.0\n"
        )
        csv_file.write_text(csv_content, encoding="utf-8")

        records, skipped, error_msg = read_telemetry_csv(str(csv_file))
        self.assertIsNone(error_msg)
        self.assertEqual(len(records), 3)
        self.assertEqual(skipped, 2)
        self.assertEqual(records[0]["device_id"], "DEV_A")

    def test_missing_file_handling(self):
        records, skipped, error_msg = read_telemetry_csv("non_existent_file.csv")
        self.assertIsNone(records)
        self.assertIn("does not exist", error_msg)

    def test_aggregation_calculations(self):
        records = [
            {"device_id": "DEV_A", "status": "ACTIVE", "temperature": 60.0},
            {"device_id": "DEV_A", "status": "ERROR", "temperature": 70.0},
            {"device_id": "DEV_B", "status": "ACTIVE", "temperature": 85.0},
            {"device_id": "DEV_B", "status": "ERROR", "temperature": 95.0},
        ]
        aggregated = aggregate_telemetry(records)

        self.assertIn("DEV_A", aggregated)
        self.assertEqual(aggregated["DEV_A"]["total_records"], 2)
        self.assertEqual(aggregated["DEV_A"]["avg_temperature"], 65.0)
        self.assertEqual(aggregated["DEV_A"]["error_count"], 1)

        self.assertIn("DEV_B", aggregated)
        self.assertEqual(aggregated["DEV_B"]["total_records"], 2)
        self.assertEqual(aggregated["DEV_B"]["avg_temperature"], 90.0)
        self.assertEqual(aggregated["DEV_B"]["error_count"], 1)

    def test_filtering_above_80(self):
        aggregated = {
            "DEV_A": {"device_id": "DEV_A", "avg_temperature": 79.9, "total_records": 10, "error_count": 0},
            "DEV_B": {"device_id": "DEV_B", "avg_temperature": 80.0, "total_records": 10, "error_count": 1},
            "DEV_C": {"device_id": "DEV_C", "avg_temperature": 80.1, "total_records": 10, "error_count": 2},
            "DEV_D": {"device_id": "DEV_D", "avg_temperature": 95.0, "total_records": 5, "error_count": 3},
        }
        filtered = filter_devices_by_max_temp(aggregated, max_temp_threshold=80.0)

        # DEV_A (79.9) and DEV_B (80.0) should be retained; DEV_C (80.1) and DEV_D (95.0) should be dropped
        self.assertIn("DEV_A", filtered)
        self.assertIn("DEV_B", filtered)
        self.assertNotIn("DEV_C", filtered)
        self.assertNotIn("DEV_D", filtered)

    def test_export_to_json(self):
        filtered = {
            "DEV_1": {"device_id": "DEV_1", "total_records": 3, "avg_temperature": 55.4, "error_count": 1}
        }
        json_path = self.test_dir_path / "out.json"
        export_to_json(filtered, str(json_path))

        self.assertTrue(json_path.exists())
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["device_id"], "DEV_1")


if __name__ == "__main__":
    unittest.main()
