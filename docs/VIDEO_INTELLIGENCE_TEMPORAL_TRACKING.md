# PUI89 Video Intelligence — Temporal Evidence Foundation

**Status:** dependency-free software scaffold added for synthetic/offline evaluation. No VideoCUPS model, pretrained weights, video decoder, detector, segmentation network, optical-flow model or depth model is included. No real flood video has been evaluated.

## Research inspiration and scope

This work is inspired by research directions in unsupervised video panoptic segmentation, including temporal consistency and cautious use of pseudo-labels. It is an independent PUI89 contract/evaluation scaffold; it does not reproduce VideoCUPS, copy its implementation, or claim comparable performance.

The foundation separates:
- **Semantic evidence:** what category a pixel region is believed to represent (for example, water, road or person).
- **Instance evidence:** which individual object an upstream system associates with a persistent track ID.
- **Temporal evidence:** when each frame and observation occurred, whether tracks persist, and whether labels conflict or frames are missing.
- **Review evidence:** whether a generated pseudo-label has been explicitly reviewed and approved.

## Implemented files

- \`pui89_autonomy/video_intelligence.py\`
  - \`VideoFrame\`: frame index, timestamp, source identifier and SHA-256, image dimensions.
  - \`PanopticSegment\`: semantic label/kind, mask digest, confidence, optional instance ID and review state.
  - \`VideoFrameEvidence\`: frame plus segment records; rejects duplicate instance IDs in one frame.
  - \`TemporalVideoLedger\`: ordered frame ledger, supplied-track continuity, frame-gap records and label-conflict events.
  - \`assess_pseudo_label\`: requires explicit human approval and a confidence threshold before a label can enter offline evaluation.
  - \`build_video_evidence_report\`: deterministic summary with limitations and a no-hardware-actuation assertion.
- \`tests/test_video_intelligence.py\`: standard-library unittest coverage for metadata validation, identity continuity, frame gaps, label conflicts, ordering, pseudo-label review and deterministic reports.

## Safety and evidence boundaries

- Track IDs and mask hashes are supplied by an upstream detector/tracker/segmenter. This module does not verify their visual correctness or associate objects between frames.
- A changed class label on one track is a review event, not proof of an identity switch.
- A missing frame interval is recorded as a gap; it is not interpreted as disappearance, death, rescue status or a new identity.
- Identity-switch metrics require independently reviewed ground-truth tracks and are not calculated here.
- Generated pseudo-labels remain in review until a human explicitly approves them. Approval permits offline evaluation only.
- No label, track, confidence score or report authorizes rescue dispatch, route clearance, physical motion or hardware actuation.
- A mask digest provides an integrity reference only; it does not prove that the referenced mask exists or is accurate.

## Zero-cost implementation policy

The module uses only the Python standard library. It does not download video, datasets, pretrained models or checkpoints; install packages; call hosted APIs; create cloud compute; or issue robot commands. The existing project dependency declarations are not changed by this feature.

Before considering optional VideoCUPS or other pretrained components, separately verify the exact repository, code licence, checkpoint licence, third-party dependencies, dataset terms, model provenance, file size, RAM/VRAM/disk requirements and offline operation. Public availability is not blanket permission for reuse or commercial deployment.

## Evaluation plan

1. Run the focused tests with an already available Python interpreter: \`python -m unittest tests.test_video_intelligence -v\` (or \`python -m unittest discover -s tests -p "test_video_intelligence.py" -v\`).
2. Add synthetic sequences with occlusion, temporary track loss, label ambiguity, duplicate IDs, stale timestamps and source-hash changes.
3. For identity-switch and segmentation metrics, use a reviewed dataset split and a documented ground-truth protocol; report sample counts and metric definitions.
4. Add a video decoder/vision adapter only after licence and resource review. Keep the current evidence contracts independent of any specific model.
5. Integrate validated observations into the shared PUI89 WorldState only after a schema mapping review. Preserve uncertainty and provenance; do not let video evidence override existing safety gates.

**Current claim boundary:** this is a contract and evidence-led evaluation foundation, not a working video perception model, not a trained flood detector, and not validated rescue technology.
