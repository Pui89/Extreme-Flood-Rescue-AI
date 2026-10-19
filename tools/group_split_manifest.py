#!/usr/bin/env python3
"""Create leakage-aware train/validation/test assignments by source group.

Only assigns rows whose licence is approved and whose labels are human_verified.
It never creates labels, and it must not replace official benchmark splits.
"""
from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path

REQUIRED = {
    "source_group_id", "license_status", "label_status", "split",
    "source_url", "license_url", "ground_truth_basis",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--seed", type=int, default=89)
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--validation", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    if abs(args.train + args.validation + args.test - 1.0) > 1e-8 or min(
        args.train, args.validation, args.test
    ) <= 0:
        parser.error("train, validation and test fractions must be positive and sum to 1")
    if not args.manifest.is_file():
        parser.error(f"manifest not found: {args.manifest}")
    with args.manifest.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        missing = REQUIRED - set(fields)
        if missing:
            parser.error("missing columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    if not rows:
        parser.error("manifest contains no image rows")
    for line, row in enumerate(rows, start=2):
        if (row.get("license_status") or "").strip().lower() != "approved":
            parser.error(f"line {line}: licence is not approved; review rights before splitting")
        if (row.get("label_status") or "").strip() != "human_verified":
            parser.error(f"line {line}: labels are not human_verified")
        for key in ("source_group_id", "source_url", "license_url", "ground_truth_basis"):
            if not (row.get(key) or "").strip():
                parser.error(f"line {line}: {key} is required")
        if (row.get("split") or "").strip():
            parser.error(f"line {line}: split already set; refusing to overwrite existing split")

    groups: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(rows):
        groups[row["source_group_id"].strip()].append(index)
    if len(groups) < 3:
        parser.error(
            "at least three distinct source_group_id values are required to populate "
            "train, validation and test without splitting a source group"
        )

    group_names = list(groups)
    random.Random(args.seed).shuffle(group_names)
    total = len(rows)
    desired = [args.train * total, args.validation * total, args.test * total]
    counts = [0, 0, 0]
    mapping: dict[str, str] = {}
    split_names = ("train", "validation", "test")
    for group in group_names:
        size = len(groups[group])
        index = max(
            range(3),
            key=lambda split_index: (
                desired[split_index] - counts[split_index]
            ) / max(desired[split_index], 1),
        )
        mapping[group] = split_names[index]
        counts[index] += size

    for row in rows:
        row["split"] = mapping[row["source_group_id"].strip()]
    output = args.output or args.manifest.with_name(args.manifest.stem + "_split.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    split_groups: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        split_groups[row["split"]].add(row["source_group_id"].strip())
    assert not (split_groups["train"] & split_groups["validation"])
    assert not (split_groups["train"] & split_groups["test"])
    assert not (split_groups["validation"] & split_groups["test"])
    print(f"Rows: {total}; unique groups: {len(groups)}; seed: {args.seed}")
    print(f"Output: {output}")
    print(
        "Rows by split: "
        + ", ".join(
            f"{split}={sum(row['split'] == split for row in rows)}"
            for split in split_names
        )
    )
    print("Group leakage check: PASS (groups kept intact)")
    print(
        "Note: proportions are approximate when source groups differ in size; "
        "inspect class balance and preserve official splits where provided."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
