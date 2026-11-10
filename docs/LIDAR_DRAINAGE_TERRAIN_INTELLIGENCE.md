# LiDAR Drainage & Terrain Intelligence

**Status:** architecture plus initial dependency-free software reference tools. The metadata gate and small synthetic-grid terrain functions are implemented on a feature branch; tests are added but have not yet been executed. No LAS/LAZ ingestion, drainage detection, hydrological model, LiDAR survey, or field validation is claimed.

## Purpose

Turn georeferenced, classified 3D point-cloud data and supporting GIS layers into traceable terrain and drainage evidence for flood situational awareness and rescue-route planning.

This extends the existing RGB-D/LiDAR 3D world model. It is a terrain/infrastructure evidence layer, not a standalone flood predictor.

## Processing pipeline

1. **Ingest and preserve** — accept LAS/LAZ or an explicitly documented interchange format through an optional, locally installed reader. Record source filename, SHA-256, CRS/EPSG, horizontal/vertical units and datum, coordinate epoch if relevant, acquisition time, sensor/platform, point density, classification scheme, processing software/version and licence/provenance. Preserve the original file unchanged.
2. **Quality gate** — reject or quarantine missing CRS/units, invalid coordinates, unsupported classification codes, non-finite elevations, implausible extents, duplicate/empty inputs and incompatible vertical datums. Report point density, gaps, scan angle and classification confidence when available. Never silently reproject or reinterpret units.
3. **Class-aware surface generation** — derive a ground-only terrain surface (DTM) separately from surface/structure returns (DSM or object layer). Keep water, bridge decks, buildings, vegetation, road surfaces and unclassified points distinct where the source scheme supports them. Do not assume a classification label is correct merely because it exists.
4. **Terrain analysis** — derive elevation, slope, aspect, local relief, depressions, flow direction and flow accumulation using a documented method and cell size. Record NoData handling, edge effects, depression conditioning/breach/fill choices and sensitivity to resolution. Keep the unconditioned surface for audit.
5. **Drainage evidence extraction** — combine terrain-derived candidates with mapped assets, road/bridge layers, imagery and field-survey records. Candidate classes: open channel, roadside ditch, inlet/grate, culvert portal, outfall, stormwater structure and unknown drainage feature. Store each as a candidate with geometry, source evidence, confidence, uncertainty, review status and provenance.
6. **Hydrology/hydraulics interface** — export terrain and candidate drainage network as GIS-ready layers for a separately configured hydrological/hydraulic model. Rainfall, catchment boundaries, infiltration/land cover, channel roughness, structure dimensions/condition, downstream boundary conditions and time series must be supplied and quality checked by the responsible analyst.
7. **Flood-rescue world-state integration** — publish versioned, timestamped terrain/drainage observations into the shared world-state contract. Attach source hashes, CRS, vertical datum, resolution, acquisition time, confidence and stale-data status. The planner may use these as advisory map constraints; they do not authorize motion or establish a safe route.
8. **Human review and reporting** — distinguish observed, inferred, unknown, stale and field-verified features. Produce a review queue and machine-readable evidence report; retain reviewer, decision, timestamp and reason.

## Important detection limits

- Airborne/topographic LiDAR can reveal terrain depressions, open channels, embankments and visible surface structures when point density, scan geometry and classification are adequate.
- It generally cannot establish the internal path, diameter, blockage, invert level or condition of a buried/covered culvert from surface returns alone. Culvert portals may be occluded or confused with shadows, vegetation and other openings.
- Drainage inlets, grates and outfalls require suitable resolution and visibility; many need orthophotos, engineering asset records, mobile/terrestrial surveys or field inspection.
- Water surfaces, rain, fog, vegetation, reflective materials, bridges and occlusion can create gaps or misleading returns. Missing evidence is not evidence that a drainage feature is absent.
- A DEM-derived flow path is a terrain-based hypothesis. It is not measured flow, a verified drainage connection, or a hydraulic simulation.
- LiDAR classification alone does not predict flood extent, depth, timing, velocity or rescue feasibility.

## Candidate data contracts

Each point-cloud/terrain input should carry:

- `source_id`, `source_sha256`, `acquired_at`, `crs`, `horizontal_units`, `vertical_datum`, `vertical_units`
- `classification_scheme`, `processing_method`, `software_versions`, `resolution_m`, `quality_flags`
- `evidence_status`: `OBSERVED`, `INFERRED`, `UNKNOWN`, `STALE` or `FIELD_VERIFIED`

Each drainage candidate should carry:

- stable candidate ID and geometry reference;
- candidate type and detection method;
- source point-cloud/layer hashes;
- confidence and uncertainty (not confidence alone);
- visibility/occlusion and quality flags;
- field-review state, reviewer and review timestamp;
- explicit unknown fields for dimensions, connectivity, blockage and condition until measured.

