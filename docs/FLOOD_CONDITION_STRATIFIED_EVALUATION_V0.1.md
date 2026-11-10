# Flood Rescue condition-stratified perception evaluation v0.1

## Purpose

This project-specific utility makes flood-scene detector evaluation harder to overstate by reporting matched detection counts separately for difficult conditions such as night, rain, glare, occlusion, debris and low visibility. It complements the existing PUI89 perception evaluator and this repository's dataset manifest, split-leakage and validation-matrix tools. It does not replace them.

## Implemented scope

- Accepts per-sample true-positive (TP), false-positive (FP) and false-negative (FN) counts produced by a separately documented matching process.
- Computes overall and per-condition precision, recall, F1 and false-negative rate.
- Requires unique sample IDs and a controlled condition vocabulary.
- Labels results as `held_out_test` only when `split=test` and `test_split_frozen=true`; otherwise reports `diagnostic_only`.
- Keeps undefined metrics as JSON null rather than silently reporting zero.
- Uses only the Python standard library and never downloads data, installs packages, runs a model, or controls hardware.

## Run

```bash
python -m unittest discover -s tests -p "test_condition_stratified_metrics.py" -v
python -m flood_robot.perception.condition_stratified_metrics path/to/matched-counts.json --output reports/flood-condition-evaluation.json
```

The JSON input must include `schema_version`, `dataset_id`, `model_id`, `model_revision`, `split`, `test_split_frozen`, and a non-empty `records` list. Each record includes a unique `sample_id`, one or more controlled `condition_tags`, and non-negative integer `tp`, `fp`, `fn` counts.

Supported condition tags: `daylight`, `dusk`, `night`, `rain`, `glare`, `occlusion`, `debris`, `low_visibility`, `camera_motion`, `missing_modality`, `stale_sensor`, `communication_loss`, `geographic_shift`, `unknown_environment`.

## Interpretation and limits

- Condition tags may overlap. A night-and-rain image contributes to both strata; do not sum stratum counts to derive the dataset total.
- TP/FP/FN counts are only as trustworthy as the ground-truth labels and the documented matching procedure. The utility does not inspect images, labels, licences or detector outputs.
- This is not a full COCO mAP evaluator, does not calculate IoU, does not measure confidence calibration, and does not evaluate tracking, depth, route safety or rescue outcomes.
- Flood-scene segmentation and person/animal detection require separate ground-truth tasks and must not be mixed into one score.
- Synthetic fixtures test calculation and input validation only. They do not establish real-image performance.
- No project-approved held-out real flood evaluation set is asserted by this implementation.

## Acceptance gate for real evaluation

Before publishing project metrics, record the exact dataset and model revisions, source/licence/attribution, human-verified ground truth, matching rule and thresholds, frozen scene/event split, condition annotation protocol, sample counts and all exclusions. Preserve difficult scenes and report false negatives by condition. Never promote a model or claim rescue readiness from this utility alone.
