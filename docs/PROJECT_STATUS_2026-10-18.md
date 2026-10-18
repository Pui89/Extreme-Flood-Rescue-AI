# Project status and verification log — 18 October 2026

## Current state

**Stage:** local-first AI application and simulation-oriented rescue workflow prototype. This is not a field-validated rescue robot.

## Successful and evidenced

- Latest known Python CI run [39096446071](https://github.com/Pui89/Flood-Rescue-AI/actions/runs/39096446071) passed across Python 3.10, 3.11 and 3.12. This validates tested software paths only.
- Repository includes dataset provenance/manifest tooling, group-aware splitting and audit tools, deterministic workflow/safety tests, API/dashboard components, and a benchmark protocol.
- The workflow is designed to require human review and does not authorize actuator commands.

## Continuing now

- Verify dataset source, licence, permitted use, checksums, duplicates, labels and class coverage.
- Keep flood/water/road/building segmentation distinct from person/victim detection: FloodNet scene labels do not by themselves establish a person-detection dataset.
- Test missing/stale/conflicting sensor inputs, uncertain observations, communication loss and fail-closed decisions.
- Keep the benchmark reproducible with fixed scenarios/seeds and record failures, not only successful runs.

## Not yet demonstrated

- A curated, licence-cleared dataset covering all intended classes.
- A trained model's independent held-out accuracy or geographic generalization.
- Reliable person/victim detection, validated water-depth estimates, real-world route safety, navigation success under flood conditions, or a physical rescue.
- A runnable and validated ROS 2/Nav2/Gazebo end-to-end rescue deployment unless separately evidenced by reproducible tests.

## Next actions

1. Audit manifests, source terms, checksums, duplicates, label quality and official split rules.
2. Choose separate tasks and metrics for flood-scene segmentation, person detection, hazard mapping and navigation.
3. Obtain appropriate lawful person-detection data if that task remains in scope; do not infer person detection from FloodNet labels.
4. Run deterministic simulation scenarios and report success/failure counts, latency, false negatives, route failures and sensor-fault behavior.
5. Only after dataset rights and labels pass review, train/evaluate a baseline on a frozen held-out split.

## Future

Evaluate weather, lighting, water levels, camera viewpoints, geographic shift and sensor loss; integrate ROS 2/Nav2/Gazebo only when the interfaces and scenarios can be reproduced; require qualified safety review before any hardware-in-the-loop or field testing.

## Corrections and boundaries

- Flood-scene segmentation is not the same task as human detection.
- Synthetic/hand-authored hypotheses and dashboard inputs are not model detections.
- A collision-check flag supplied to the workflow is not itself an independent collision checker.
- CI passing does not establish victim-detection accuracy, route safety or successful rescue.
- No physical rescue actions or actuator commands are authorized by this prototype.

## Cost boundary

Free/open-source-first. No paid inference API, cloud GPU or subscription is required by the plan. Review licences and privacy terms before using or publishing data.