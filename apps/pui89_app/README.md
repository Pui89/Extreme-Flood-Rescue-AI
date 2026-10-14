# PUI89 Flood Rescue AI Application

A simulation-first API and interactive dashboard for flood-scene reconnaissance and **human-supervised rescue decision support**. The baseline processes structured candidate and hazard observations; it is not a trained victim detector, a hydrodynamic simulator, or a certified rescue system.

## Interactive web demo

The Streamlit dashboard lets you adjust example sensor-health values, water depth/current estimates and one possible-person track, submit those observations to the API, inspect the resulting review status, and download a JSON report.

### Run locally

From the repository root, install the application dependencies:

```bash
python -m pip install -r apps/pui89_app/requirements.txt
```

**Terminal 1 — start the API:**

```bash
uvicorn apps.pui89_app.main:app --reload
```

**Terminal 2 — start the dashboard:**

```bash
streamlit run apps/pui89_app/web_demo.py
```

Open the local URL printed by Streamlit. The API documentation is available at `http://127.0.0.1:8000/docs`.

Optional: upload a flood-scene image to display it as context. **The uploaded image is preview-only; no computer-vision model analyses it in this demo.** The candidate values are entered manually and passed to the existing API.

## API

- `GET /health` — service status.
- `POST /analyze` — sensor-quality gate, candidate evidence review, hazard-aware route status.
- `GET /metrics` — request counters, not AI benchmark results.

Example request:

```json
{
  "rgb_available": true,
  "thermal_available": true,
  "lidar_valid": true,
  "timestamp_skew_ms": 12,
  "water_depth_m": 0.25,
  "current_speed_mps": 0.2,
  "candidates": [{
    "track_id": "person-candidate-01",
    "visual_confidence": 0.88,
    "thermal_support": true,
    "track_stability_frames": 8,
    "distance_m": 6.2
  }]
}
```

## Safety and evidence boundaries

- Missing sensor evidence, stale timestamps, excessive illustrative water depth/current, or uncertain tracks lead to `SAFE_HOLD` or `HUMAN_REVIEW`.
- Candidate scores are heuristic evidence-ranking values, not probabilities or definitive victim identification.
- A route status of `NOT_VALIDATED` does not mean the route is safe.
- This service never issues movement commands and must not replace emergency services or trained rescue personnel.
- Thresholds are illustrative configuration defaults, not universally safe flood limits.
- This is an interactive API demo, not evidence of real-world detection accuracy or field-tested rescue capability.

## Benchmark plan

Use labeled, consented datasets and simulator scenarios. Report detection precision/recall, time-to-detect, tracking continuity, localization error, hazard false negatives, route feasibility, latency, resource use, sensor-dropout behavior and sim-to-real gap. Do not mix simulated and field results.

## Tests

```bash
python -m unittest discover -s apps/pui89_app -p 'test_*.py' -v
```
