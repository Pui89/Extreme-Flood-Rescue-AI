"""Standard-library tests for spatial drainage intelligence."""
import unittest
from pui89_autonomy.drainage_intelligence import (
    ClassifiedPoint, analyze_dem, build_drainage_report,
    extract_drainage_features, verify_drainage_report,
)

class DrainageTests(unittest.TestCase):
    def points(self):
        return [
            ClassifiedPoint(1,2,3,"drainage_inlet",0.95,"survey-A"),
            ClassifiedPoint(2,3,2,"culvert",0.8,"survey-A"),
            ClassifiedPoint(3,4,1,"outfall",0.3,"survey-B"),
        ]

    def test_extracts_confident_supplied_classes(self):
        found = extract_drainage_features(self.points(), minimum_confidence=0.5)
        self.assertEqual([f.feature_type for f in found], ["drainage_inlet","culvert"])
        self.assertTrue(all(f.review_required for f in found))

    def test_unknown_class_rejected(self):
        with self.assertRaises(ValueError):
            extract_drainage_features([ClassifiedPoint(0,0,0,"road",0.9,"survey")])

    def test_invalid_confidence_source_and_coordinate_rejected(self):
        invalid = [
            ClassifiedPoint(0,0,0,"culvert",1.1,"survey"),
            ClassifiedPoint(0,0,0,"culvert",0.8," "),
            ClassifiedPoint(float("nan"),0,0,"culvert",0.8,"survey"),
        ]
        for p in invalid:
            with self.subTest(point=p), self.assertRaises(ValueError):
                extract_drainage_features([p])

    def test_dem_local_low_and_downslope(self):
        cells = analyze_dem([[3,2,3],[2,0,2],[3,2,3]], cell_size_m=1)
        center = next(c for c in cells if (c.row,c.col)==(1,1))
        self.assertTrue(center.is_local_low)
        self.assertIsNone(center.downslope_neighbor)
        corner = next(c for c in cells if (c.row,c.col)==(0,0))
        self.assertIsNotNone(corner.downslope_neighbor)

    def test_dem_rejects_ragged_nonfinite_and_bad_resolution(self):
        for grid in ([[1,2],[3]], [[1,float("inf")],[3,4]]):
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                analyze_dem(grid, cell_size_m=1)
        with self.assertRaises(ValueError):
            analyze_dem([[1,2],[3,4]], cell_size_m=0)

    def test_report_deterministic_review_only_and_verifiable(self):
        args=(self.points(), [[3,2],[2,1]])
        a=build_drainage_report(*args,cell_size_m=1,source_dataset_id="synthetic-demo")
        b=build_drainage_report(*args,cell_size_m=1,source_dataset_id="synthetic-demo")
        self.assertEqual(a,b)
        self.assertTrue(verify_drainage_report(a))
        self.assertEqual(a["status"],"REVIEW_REQUIRED")
        self.assertFalse(a["physical_safety_validated"])
        self.assertFalse(a["robot_commands_emitted"])

    def test_tampering_breaks_checksum(self):
        report=build_drainage_report(self.points(),[[3,2],[2,1]],cell_size_m=1,source_dataset_id="synthetic-demo")
        report["summary"]["candidate_feature_count"]=999
        self.assertFalse(verify_drainage_report(report))

    def test_dataset_provenance_required(self):
        with self.assertRaises(ValueError):
            build_drainage_report(self.points(),[[1,2],[3,4]],cell_size_m=1,source_dataset_id=" ")

if __name__ == "__main__":
    unittest.main()
