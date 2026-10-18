# Project status and verification log — 18 October 2026

## Current state

**Stage:** local-first AI application and simulation-oriented rescue workflow prototype. It is not a field-validated rescue robot.

### Completed and evidenced
- [Latest main-branch Python test run passed](https://github.com/Pui89/Flood-Rescue-AI/actions/runs/39091991048).
- Earlier [PUI89 application CI passed](https://github.com/Pui89/Flood-Rescue-AI/actions/runs/38086003909).
- Dataset acquisition and labelling plan, manifest template, and local manifest audit tool are documented in the repository.
- Safety boundary: simulation/software checks do not authorize robot actuation or establish real-world rescue safety.

### In progress
- Prepare a provenance-complete dataset manifest and verify each source's licence and reuse terms.
- FloodNet may support flood/water/road/building scene understanding, but it does **not** supply the required person-detection labels. Do not claim person detection from flood-scene labels.
- Verify data-audit edge cases, simulation scenarios and repeatable benchmark reporting.

### Not yet demonstrated
- A fully licensed, curated dataset for all intended classes.
- Trained-model accuracy, independent-region generalization, reliable victim/person detection, navigation success under real flood conditions, or physical rescue capability.

## Next actions
1. Validate dataset manifest schema, missing files, checksums, licence/source fields, duplicate files and class coverage.
2. Review class definitions and label quality; source separate appropriately licensed person data if person detection remains in scope.
3. Add deterministic tests for audit failures and safety-gate behaviour.
4. Run simulation scenarios with fixed seeds and report success/failure counts, latency and failure cases.
5. Train/evaluate only after dataset rights and labels are checked; keep a held-out split.

## Future
- Evaluate water/flooded-road/building perception across weather, daylight, camera altitude and geographic shifts.
- Integrate ROS 2/Nav2/Gazebo only when simulation scenarios and interfaces are reproducible.
- Treat human review, uncertainty handling, communication loss, no-go zones and emergency stops as mandatory safety requirements.

## Cost and safety
Free/open-source-first; no paid inference, cloud GPU or subscription requirement. Never expose private data or deploy physical rescue behaviours based only on simulation results.