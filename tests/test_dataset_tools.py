from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tools" / "dataset_inventory.py"
SPLITTER = ROOT / "tools" / "group_split_manifest.py"
AUDITOR = ROOT / "tools" / "audit_dataset_manifest.py"

FIELDS = [
    "image_path", "source_url", "source_name", "dataset_version", "license_name",
    "license_url", "license_status", "attribution", "source_group_id", "sha256",
    "label_status", "label_reviewer", "ground_truth_basis", "split", "notes",
]


def run_tool(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def verified_row(index: int, group: str) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    row.update({
        "image_path": f"image-{index}.jpg",
        "source_url": "https://example.org/data",
        "license_name": "Test licence",
        "license_url": "https://example.org/license",
        "license_status": "approved",
        "source_group_id": group,
        "sha256": hashlib.sha256(f"image-{index}".encode()).hexdigest(),
        "label_status": "human_verified",
        "label_reviewer": "qualified reviewer",
        "ground_truth_basis": "verified fixture label",
    })
    return row


class DatasetToolTests(unittest.TestCase):
    def test_inventory_never_invents_labels_or_licence_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "images"
            root.mkdir()
            (root / "sample.jpg").write_bytes(b"fixture image bytes")
            out = Path(temp) / "manifest.csv"
            result = run_tool(
                INVENTORY, str(root), "--output", str(out),
                "--source-name", "test fixture", "--source-url", "https://example.org/data",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with out.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["label_status"], "unreviewed")
            self.assertEqual(rows[0]["license_status"], "pending_review")
            self.assertEqual(rows[0]["sha256"], hashlib.sha256(b"fixture image bytes").hexdigest())

    def test_splitter_rejects_unreviewed_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.csv"
            row = verified_row(0, "scene-1")
            row["license_status"] = "pending_review"
            row["label_status"] = "unreviewed"
            write_manifest(manifest, [row])
            result = run_tool(SPLITTER, str(manifest))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("licence is not approved", result.stderr)

    def test_splitter_rejects_fewer_than_three_source_groups(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.csv"
            write_manifest(manifest, [verified_row(0, "only-one-source")])
            result = run_tool(SPLITTER, str(manifest))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("at least three distinct source_group_id", result.stderr)

    def test_splitter_keeps_each_group_in_one_partition(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.csv"
            rows = [verified_row(i, f"group-{i // 2}") for i in range(12)]
            write_manifest(manifest, rows)
            output = Path(temp) / "split.csv"
            result = run_tool(SPLITTER, str(manifest), "--seed", "89", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            with output.open(newline="", encoding="utf-8") as handle:
                assigned = list(csv.DictReader(handle))
            group_splits: dict[str, set[str]] = {}
            for row in assigned:
                group_splits.setdefault(row["source_group_id"], set()).add(row["split"])
            self.assertTrue(all(len(splits) == 1 for splits in group_splits.values()))
            self.assertEqual({row["split"] for row in assigned}, {"train", "validation", "test"})

    def test_auditor_detects_cross_split_group_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = root / "sample.jpg"
            image.write_bytes(b"approved fixture")
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            rows = []
            for split in ("train", "test"):
                row = {field: "" for field in FIELDS}
                row.update({
                    "image_path": "sample.jpg", "source_url": "https://example.org/data",
                    "license_name": "Test licence", "license_url": "https://example.org/license",
                    "license_status": "approved", "source_group_id": "same-scene",
                    "sha256": digest, "label_status": "human_verified",
                    "label_reviewer": "qualified reviewer", "ground_truth_basis": "verified fixture",
                    "split": split,
                })
                rows.append(row)
            manifest = root / "manifest.csv"
            write_manifest(manifest, rows)
            result = run_tool(AUDITOR, str(manifest), "--root", str(root), "--require-ready")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("appears in multiple splits", result.stdout)

    def test_auditor_accepts_complete_verified_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = root / "sample.jpg"
            image.write_bytes(b"verified fixture")
            row = {field: "" for field in FIELDS}
            row.update({
                "image_path": "sample.jpg",
                "source_url": "https://example.org/data",
                "source_name": "test dataset",
                "dataset_version": "fixture-v1",
                "license_name": "Test licence",
                "license_url": "https://example.org/license",
                "license_status": "approved",
                "attribution": "Attribution recorded for test fixture",
                "source_group_id": "scene-1",
                "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                "label_status": "human_verified",
                "label_reviewer": "qualified reviewer",
                "ground_truth_basis": "independently verified fixture",
                "split": "test",
            })
            manifest = root / "manifest.csv"
            write_manifest(manifest, [row])
            result = run_tool(AUDITOR, str(manifest), "--root", str(root), "--require-ready")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Errors: 0", result.stdout)
            self.assertIn("Rows passing basic verified-label/hash/split checks: 1", result.stdout)

    def test_auditor_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root.parent / (root.name + "-outside.jpg")
            outside.write_bytes(b"outside")
            try:
                row = {field: "" for field in FIELDS}
                row.update({
                    "image_path": "../" + outside.name, "source_url": "https://example.org/data",
                    "license_name": "Test licence", "license_url": "https://example.org/license",
                    "license_status": "approved", "source_group_id": "group-1",
                    "sha256": hashlib.sha256(outside.read_bytes()).hexdigest(),
                    "label_status": "human_verified", "label_reviewer": "reviewer",
                    "ground_truth_basis": "verified fixture", "split": "test",
                })
                manifest = root / "manifest.csv"
                write_manifest(manifest, [row])
                result = run_tool(AUDITOR, str(manifest), "--root", str(root), "--require-ready")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("escapes dataset root", result.stdout)
            finally:
                outside.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