Use the existing shared PUI89 Observation/WorldState and evidence-report contracts rather than creating a parallel, project-only world model. Schema mapping must be reviewed against the current shared-core version before implementation.

## Evaluation plan

Build deterministic synthetic fixtures first; do not require downloads, paid APIs, cloud compute or new dependencies.

| Test group | Required checks |
|---|---|
| CRS and units | missing/invalid CRS, feet/metres mismatch, vertical datum mismatch, coordinate transform provenance |
| Point-cloud quality | empty input, NaN/Inf, duplicates, sparse coverage, outliers, classification gaps |
| Terrain | known planar slopes, pits, ridges, NoData edges, resolution sensitivity |
| Flow analysis | hand-constructed small grids with known downslope paths and accumulation; flat areas and sinks |
| Drainage candidates | visible channel vs road ditch ambiguity, occlusion, false candidate rejection, unknown class retention |
| Culvert limits | no automatic assertion of hidden connectivity, diameter, blockage or condition without independent evidence |
| Robustness | noise, missing tiles, stale layers, conflicting sources, changed CRS and incomplete metadata |
| Evidence integrity | source hashes, deterministic outputs, configuration/version capture, report schema validation |
| Safety integration | stale/uncertain map data cannot clear a route; planner output remains proposal-only and deterministic safety gates retain authority |

Report precision/recall only against a reviewed reference inventory with documented spatial tolerance and class definitions. Report terrain error only against an independent reference surface. Record sample counts, coverage, confidence intervals where appropriate, software versions, parameters and random seeds. Do not invent benchmark scores.

## Integration boundaries

- **Shared AI Core:** provenance, uncertainty propagation, evidence alignment, stale/conflict handling, versioned observations and human-review status.
- **Flood Rescue AI:** terrain and drainage layers support situational awareness, catchment/route context and mission planning. Dynamic water depth/current sensing and platform operating-envelope checks remain separate.
- **Other PUI89 projects:** expose reusable geospatial contracts only after the shared-core interface is approved; do not duplicate project-specific pipelines.
- **Safety:** no direct actuator command, automatic dispatch, route clearance or rescue decision from a LiDAR-derived candidate. Unknown or conflicting critical evidence must remain unknown and trigger conservative planning/human review.

## Open-source-first resource policy

Start with standard-library contract checks and small synthetic grids. Evaluate QGIS, PDAL and GDAL only as optional, locally installed tools after checking current licence, platform compatibility, disk/RAM needs and data-format requirements. Do not install packages or download datasets/models automatically. No hosted processing, paid API, subscription or metered compute is required by this design.

## Implementation sequence

1. Review the existing shared-core schemas and repository test conventions; map fields without duplicating contracts.
2. Add dependency-free metadata validation, provenance records and small synthetic terrain fixtures.
3. Add deterministic raster-grid slope/flow reference algorithms with explicit NoData and edge semantics, or use a separately verified GIS engine behind an adapter.
4. Add drainage-candidate records and uncertainty/review workflow; never infer buried culvert internals.
5. Add report generation and regression tests, then wire advisory layers into the Flood Rescue world-state interface.
6. Run tests and publish observed results, commit, configuration and limitations. Keep field validation as a separate future gate.

**Current implementation status:** this document records the proposed design and acceptance criteria only. The processing algorithms, data ingestion, drainage detection, GIS exports and hydrological/hydraulic coupling are not implemented or validated by this change.


## Initial software implementation (feature branch)

The feature branch `feature/lidar-metadata-terrain-reference` adds:

- `tools/pui89_lidar.py`: fail-closed metadata validation for source ID/hash, timezone-aware acquisition time, CRS presence, horizontal/vertical units and datum, classification scheme, and optional finite XYZ coordinate checks.
- A dependency-free central-difference slope reference with explicit NoData-neighbour and border handling.
- A deterministic D8 steepest-descent direction reference. Flats and sinks remain terminal; no automatic sink filling or flat resolution is performed.
- A topological flow-accumulation reference with explicit optional NoData mask and cycle/invalid-edge rejection.
- `tests/test_lidar_terrain.py`: synthetic tests for metadata rejection, finite coordinates, analytic planar slope, NoData/borders, D8 routing, converging accumulation and cycle rejection.

**Verification status:** tests are authored but not yet run. Do not interpret the reference algorithms as validated GIS/hydrology. They operate on small in-memory grids only; no LAS/LAZ parser, CRS transformation, point-cloud interpolation, drainage feature detector, hydraulic model, or field validation is included. To avoid unexpected dependency downloads, the full repository CI workflow has not been triggered from this branch.
