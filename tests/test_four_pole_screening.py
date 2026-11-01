import math
import unittest

from tools.four_pole_screening import DISCLAIMER, calculate_screening


class FourPoleScreeningTests(unittest.TestCase):
    def inputs(self):
        return {
            "water_density_kg_m3": 1000.0,
            "drag_coefficient": 1.0,
            "projected_area_m2": 0.1,
            "current_velocity_m_s": 2.0,
            "elastic_modulus_pa": 200e9,
            "second_moment_area_m4": 1e-6,
            "effective_length_factor": 1.0,
            "unsupported_length_m": 2.0,
            "axial_compressive_load_n": 1000.0,
        }

    def test_calculates_drag_moment_and_euler_screen(self):
        result = calculate_screening(**self.inputs())
        self.assertAlmostEqual(result["results"]["steady_flow_drag_estimate_n"], 200.0)
        self.assertAlmostEqual(
            result["results"]["drag_times_unsupported_length_moment_estimate_nm"],
            400.0,
        )
        expected = math.pi**2 * 200e9 * 1e-6 / 2.0**2
        self.assertAlmostEqual(
            result["results"]["ideal_euler_critical_load_estimate_n"], expected
        )
        self.assertEqual(
            result["status"], "SCREENING_RESULT_ONLY_NO_SAFETY_VERDICT"
        )

    def test_zero_current_produces_zero_drag(self):
        values = self.inputs()
        values["current_velocity_m_s"] = 0
        result = calculate_screening(**values)
        self.assertEqual(result["results"]["steady_flow_drag_estimate_n"], 0)

    def test_zero_axial_load_produces_zero_demand_ratio(self):
        values = self.inputs()
        values["axial_compressive_load_n"] = 0
        result = calculate_screening(**values)
        self.assertEqual(
            result["results"]["axial_demand_divided_by_ideal_euler_load"], 0
        )

    def test_rejects_negative_velocity(self):
        values = self.inputs()
        values["current_velocity_m_s"] = -0.1
        with self.assertRaisesRegex(ValueError, "current_velocity_m_s"):
            calculate_screening(**values)

    def test_rejects_zero_geometry_and_material_inputs(self):
        for field in (
            "water_density_kg_m3",
            "drag_coefficient",
            "projected_area_m2",
            "elastic_modulus_pa",
            "second_moment_area_m4",
            "effective_length_factor",
            "unsupported_length_m",
        ):
            values = self.inputs()
            values[field] = 0
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    calculate_screening(**values)

    def test_rejects_non_finite_values(self):
        values = self.inputs()
        values["projected_area_m2"] = float("nan")
        with self.assertRaisesRegex(ValueError, "projected_area_m2"):
            calculate_screening(**values)

    def test_report_carries_strong_limitations(self):
        result = calculate_screening(**self.inputs())
        self.assertEqual(result["disclaimer"], DISCLAIMER)
        self.assertIn("no load sharing assumed", result["scope"])
        self.assertTrue(result["required_next_step"].startswith("Independent"))


if __name__ == "__main__":
    unittest.main()
