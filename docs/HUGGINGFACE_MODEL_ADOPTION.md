# Hugging Face Model Adoption — Flood Rescue

**Status:** model candidate registered for evaluation; not integrated into runtime, not downloaded, and not validated on flood-rescue data.

## Decision

Adopt **[Realcat/skywater_seg](https://huggingface.co/Realcat/skywater_seg)** as the first RGB water/person segmentation candidate for a controlled offline evaluation.

Why this candidate:
- Its model card identifies a SegFormer MiT-B2 architecture with 24.7M parameters.
- The published label set is background, sky, water and person.
- The model card declares an MIT licence.
- The model card reports 79.4% water IoU and 77.8% person IoU on its ADE20K-filtered validation set. These are author-reported results on that dataset, not PUI89 results.
- The model card lists an ONNX FP32 checkpoint of about 95 MB, which is a possible later CPU evaluation route. This file is not downloaded by this change.

**Important limitation:** ADE20K-filtered imagery is not a flood-rescue benchmark. The model may confuse muddy water, reflections, rain, debris, submerged objects, people in unusual poses, night scenes and flood boundaries. Its output must be treated as uncertain visual evidence, never as a water-depth estimate, safe-route decision, person-presence guarantee or rescue command.

## Candidate register

| Priority | Model | Intended role | Decision |
|---|---|---|---|
| 1 | [Realcat/skywater_seg](https://huggingface.co/Realcat/skywater_seg) | RGB water/person masks | Evaluate first; MIT declared by model card; no weights downloaded |
| 2 | [nvidia/segformer-b0-finetuned-ade-512-512](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512) | Small general semantic-segmentation baseline | Keep as a fallback baseline; ADE20K labels are broad and do not provide a dedicated flood-water guarantee |
| 3 | [torch-pointcloud/ptv3-base.nuscenes.pointcept](https://huggingface.co/torch-pointcloud/ptv3-base.nuscenes.pointcept) | 3D point-cloud semantic segmentation research | Defer: trained on nuScenes (not flood terrain), 46.2M parameters, GPU-oriented runtime and additional CUDA dependencies |

## Zero-cost and supply-chain gate

This registration does **not**:
- download model weights or datasets;
- install packages or change dependency files;
- call an inference provider, hosted API or cloud GPU;
- add a paid service or create a robot command path.

Before any later download or integration, review and record:
1. Exact model revision/commit and file SHA-256 hashes.
2. Model-card licence and upstream code licence separately; verify whether the licence covers intended redistribution and commercial use.
3. Training-data provenance and dataset terms; the model-card label "ADE20K" is not a substitute for a full dataset-rights review.
4. Safetensors/ONNX/PyTorch file formats, dependency tree, known vulnerabilities and reproducible installation source.
5. Checkpoint size, available disk/RAM/VRAM, CPU compatibility and offline behavior.
6. A human-reviewed flood-specific test set, split provenance and class mapping before any performance claim.

## Required PUI89 evaluation

Use an offline, local, human-reviewed evaluation set with separate scenes for:
- clear and muddy water;
- reflections, glare, rain, fog and low light;
- waves, current, foam, debris and partial submersion;
- people, animals, boats, vegetation, buildings and rescue equipment;
- camera motion, blur, occlusion and dropped frames;
- dry roads, wet roads, shallow water and deep water as visually distinct but not inferable depth classes.

Report per-class IoU, precision, recall, false-negative rate for people, calibration/uncertainty behavior, latency, peak RAM, failure cases and confidence intervals where sample counts permit. Keep scene-level train/validation/test separation to avoid near-duplicate leakage.

Acceptance gates:
- No weights are accepted based only on the upstream model-card scores.
- A missing/invalid frame or unsupported input must produce an explicit unknown/failure state, not a confident mask.
- Preserve frame timestamp, source identifier/hash, model revision, preprocessing configuration and output hash.
- Propagate uncertainty and disagreement into the PUI89 evidence ledger / WorldState; do not overwrite conflicting sensor evidence.
- A person mask is only a candidate observation for human review, not proof that a person is present or absent.
- No model output may directly trigger navigation, propulsion, deployment, contact or rescue actions.

## Integration boundary

If the evaluation passes, add a separately reviewed adapter that emits the existing observation/evidence contract. Keep the model optional and isolated behind an interface. Rule-based checks, safety gates and human approval remain authoritative. The model must be removable without breaking the dependency-free core.

## Current implementation record

- Model metadata and adoption gates: documented in this file.
- Runtime adapter: not implemented.
- Model weights: not downloaded.
- Dependencies: unchanged.
- Flood-specific benchmark: not yet available / not yet run.
- Hardware performance on PUI89 devices: unknown.
- Real-world rescue safety or capability: not established.

## Sources

- [Hugging Face model card — Realcat/skywater_seg](https://huggingface.co/Realcat/skywater_seg)
- [Hugging Face model card — Point Transformer V3 nuScenes checkpoint](https://huggingface.co/torch-pointcloud/ptv3-base.nuscenes.pointcept)
- [Hugging Face SegFormer documentation](https://huggingface.co/docs/transformers/model_doc/segformer)
