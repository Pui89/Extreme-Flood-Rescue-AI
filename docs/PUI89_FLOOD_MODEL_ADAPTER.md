# Flood Rescue — PUI89 Project Model Adapter

**Status:** mock-only; model inference is disabled.

The adapter is `tools/pui89_flood_model_adapter.py`. It accepts synthetic hazard-description fixtures and a numeric `scenario_depth_m` between 0 and 15 for simulation test coverage.

The depth value is a scenario parameter only. It does not demonstrate that a robot can operate at that depth, detect people or animals, withstand flood currents, navigate debris, or perform a rescue. The adapter emits no route, rescue instruction, movement command or physical action.

Evidence must be explicitly marked `synthetic`, use a `synthetic://` source reference, include timestamp and lineage, and not be future-dated relative to the request. Physical command fields are rejected. All accepted outputs require operator review.

Run tests: `PYTHONPATH=tools python -m unittest discover -s tests -p "test_pui89_flood_model_adapter.py" -v`.

No model weights, third-party packages, network calls, paid APIs, cloud GPUs or hardware are used. This tests the software boundary only, not flood perception or rescue capability.