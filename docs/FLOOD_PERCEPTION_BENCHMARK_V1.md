# Flood perception benchmark v1 — segmentation and temporal tracking

**Status:** dependency-free evaluation utilities added. No segmentation or tracking model is executed by these utilities; no real flood dataset is evaluated.

## Reuse-first implementation

This increment connects three existing PUI89 foundations rather than introducing parallel AI engines:

- Flood-scene segmentation candidates and smoke-test documentation already exist in the repository (including the optional SAM 3 path). Model execution remains opt-in and is not performed by this change.
- `pui89_autonomy/video_intelligence.py` records upstream semantic/instance masks, frame metadata, supplied track IDs, gaps and label conflicts. It does not perform video decoding, segmentation or object association.
- `pui89_autonomy/world_state.py` keeps stale, low-confidence and conflicting observations explicit.
- `pui89_autonomy/experiment_report.py` records supplied metrics and provenance without inventing measurements.

## New standard-library evaluator

- `pui89_autonomy/perception_benchmark.py`
  - Semantic segmentation: confusion matrix, pixel accuracy, per-class IoU, Dice, precision and recall; supports an explicit ignore index.
  - Temporal identity continuity: identity-switch and fragmentation diagnostics from supplied ground-truth-to-prediction matches.
  - Missing classes are represented as `null`, not fabricated zero scores.
  - Invalid labels, mismatched arrays, duplicate IDs and invalid matches are rejected.
- `tests/test_perception_benchmark.py`: deterministic unit tests for metric arithmetic, ignore pixels, absent classes, identity switches, fragmentations and invalid input.

## Model adoption sequence

1. Evaluate an existing flood-segmentation baseline only after confirming the exact checkpoint revision, weight/code/dependency licences, dataset terms, local disk/RAM/compute and privacy constraints.
2. Keep water/road/building scene segmentation separate from person detection. Dataset labels must actually support each class.
3. Preserve frame-level source hashes, timestamps, camera metadata, model revision, preprocessing, mask hashes and review status.
4. Use the temporal ledger for continuity evidence; use the new continuity metrics only with independently reviewed ground-truth identities and documented spatial matching.
5. Record per-class IoU/Dice, false negatives, condition-stratified failures, identity switches, fragmentations, latency, memory, and uncertainty.
6. Keep the held-out test split frozen and separate by event/location/video source to reduce leakage.

## Required flood conditions

Day/night and low light; rain/fog; glare and reflections; clear/muddy/turbulent water; aerial and ground-level viewpoints; camera vibration and motion blur; occlusion; debris/vegetation; partial submersion; dropped frames; timestamp skew; sensor dropout; unknown scenes.

## Safety, evidence and cost boundaries

- Standard library only; no package installation, model/weight/data downloads, hosted inference, API, cloud GPU or paid service.
- No physical robot commands, rescue dispatch, route clearance or actuation.
- Segmentation masks are not calibrated flood depth. RGB appearance alone does not establish water depth, current speed or route safety.
- Tracking metrics depend on upstream matching and reviewed ground truth; they do not validate the detector or tracker.
- Unit tests validate metric code on synthetic arrays only, not AI accuracy, model quality, flood physics or rescue outcomes.
- All outputs remain research/evaluation evidence and require human review.

## Verification command

```bash
python -m unittest discover -s tests -p "test_perception_benchmark.py" -v
```

Run with an already available Python interpreter. Do not install a new interpreter or dependencies just for this check.
