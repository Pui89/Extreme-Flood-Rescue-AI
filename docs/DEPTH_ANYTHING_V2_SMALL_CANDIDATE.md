# Depth Anything V2 Small — Flood Rescue Candidate

**Decision:** Register the official Hugging Face Transformers checkpoint as the next optional monocular relative-depth candidate.

- Model: [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf)
- Task: monocular depth estimation from a single RGB image.
- Architecture: DPT decoder with a DINOv2 backbone (per model card).
- Parameters: 24.8M.
- Checkpoint tensor type: F32 / SafeTensors (as listed by Hugging Face).
- Declared model licence: Apache-2.0 (verify the exact revision and accompanying files before redistribution).
- Model card: https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf

## Why this candidate

The Small checkpoint is a reasonable first relative-depth research candidate because it is substantially smaller than the Base and Large variants and is distributed as SafeTensors. Its output can provide a relative scene-depth cue for comparison with RGB segmentation and LiDAR evidence.

**Critical limitation:** monocular relative depth is not calibrated physical distance. It cannot measure floodwater depth, water level, current speed, safe wading depth, or the distance to an obstacle in metres. Reflections, transparent/muddy water, glare, rain, fog, night scenes, motion blur, unusual camera viewpoints and domain shift may produce misleading depth maps.

## PUI89 integration boundary

This candidate is an optional visual-evidence source only. It must not:
- replace LiDAR, radar, sonar, GNSS, surveyed terrain or calibrated range sensors;
- be converted to metres without a separately validated calibration procedure;
- be used alone to classify a route as safe or unsafe;
- trigger propulsion, navigation, deployment, contact, rescue or other physical actions.

If later integrated, the adapter must emit an observation containing:
- source ID and image/frame hash;
- frame timestamp and camera calibration/version where available;
- model ID, exact immutable model revision and checkpoint SHA-256;
- preprocessing configuration and output dimensions;
- relative-depth output reference/hash (not a fabricated metric value);
- uncertainty/quality status and explicit unknown/failure reason;
- provenance linking the observation to its input frame.

Missing frames, invalid dimensions, non-finite outputs, stale timestamps, unsupported image formats or model errors must fail closed to an explicit unknown/failure observation. Preserve conflicting evidence rather than silently overwriting it.

## Zero-cost adoption gate

This registration is documentation only. It does not download weights, install Python packages, change dependency declarations, invoke hosted inference, provision cloud compute or issue robot commands.

Before any download or runtime integration:
1. Confirm the exact model revision and record its immutable commit ID.
2. Verify model, code and dependency licences separately; review commercial redistribution rights.
3. Record checkpoint SHA-256 and verify SafeTensors format before loading.
4. Review model provenance, vulnerability advisories and dependency supply chain.
5. Check available disk, RAM/VRAM and CPU capability before downloading or running.
6. Build a human-reviewed flood-specific evaluation split with scene-level separation.
7. Compare relative-depth outputs with calibrated range references where available; do not treat relative-depth visualizations as metric ground truth.
8. Report latency, peak memory, failure rate, uncertainty behavior and subgroup performance by weather, lighting, water appearance and camera motion.

## Evaluation protocol

Required test conditions:
- dry ground, wet pavement, shallow water and deep-looking water;
- clear, muddy, reflective and turbulent water;
- rain, fog, glare, low light and night imagery;
- boats, people, animals, debris, vegetation, buildings and partially submerged objects;
- motion blur, camera vibration, occlusion, frame drops and camera-height changes.

Required reporting:
- dataset source/licence and scene counts;
- immutable model revision, preprocessing and hardware configuration;
- relative-depth error/ordering metrics where valid reference annotations exist;
- performance by environmental condition;
- invalid-output and failure rates;
- uncertainty and calibration limitations;
- CPU latency and peak RAM measured on the target device.

Acceptance requires independent review and must not be inferred from upstream benchmark results alone.

## Current status

| Item | Status |
|---|---|
| Candidate and model card identified | Documented |
| Model licence declaration | Apache-2.0 on current model card; revision-level verification still required |
| Weights downloaded | No |
| Dependencies installed or changed | No |
| Runtime adapter | Not implemented |
| Flood-specific benchmark | Not available / not run |
| PUI89 device performance | Unknown |
| Metric flood-depth capability | Not provided |
| Physical rescue capability | Not established |

## Sources

- Hugging Face model card: https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf
- Depth Anything V2 paper: https://arxiv.org/abs/2406.09414
- Hugging Face Transformers documentation: https://huggingface.co/docs/transformers/model_doc/depth_anything_v2
