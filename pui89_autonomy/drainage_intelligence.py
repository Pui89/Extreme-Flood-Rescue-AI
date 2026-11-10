"""Dependency-free LiDAR/terrain drainage intelligence; no raw classifier or robot control."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from hashlib import sha256
import json, math
from typing import Any, Iterable, Sequence

SUPPORTED_CLASSES = {"drainage_inlet", "drainage_channel", "culvert", "roadside_drain", "outfall", "stormwater_structure"}
SCHEMA_VERSION = "pui89.spatial-drainage.v1"

@dataclass(frozen=True)
class ClassifiedPoint:
    x: float
    y: float
    z: float
    class_label: str
    confidence: float
    source_id: str

@dataclass(frozen=True)
class DrainageFeature:
    feature_id: str
    feature_type: str
    x: float
    y: float
    z: float
    confidence: float
    source_ids: tuple[str, ...]
    review_required: bool = True

@dataclass(frozen=True)
class TerrainCell:
    row: int
    col: int
    elevation_m: float
    slope_deg: float
    downslope_neighbor: tuple[int, int] | None
    is_local_low: bool

def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"{name} must be a finite number")
    return float(value)

def validate_point(point: ClassifiedPoint) -> ClassifiedPoint:
    if not isinstance(point, ClassifiedPoint):
        raise ValueError("each point must be a ClassifiedPoint")
    confidence = _number(point.confidence, "confidence")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    if point.class_label not in SUPPORTED_CLASSES:
        raise ValueError("unsupported or unknown class_label")
    if not isinstance(point.source_id, str) or not point.source_id.strip():
        raise ValueError("source_id must be a non-empty string")
    return ClassifiedPoint(_number(point.x, "x"), _number(point.y, "y"), _number(point.z, "z"),
                           point.class_label, confidence, point.source_id.strip())

def extract_drainage_features(points: Iterable[ClassifiedPoint], *, minimum_confidence: float = 0.5) -> list[DrainageFeature]:
    threshold = _number(minimum_confidence, "minimum_confidence")
    if not 0 <= threshold <= 1:
        raise ValueError("minimum_confidence must be between 0 and 1")
    result = []
    for index, point in enumerate(validate_point(p) for p in points):
        if point.confidence < threshold:
            continue
        raw = json.dumps(asdict(point), sort_keys=True, separators=(",", ":"))
        digest = sha256(raw.encode()).hexdigest()[:12]
        result.append(DrainageFeature(f"drain-{index:05d}-{digest}", point.class_label,
                                      point.x, point.y, point.z, point.confidence,
                                      (point.source_id,)))
    return result

def analyze_dem(elevation_grid: Sequence[Sequence[float]], *, cell_size_m: float) -> list[TerrainCell]:
    cell = _number(cell_size_m, "cell_size_m")
    if cell <= 0:
        raise ValueError("cell_size_m must be greater than zero")
    if not isinstance(elevation_grid, Sequence) or len(elevation_grid) < 2:
        raise ValueError("elevation_grid must contain at least two rows")
    width = len(elevation_grid[0]) if isinstance(elevation_grid[0], Sequence) else 0
    if width < 2 or any(not isinstance(row, Sequence) or len(row) != width for row in elevation_grid):
        raise ValueError("elevation_grid must be a rectangular grid at least 2x2")
    grid = [[_number(v, "elevation") for v in row] for row in elevation_grid]
    height, output = len(grid), []
    for r in range(height):
        for c in range(width):
            l, rt = max(0, c-1), min(width-1, c+1)
            u, d = max(0, r-1), min(height-1, r+1)
            dx = (grid[r][rt]-grid[r][l])/(max(1, rt-l)*cell)
            dy = (grid[d][c]-grid[u][c])/(max(1, d-u)*cell)
            slope = math.degrees(math.atan(math.hypot(dx, dy)))
            neighbours = [(rr, cc) for rr in range(max(0,r-1), min(height,r+2))
                          for cc in range(max(0,c-1), min(width,c+2)) if (rr,cc)!=(r,c)]
            lower = [(rr,cc) for rr,cc in neighbours if grid[rr][cc] < grid[r][c]]
            target = min(lower, key=lambda rc: (grid[rc[0]][rc[1]], rc)) if lower else None
            low = all(grid[r][c] <= grid[rr][cc] for rr,cc in neighbours)
            output.append(TerrainCell(r,c,grid[r][c],slope,target,low))
    return output

def build_drainage_report(points: Iterable[ClassifiedPoint], elevation_grid: Sequence[Sequence[float]], *,
                          cell_size_m: float, minimum_confidence: float = 0.5,
                          source_dataset_id: str) -> dict[str, Any]:
    if not isinstance(source_dataset_id, str) or not source_dataset_id.strip():
        raise ValueError("source_dataset_id must be a non-empty string")
    validated = [validate_point(p) for p in points]
    features = extract_drainage_features(validated, minimum_confidence=minimum_confidence)
    terrain = analyze_dem(elevation_grid, cell_size_m=cell_size_m)
    report = {
        "schema_version": SCHEMA_VERSION, "status": "REVIEW_REQUIRED",
        "evidence_type": "SUPPLIED_CLASSIFIED_POINTS_AND_SYNTHETIC_DEM",
        "source_dataset_id": source_dataset_id.strip(),
        "features": [asdict(f) for f in features], "terrain": [asdict(c) for c in terrain],
        "summary": {
            "candidate_feature_count": len(features),
            "feature_counts_by_type": {k: sum(f.feature_type == k for f in features) for k in sorted(SUPPORTED_CLASSES)},
            "local_low_cell_count": sum(c.is_local_low for c in terrain),
            "terrain_cell_count": len(terrain),
            "flow_path_interpretation": "steepest-neighbour terrain indicator only",
        },
        "limitations": [
            "Class labels are supplied upstream; raw LiDAR classification is not performed.",
            "A candidate does not prove an asset exists or functions.",
            "DEM slope and downslope neighbours are not hydrological or hydraulic simulation.",
            "Vegetation, buildings, water, occlusion, survey density, vertical datum and DEM resolution can alter results.",
            "Candidate features require human verification against authoritative GIS, field survey or asset records.",
            "This report does not predict flooding or establish a safe rescue route.",
        ],
        "decision_authority": "HUMAN_REVIEW_ONLY", "physical_safety_validated": False,
        "robot_commands_emitted": False,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False)
    report["integrity_sha256"] = sha256(canonical.encode()).hexdigest()
    return report

def verify_drainage_report(report: dict[str, Any]) -> bool:
    if not isinstance(report, dict) or not isinstance(report.get("integrity_sha256"), str):
        return False
    if report.get("schema_version") != SCHEMA_VERSION or report.get("physical_safety_validated") is not False or report.get("robot_commands_emitted") is not False:
        return False
    payload = {k:v for k,v in report.items() if k != "integrity_sha256"}
    try:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError):
        return False
    return sha256(canonical.encode()).hexdigest() == report["integrity_sha256"]
