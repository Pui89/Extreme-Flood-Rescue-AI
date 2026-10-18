#!/usr/bin/env python3
"""Create leakage-aware train/validation/test assignments by source group.

Only assigns rows whose licence is approved and whose labels are human_verified.
It never creates labels, and it must not replace official benchmark splits.
"""
from __future__ import annotations
import argparse, csv, random
from collections import defaultdict
from pathlib import Path

REQUIRED = {"source_group_id","license_status","label_status","split","source_url","license_url","ground_truth_basis"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest",type=Path)
    p.add_argument("--seed",type=int,default=89)
    p.add_argument("--train",type=float,default=.70)
    p.add_argument("--validation",type=float,default=.15)
    p.add_argument("--test",type=float,default=.15)
    p.add_argument("--output",type=Path,default=None)
    a=p.parse_args()
    if abs(a.train+a.validation+a.test-1.0)>1e-8 or min(a.train,a.validation,a.test)<=0:
        p.error("train, validation and test fractions must be positive and sum to 1")
    if not a.manifest.is_file(): p.error(f"manifest not found: {a.manifest}")
    with a.manifest.open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f); fields=reader.fieldnames or []
        missing=REQUIRED-set(fields)
        if missing: p.error("missing columns: "+", ".join(sorted(missing)))
        rows=list(reader)
    if not rows: p.error("manifest contains no image rows")
    for i,row in enumerate(rows,start=2):
        if (row.get("license_status") or "").strip().lower() != "approved":
            p.error(f"line {i}: licence is not approved; review rights before splitting")
        if (row.get("label_status") or "").strip() != "human_verified":
            p.error(f"line {i}: labels are not human_verified")
        for key in ("source_group_id","source_url","license_url","ground_truth_basis"):
            if not (row.get(key) or "").strip(): p.error(f"line {i}: {key} is required")
        if (row.get("split") or "").strip():
            p.error(f"line {i}: split already set; refusing to overwrite existing split")
    groups=defaultdict(list)
    for i,row in enumerate(rows): groups[row["source_group_id"].strip()].append(i)
    names=list(groups); random.Random(a.seed).shuffle(names)
    total=len(rows); targets=[a.train*total,(a.train+a.validation)*total]
    counts=[0,0,0]; mapping={}
    for group in names:
        n=len(groups[group])
        # Assign whole groups to the currently most-underfilled target partition.
        deficits=[targets[0]-counts[0],targets[1]-counts[0]-counts[1],total-counts[0]-counts[1]-counts[2]]
        # Normalize by desired partition size, then assign to the largest relative deficit.
        desired=[a.train*total,a.validation*total,a.test*total]
        idx=max(range(3),key=lambda j:(desired[j]-counts[j])/max(desired[j],1))
        mapping[group]=("train","validation","test")[idx]
        counts[idx]+=n
    for row in rows: row["split"]=mapping[row["source_group_id"].strip()]
    output=a.output or a.manifest.with_name(a.manifest.stem+"_split.csv")
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    split_groups=defaultdict(set)
    for row in rows: split_groups[row["split"]].add(row["source_group_id"].strip())
    assert not (split_groups["train"] & split_groups["validation"])
    assert not (split_groups["train"] & split_groups["test"])
    assert not (split_groups["validation"] & split_groups["test"])
    print(f"Rows: {total}; unique groups: {len(groups)}; seed: {a.seed}")
    print(f"Output: {output}")
    print("Rows by split: "+", ".join(f"{s}={sum(r['split']==s for r in rows)}" for s in ("train","validation","test")))
    print("Group leakage check: PASS (groups kept intact)")
    print("Note: proportions are approximate when source groups differ in size; inspect class balance and preserve official splits where provided.")

if __name__=="__main__": main()
