# Validation Matrix — Flood Rescue AI

Last reviewed: 18 October 2026. This matrix separates software evidence from rescue capability.

| Capability | Repository evidence | Current status | What is still required |
|---|---|---|---|
| Workflow orchestration and audit | `flood_robot/`, `demo_end_to_end.py` | Software prototype and regression tests exist | Continue running full CI for changes; review audit output |
| Fail-safe decision gates | Existing end-to-end and safety tests | Tests include human-review requirement and no actuator command | Independent hazard analysis and simulation fault injection |
| Dataset provenance | `tools/dataset_inventory.py`, `tools/audit_dataset_manifest.py` | Local inventory and licence/label audit tools; regression tests passed in CI | Download and inspect actual source files; verify licence and attribution per dataset |
| Leakage-aware splitting | `tools/group_split_manifest.py` | Requires approved rights and human-verified labels; tests passed in CI | Group images by scene/video/location; preserve official benchmark splits |
| Flood segmentation | Dataset guidance for FloodNet | Data source and task are documented; no trained result claimed | Inspect official labels, train a compatible segmentation model, evaluate on official held-out split |
| Person detection | Separate task from flood segmentation | **Not validated by FloodNet alone** | Suitable licensed person dataset, reviewed labels, independent test and false-negative analysis |
| Navigation and hazard mapping | Blueprint for ROS 2 / Gazebo / Nav2 integration | Architecture/adapter work remains | Runnable simulation, coordinate-frame validation, traversability checks and route-failure tests |
| Real flood rescue | No field validation established | **Not validated** | Authorised rescue partners, suitable hardware, supervised non-hazardous trials, safety review and documented results |

## Data and safety rules

- Flood segmentation is not person detection, and RGB imagery alone does not provide reliable water-depth measurements.
- Unknown terrain is not safe terrain. Missing or stale sensor data must produce STOP or human review.
- Do not send a robot into floodwater on the basis of model predictions.
- Keep raw data and weights out of Git unless rights permit redistribution.
- Mark tests **PASS**, **FAIL**, or **NOT RUN** and attach the exact run or report.
