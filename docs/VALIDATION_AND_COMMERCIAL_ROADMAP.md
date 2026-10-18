# Flood Rescue AI — validation and commercial roadmap

## Current baseline
The prototype provides an API/dashboard for manually entered illustrative sensor observations and a deterministic software workflow. The documented end-to-end demo uses synthetic observations. It is not a trained flood/person detector, hydrodynamic model, validated collision checker or field-tested rescue robot.

## Dataset and annotation
Keep tasks separate: person detection (bounding boxes, visibility/occlusion tags), flood segmentation (pixel masks), hazard/debris detection (separate class definitions), and localization/mapping (compare predictions with independently measured ground truth). Record source, licence/permission, event/location group, modality, annotation version, reviewer and privacy restrictions. Split by event/location/source to reduce leakage.

## Training and evaluation gates
1. Choose one task and a compatible, licensed dataset.
2. Review labels and remove duplicate/near-duplicate leakage across splits.
3. Train a local baseline and log seed, commit, packages, device, split counts, configuration, elapsed time and checkpoint SHA-256.
4. Freeze the test set. Report detection precision/recall/F1/AP or segmentation IoU/Dice, latency, memory, class counts and stratified failure cases as appropriate.
5. Test rain, darkness, reflections, blur, occlusion, low resolution, missing modalities and timestamp skew.
6. Run software tests and fault injection separately from model metrics.
7. Test navigation in a physics-backed simulator with a validated robot model and independently tested collision/safe-stop logic.
8. Only then consider controlled, authorized hardware trials with qualified safety supervision.

## Minimum benchmark report
Include task definition; dataset provenance/licence; annotation protocol; train/validation/test counts; split-generation method; code commit; model/checkpoint checksum; inference settings and threshold; hardware/software versions; class-wise metrics; latency; failure examples; limitations; and exact reproduction command. Do not publish a number until it is generated from predictions on the frozen test set.

## Product readiness
Potential early offer: research collaboration, simulation evaluation, data/benchmark partnership or feasibility study. Do not market the project as a field-ready autonomous rescue robot. Deployment requires independent safety review, agency authorization, privacy/security review, robust communications and safe-stop behavior, measured detection/mapping performance, operator procedures, field trials and agreed acceptance criteria.

## Zero-cost-first rule
Prefer local/open-source tooling and simulation. Do not add paid inference APIs, hosted GPU subscriptions or automatic model downloads without explicit review. Check dataset and checkpoint licences separately; free download does not automatically mean commercial reuse is permitted.
