#!/usr/bin/env python3
"""Create a provenance manifest template for local images; never invent labels/licences."""
from __future__ import annotations
import argparse, csv, hashlib
from pathlib import Path

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
FIELDS = ["image_path","source_url","source_name","dataset_version","license_name","license_url",
          "license_status","attribution","source_group_id","sha256","label_status",
          "label_reviewer","ground_truth_basis","split","notes"]

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("image_root", type=Path)
    p.add_argument("--output", type=Path, default=Path("data/manifest.csv"))
    p.add_argument("--source-name", default="")
    p.add_argument("--source-url", default="")
    p.add_argument("--dataset-version", default="")
    p.add_argument("--license-name", default="")
    p.add_argument("--license-url", default="")
    p.add_argument("--attribution", default="")
    p.add_argument("--group-from-parent", action="store_true",
                   help="Use each image's parent folder as source_group_id; review this choice before splitting")
    a=p.parse_args()
    root=a.image_root.resolve()
    if not root.is_dir(): p.error(f"image root not found: {root}")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    files=sorted(x for x in root.rglob("*") if x.is_file() and x.suffix.lower() in EXTS)
    seen={}
    with a.output.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for image in files:
            rel=image.relative_to(root).as_posix()
            sha=digest(image)
            duplicate=seen.get(sha,"")
            seen.setdefault(sha,rel)
            group=image.parent.relative_to(root).as_posix() if a.group_from_parent else ""
            note=f"duplicate_content_of={duplicate}" if duplicate else "label_status unreviewed; licence approval requires human review"
            w.writerow({"image_path":rel,"source_url":a.source_url,"source_name":a.source_name,
                        "dataset_version":a.dataset_version,"license_name":a.license_name,
                        "license_url":a.license_url,"license_status":"pending_review",
                        "attribution":a.attribution,"source_group_id":group,"sha256":sha,
                        "label_status":"unreviewed","label_reviewer":"","ground_truth_basis":"",
                        "split":"","notes":note})
    print(f"Images inventoried: {len(files)}")
    print(f"Manifest: {a.output}")
    print("All licence statuses remain pending_review and all labels remain unreviewed.")
    print("Review duplicate notes and source groups; do not train until rights, labels and splits are approved.")

if __name__ == "__main__": main()
