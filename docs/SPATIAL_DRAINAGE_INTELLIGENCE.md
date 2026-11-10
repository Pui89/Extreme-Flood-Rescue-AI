# PUI89 Spatial Drainage Intelligence

## Status and purpose

**Status: initial dependency-free software module; synthetic/unit-test scope only.**

This capability consumes point records already classified by an upstream process and a regular digital elevation model (DEM) grid. It produces candidate drainage-asset records and simple terrain indicators for human review.

It does not implement raw LiDAR point-cloud classification, point-cloud registration, GIS asset discovery, hydrological modelling, hydraulic simulation, flood prediction, route safety certification or robot control.

## Candidate classes

Drainage inlet, drainage channel, culvert, roadside drain, outfall and stormwater structure. Class labels and confidence values are supplied inputs, not model outputs. Candidates below the confidence threshold are omitted; this is not evidence that an asset is absent.

## Terrain indicators

For a rectangular DEM grid, the module estimates slope by finite differences, chooses the steepest lower neighbour among eight adjacent cells, and flags cells no higher than any adjacent cell. These are local terrain indicators only. A local low may be a closed depression, artefact, interpolation issue or water-filled area; it is not automatically a drain or flood hotspot.

Real drainage analysis needs a validated DEM, coordinate reference system and vertical datum, sink-conditioning policy, breaklines/culvert enforcement, catchment boundaries, rainfall/runoff inputs, soil/imperviousness information and an appropriate hydrological/hydraulic model. Culvert and inlet connectivity needs authoritative asset data or field confirmation.

## Example

~~~python
from pui89_autonomy.drainage_intelligence import ClassifiedPoint, build_drainage_report, verify_drainage_report

points = [ClassifiedPoint(10, 20, 4.2, "drainage_inlet", 0.91, "synthetic-survey-01")]
dem = [[5.0, 4.8, 4.6], [4.9, 4.4, 4.2], [4.7, 4.3, 4.0]]
report = build_drainage_report(points, dem, cell_size_m=1.0, source_dataset_id="synthetic-example-v1")
assert verify_drainage_report(report)
~~~

Run focused tests:

~~~bash
python -m unittest discover -s tests -p "test_drainage_intelligence.py" -v
~~~

No paid API, cloud GPU, model download or third-party dependency is required.

## Evidence, uncertainty and safety

- Each point requires a non-empty source identifier and finite coordinates, elevation and confidence.
- Confidence is a supplied upstream score; it is not calibrated by this module.
- Every extracted feature is marked for human review.
- Reports include evidence type, source dataset ID and deterministic SHA-256 integrity checksum. The checksum detects content changes; it is not a digital signature and does not authenticate the source.
- Unsupported labels and malformed values are rejected rather than guessed.
- Reports remain REVIEW_REQUIRED; physical safety validation and robot command emission are always false.
- Do not infer drain functionality, water depth/current, flood probability, route traversability or rescue safety from this report.

## Integration roadmap

1. Validate this contract and deterministic tests.
2. Add a separately licensed point-cloud reader/classifier adapter only after format, provenance and licence review.
3. Add CRS-aware GIS exchange and surveyed asset matching.
4. Add DEM quality checks, uncertainty metadata, sink treatment and culvert breakline support.
5. Connect outputs to a validated hydrological/hydraulic model and report assumptions/calibration separately.
6. Integrate candidate map layers into Flood Rescue AI route-planning review, never as autonomous route authorization.
