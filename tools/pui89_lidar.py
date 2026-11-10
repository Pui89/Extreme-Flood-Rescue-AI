"""Dependency-free LiDAR metadata gates and deterministic terrain reference tools.

These routines validate metadata and small synthetic raster grids. They are not a
LAS/LAZ reader, GIS engine, hydrological model, flood predictor, or route-safety system.
"""
from __future__ import annotations

from datetime import datetime
import heapq
import math
import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_ALLOWED_HORIZONTAL_UNITS = {"m", "metre", "metres", "meter", "meters", "ft", "foot", "feet"}
_ALLOWED_VERTICAL_UNITS = _ALLOWED_HORIZONTAL_UNITS
_REQUIRED_METADATA = (
    "source_id",
    "source_sha256",
    "acquired_at",
    "crs",
    "horizontal_units",
    "vertical_datum",
    "vertical_units",
    "classification_scheme",
)


def validate_lidar_metadata(
    metadata: Mapping[str, Any],
    coordinates: Iterable[Sequence[float]] | None = None,
) -> dict[str, Any]:
    """Return a fail-closed validation report; never infer missing CRS or units."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(metadata, Mapping):
        return {
            "status": "INVALID",
            "errors": ["metadata must be a mapping"],
            "warnings": [],
        }

    for key in _REQUIRED_METADATA:
        value = metadata.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing_or_invalid:{key}")

    digest = metadata.get("source_sha256")
    if isinstance(digest, str) and digest.strip() and not _SHA256_RE.fullmatch(digest.strip()):
        errors.append("invalid:source_sha256")

    timestamp = metadata.get("acquired_at")
    if isinstance(timestamp, str) and timestamp.strip():
        try:
            parsed = datetime.fromisoformat(timestamp.strip().replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                errors.append("timezone_required:acquired_at")
        except ValueError:
            errors.append("invalid:acquired_at")

    for key, allowed in (
        ("horizontal_units", _ALLOWED_HORIZONTAL_UNITS),
        ("vertical_units", _ALLOWED_VERTICAL_UNITS),
    ):
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            if value.strip().lower() not in allowed:
                errors.append(f"unsupported:{key}")
    if isinstance(metadata.get("crs"), str) and metadata["crs"].strip():
        crs = metadata["crs"].strip()
        if not (re.search(r"(EPSG:\s*\d+|urn:ogc:def:crs:|GEOGCS\[|PROJCRS\[)", crs, re.I)):
            warnings.append("crs_format_unverified:retain_source_definition")
    if isinstance(metadata.get("vertical_datum"), str) and metadata["vertical_datum"].strip():
        if metadata["vertical_datum"].strip().lower() in {"unknown", "n/a", "na", "none"}:
            errors.append("unknown:vertical_datum")

    point_count = 0
    if coordinates is not None:
        try:
            for index, point in enumerate(coordinates):
                point_count += 1
                if not isinstance(point, Sequence) or isinstance(point, (str, bytes)) or len(point) < 3:
                    errors.append(f"invalid_coordinate_triplet:{index}")
                    continue
                for axis, value in zip(("x", "y", "z"), point[:3]):
                    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                        errors.append(f"non_finite_or_non_numeric:{index}:{axis}")
        except TypeError:
            errors.append("coordinates_not_iterable")
        if point_count == 0:
            errors.append("empty_coordinates")

    return {
        "status": "VALID" if not errors else "INVALID",
        "errors": errors,
        "warnings": warnings,
        "point_count_checked": point_count if coordinates is not None else None,
        "evidence_status": "OBSERVED" if not errors else "UNKNOWN",
        "processing_mode": "METADATA_GATE_ONLY",
        "execution_authorized": False,
    }


def _validate_grid(
    grid: Sequence[Sequence[float | None]],
) -> tuple[int, int]:
    if not isinstance(grid, Sequence) or not grid:
        raise ValueError("grid must be a non-empty rectangular sequence")
    if any(not isinstance(row, Sequence) or isinstance(row, (str, bytes)) for row in grid):
        raise ValueError("each grid row must be a sequence")
    width = len(grid[0])
    if width == 0 or any(len(row) != width for row in grid):
        raise ValueError("grid must be rectangular and non-empty")
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError(f"grid[{row_index}][{col_index}] must be finite or None")
    return len(grid), width


def slope_degrees(
    elevation: Sequence[Sequence[float | None]],
    cell_size_x: float = 1.0,
    cell_size_y: float = 1.0,
) -> list[list[float | None]]:
    """Central-difference slope; border and NoData-neighbour cells return None."""
    rows, cols = _validate_grid(elevation)
    for name, size in (("cell_size_x", cell_size_x), ("cell_size_y", cell_size_y)):
        if isinstance(size, bool) or not isinstance(size, (int, float)) or not math.isfinite(size) or size <= 0:
            raise ValueError(f"{name} must be finite and positive")

    result: list[list[float | None]] = [[None] * cols for _ in range(rows)]
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            neighbours = (
                elevation[r][c - 1], elevation[r][c + 1],
                elevation[r - 1][c], elevation[r + 1][c],
            )
            if any(value is None for value in neighbours):
                continue
            dz_dx = (float(elevation[r][c + 1]) - float(elevation[r][c - 1])) / (2 * cell_size_x)
            dz_dy = (float(elevation[r + 1][c]) - float(elevation[r - 1][c])) / (2 * cell_size_y)
            result[r][c] = math.degrees(math.atan(math.hypot(dz_dx, dz_dy)))
    return result


def d8_flow_direction(
    elevation: Sequence[Sequence[float | None]],
    cell_size_x: float = 1.0,
    cell_size_y: float = 1.0,
) -> list[list[tuple[int, int] | None]]:
    """Choose the neighbour with greatest positive downhill gradient (D8).

    Ties use a fixed neighbour order. Flats, pits, and NoData cells have no
    downstream direction. This simple reference does not resolve flats or fill sinks.
    """
    rows, cols = _validate_grid(elevation)
    for name, size in (("cell_size_x", cell_size_x), ("cell_size_y", cell_size_y)):
        if isinstance(size, bool) or not isinstance(size, (int, float)) or not math.isfinite(size) or size <= 0:
            raise ValueError(f"{name} must be finite and positive")

    neighbours = (
        (-1, -1), (-1, 0), (-1, 1), (0, -1),
        (0, 1), (1, -1), (1, 0), (1, 1),
    )
    result: list[list[tuple[int, int] | None]] = [[None] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            current = elevation[r][c]
            if current is None:
                continue
            best_gradient = 0.0
            best_step: tuple[int, int] | None = None
            for dr, dc in neighbours:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                neighbour = elevation[nr][nc]
                if neighbour is None:
                    continue
                distance = math.hypot(dr * cell_size_y, dc * cell_size_x)
                gradient = (float(current) - float(neighbour)) / distance
                if gradient > best_gradient:
                    best_gradient = gradient
                    best_step = (dr, dc)
            result[r][c] = best_step
    return result


def flow_accumulation(
    flow_direction: Sequence[Sequence[tuple[int, int] | None]],
) -> list[list[int | None]]:
    """Count upstream cells including each valid cell; NoData is represented by None.

    Flow directions must point to an adjacent in-grid cell. A deterministic
    topological traversal rejects cycles rather than returning partial totals.
    """
    rows, cols = _validate_grid(
        [[0.0 if step is not None else None for step in row] for row in flow_direction]
    )
    accumulation: list[list[int | None]] = [
        [None if step is None and flow_direction[r][c] is None else 1 for c, step in enumerate(row)]
        for r, row in enumerate(flow_direction)
    ]
    # A None direction can mean either a valid sink or NoData. Callers can mark
    # NoData by supplying the parallel mask through None is ambiguous, so this
    # reference treats every None as a valid terminal cell.
    downstream_count = [[0] * cols for _ in range(rows)]
    downstream: dict[tuple[int, int], tuple[int, int]] = {}
    for r in range(rows):
        for c in range(cols):
            step = flow_direction[r][c]
            if step is None:
                continue
            if not isinstance(step, tuple) or len(step) != 2 or any(type(v) is not int for v in step):
                raise ValueError(f"invalid flow direction at ({r}, {c})")
            nr, nc = r + step[0], c + step[1]
            if abs(step[0]) > 1 or abs(step[1]) > 1 or step == (0, 0) or not (0 <= nr < rows and 0 <= nc < cols):
                raise ValueError(f"flow direction leaves grid or is not adjacent at ({r}, {c})")
            downstream[(r, c)] = (nr, nc)
            downstream_count[nr][nc] += 1

    queue = [(r, c) for r in range(rows) for c in range(cols) if downstream_count[r][c] == 0]
    heapq.heapify(queue)
    processed = 0
    while queue:
        r, c = heapq.heappop(queue)
        processed += 1
        target = downstream.get((r, c))
        if target is None:
            continue
        nr, nc = target
        accumulation[nr][nc] += accumulation[r][c]
        downstream_count[nr][nc] -= 1
        if downstream_count[nr][nc] == 0:
            heapq.heappush(queue, (nr, nc))
    if processed != rows * cols:
        raise ValueError("flow direction contains a cycle")
    return accumulation
