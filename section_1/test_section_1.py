import unittest
from sensor_sanitizer import clean_sensor_readings


class TestSensorSanitizer(unittest.TestCase):
    def test_basic_conversion_and_filtering(self):
        inputs = [10.5, "25.2", 0, -5.0, None, "bad_data", -0.01]
        expected = [10.5, 25.2, 0.0]
        self.assertEqual(clean_sensor_readings(inputs), expected)

    def test_clipping_above_500(self):
        inputs = [499.9, 500.0, 500.1, 1000.0, "9999.0"]
        expected = [499.9, 500.0, 500.0, 500.0, 500.0]
        self.assertEqual(clean_sensor_readings(inputs), expected)

    def test_edge_cases_empty_and_invalids(self):
        self.assertEqual(clean_sensor_readings([]), [])
        self.assertEqual(clean_sensor_readings([None, None]), [])
        self.assertEqual(clean_sensor_readings(["corrupt", "N/A", ""]), [])
        self.assertEqual(clean_sensor_readings(None), [])
        self.assertEqual(clean_sensor_readings(123), [])  # Non-iterable

    def test_booleans_and_special_floats(self):
        # Booleans should not be parsed as 1.0 / 0.0
        inputs = [True, False, float("nan"), float("inf"), 42.0]
        self.assertEqual(clean_sensor_readings(inputs), [42.0])


if __name__ == "__main__":
    unittest.main()
