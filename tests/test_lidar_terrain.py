import math
import unittest

from tools.pui89_lidar import (
    d8_flow_direction,
    flow_accumulation,
    slope_degrees,
    validate_lidar_metadata,
)


class LidarMetadataTests(unittest.TestCase):
    def valid_metadata(self):
        return {
            "source_id": "synthetic-lidar-001",
            "source_sha256": "a" * 64,
            "acquired_at": "2026-11-10T09:00:00Z",
            "crs": "EPSG:32647",
            "horizontal_units": "metres",
            "vertical_datum": "EGM2008",
            "vertical_units": "metres",
            "classification_scheme": "LAS 1.4 ASPRS",
        }

    def test_valid_metadata_and_finite_coordinates(self):
        report = validate_lidar_metadata(self.valid_metadata(), [(1.0, 2.0, 3.0)])
        self.assertEqual(report["status"], "VALID")
        self.assertEqual(report["point_count_checked"], 1)
        self.assertFalse(report["execution_authorized"])

    def test_missing_crs_and_units_fail_closed(self):
        metadata = self.valid_metadata()
        metadata["crs"] = ""
        metadata["horizontal_units"] = ""
        report = validate_lidar_metadata(metadata)
        self.assertEqual(report["status"], "INVALID")
        self.assertIn("missing_or_invalid:crs", report["errors"])
        self.assertIn("missing_or_invalid:horizontal_units", report["errors"])

    def test_naive_timestamp_is_rejected(self):
        metadata = self.valid_metadata()
        metadata["acquired_at"] = "2026-11-10T09:00:00"
        self.assertIn("timezone_required:acquired_at", validate_lidar_metadata(metadata)["errors"])

    def test_bad_hash_and_unknown_vertical_datum_are_rejected(self):
        metadata = self.valid_metadata()
        metadata["source_sha256"] = "not-a-hash"
        metadata["vertical_datum"] = "unknown"
        errors = validate_lidar_metadata(metadata)["errors"]
        self.assertIn("invalid:source_sha256", errors)
        self.assertIn("unknown:vertical_datum", errors)

    def test_non_finite_coordinates_are_rejected(self):
        report = validate_lidar_metadata(self.valid_metadata(), [(1.0, float("nan"), 3.0)])
        self.assertEqual(report["status"], "INVALID")
        self.assertIn("non_finite_or_non_numeric:0:y", report["errors"])

    def test_empty_coordinate_input_is_rejected(self):
        self.assertIn("empty_coordinates", validate_lidar_metadata(self.valid_metadata(), [])["errors"])


class SyntheticTerrainTests(unittest.TestCase):
    def test_planar_slope_matches_analytic_gradient(self):
        grid = [[float(c) for c in range(5)] for _ in range(5)]
        result = slope_degrees(grid, cell_size_x=1.0, cell_size_y=1.0)
        self.assertAlmostEqual(result[2][2], 45.0)

    def test_nodata_and_edges_are_not_interpolated(self):
        grid = [[1.0] * 5 for _ in range(5)]
        grid[2][1] = None
        result = slope_degrees(grid)
        self.assertIsNone(result[0][2])
        self.assertIsNone(result[2][2])

    def test_d8_routes_downhill_and_keeps_sink_terminal(self):
        grid = [
            [9.0, 8.0, 7.0],
            [8.0, 5.0, 6.0],
            [7.0, 6.0, 1.0],
        ]
        direction = d8_flow_direction(grid)
        self.assertEqual(direction[1][1], (1, 1))
        self.assertIsNone(direction[2][2])

    def test_flow_accumulation_counts_converging_upstream_cells(self):
        directions = [
            [(1, 1), (1, 0), (1, -1)],
            [None, (1, 0), None],
            [None, None, None],
        ]
        result = flow_accumulation(directions)
        self.assertEqual(result[1][1], 4)
        self.assertEqual(result[2][1], 5)

    def test_flow_accumulation_preserves_explicit_nodata_mask(self):
        directions = [[None, None], [None, (-1, 0)]]
        mask = [[False, True], [False, True]]
        result = flow_accumulation(directions, valid_mask=mask)
        self.assertEqual(result, [[None, 2], [None, 1]])

    def test_flow_accumulation_rejects_cycles(self):
        directions = [[(0, 1), (0, -1)]]
        with self.assertRaisesRegex(ValueError, "cycle"):
            flow_accumulation(directions)

    def test_invalid_grid_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            slope_degrees([[1.0, 2.0], [3.0, math.inf]])


if __name__ == "__main__":
    unittest.main()
