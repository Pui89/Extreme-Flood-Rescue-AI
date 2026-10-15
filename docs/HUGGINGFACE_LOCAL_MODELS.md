## Free local Hugging Face model plan

**Goal:** run a lightweight depth-estimation experiment locally on recorded or simulated flood-scene images, without paid APIs, cloud GPUs, or subscriptions.

### Suggested model
- **Model ID:** [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf)
- **License shown on model card:** Apache-2.0. Recheck the card and upstream terms before redistribution or commercial deployment.
- **Task:** monocular depth estimation and depth-map visualisation.
- **Limit:** relative depth from one image is not calibrated water depth in metres, and cannot by itself establish route safety.

### Local setup
Install PyTorch using the official [local installation selector](https://pytorch.org/get-started/locally/), then:
```bash
python -m pip install transformers accelerate pillow
```
Use batch size 1 and moderate image resolution until GPU VRAM is known. The first run downloads weights; subsequent runs can use the local cache.

### Research tasks
1. Generate depth maps for recorded/simulated flood scenes.
2. Compare maps with ground-truth depth only when valid calibration/measurements exist.
3. Combine perception with labelled obstacle/water segmentation and map uncertainty.
4. Benchmark latency, failures in rain/reflections/low light, and performance by scenario.

### Zero-cost / no-surprise-bill policy
- Run the model on the existing computer only.
- Do not use hosted inference, cloud GPU instances, paid notebooks, or cloud storage.
- Do not upload large model weights to GitHub or run model downloads in CI.
- Keep human supervision and independent robot safety controls; never use a depth map alone to approve a rescue route.

### Status
This is a documented integration plan, not proof that the model is already integrated or validated on flood data.