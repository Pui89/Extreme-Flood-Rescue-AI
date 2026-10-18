#!/usr/bin/env python3
"""Audit a local dataset manifest without downloading data or using paid services.

Usage:
  python tools/audit_dataset_manifest.py data/manifest.csv --root ./datasets

The script never changes labels or grants licence approval. A human must review rights
and ground truth, then explicitly record license_status=approved and
label_status=human_verified in the manifest.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED = {
    "image_path", "source_url", "source_name", "dataset_version",
    "license_name", "license_url", "license_status", "attribution",
    "source_group_id", "sha256", "label_status", "label_reviewer",
    "ground_truth_basis", "split", "notes",
}
ALLOWED_SPLITS = {"train", "validation", "test"}
ALLOWED_LABEL_STATES = {"unreviewed", "review_needed", "human_verified", "excluded"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="CSV manifest path")
    parser.add_argument("--root", type=Path, default=Path("."), help="Root for image_path values")
    parser.add_argument("--require-ready", action="store_true",
                        help="Exit non-zero unless every included row has approved rights, verified labels, hashes and group split")
    args = parser.parse_args()

    if not args.manifest.is_file():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    rows: list[dict[str, str]] = []
    with args.manifest.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            print("ERROR: missing columns: " + ", ".join(sorted(missing)), file=sys.stderr)
            return 2
        rows = list(reader)

    if not rows:
        print("No image rows found. This template is not a dataset and no metrics can be computed.")
        return 1 if args.require_ready else 0

    seen_hashes: dict[str, int] = {}
    group_splits: dict[str, set[str]] = defaultdict(set)
    included = 0
    ready = 0
    for line, row in enumerate(rows, start=2):
        image_value = (row.get("image_path") or "").strip()
        if not image_value:
            warnings.append(f"line {line}: blank image_path (template/empty row)")
            continue
        if (row.get("license_status") or "").strip().lower() != "approved":
            warnings.append(f"line {line}: rights not approved; excluded from ready dataset")
            continue
        included += 1
        path = (args.root / image_value).resolve()
        try:
            path.relative_to(args.root.resolve())
        except ValueError:
            errors.append(f"line {line}: image_path escapes dataset root")
            continue
        if not path.is_file():
            errors.append(f"line {line}: image file missing: {image_value}")
            continue
        actual_hash = sha256_file(path)
        recorded_hash = (row.get("sha256") or "").strip().lower()
        if not recorded_hash or actual_hash != recorded_hash:
            errors.append(f"line {line}: SHA-256 missing or mismatched for {image_value}")
        if actual_hash in seen_hashes:
            warnings.append(f"line {line}: duplicate image content matches manifest line {seen_hashes[actual_hash]}")
        else:
            seen_hashes[actual_hash] = line

        state = (row.get("label_status") or "").strip()
        if state not in ALLOWED_LABEL_STATES:
            errors.append(f"line {line}: unknown label_status {state!r}")
        if state != "human_verified":
            warnings.append(f"line {line}: labels are not human_verified")
        for key in ("source_url", "source_name", "dataset_version", "license_name",
                    "license_url", "attribution", "source_group_id",
                    "label_reviewer", "ground_truth_basis"):
            if not (row.get(key) or "").strip():
                errors.append(f"line {line}: {key} is required for an auditable dataset")
        if not (row.get("source_group_id") or "").strip():
            errors.append(f"line {line}: source_group_id is required to audit split leakage")
        split = (row.get("split") or "").strip().lower()
        if split not in ALLOWED_SPLITS:
            errors.append(f"line {line}: split must be one of {sorted(ALLOWED_SPLITS)}")
        else:
            group = (row.get("source_group_id") or "").strip()
            if group:
                group_splits[group].add(split)

        if (state == "human_verified" and recorded_hash == actual_hash
                and split in ALLOWED_SPLITS and (row.get("source_group_id") or "").strip()
                and all((row.get(key) or "").strip() for key in
                        ("source_url", "source_name", "dataset_version", "license_name",
                         "license_url", "attribution", "label_reviewer", "ground_truth_basis"))):
            ready += 1

    for group, splits in sorted(group_splits.items()):
        if len(splits) > 1:
            errors.append(f"source_group_id {group!r} appears in multiple splits: {sorted(splits)}")

    print(f"Manifest rows: {len(rows)}")
    print(f"Rows with license_status=approved: {included}")
    print(f"Rows passing basic verified-label/hash/split checks: {ready}")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
    for item in errors:
        print("ERROR: " + item)
    for item in warnings:
        print("WARNING: " + item)
    if not included:
        print("No rights-approved image rows are ready; no training should start.")
    if args.require_ready and (errors or ready != included or not included):
        return 1
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
