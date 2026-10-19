# Validation Matrix — Flood Rescue AI

Last reviewed: 20 October 2026. This matrix separates software evidence from rescue capability.

## Latest automated evidence

The latest main-branch CI run [39276988264](https://github.com/Pui89/Flood-Rescue-AI/actions/runs/39276988264) passed test jobs on Python 3.10, 3.11 and 3.12, including dataset-tool syntax checks, the test suite and a deterministic end-to-end demo. This is software-level evidence only; it does not validate real-world person detection, flood mapping, navigation or rescue.

| Capability | Repository evidence | Current status | What is still required |
|---|---|---|---|
| Workflow orchestration and audit | `flood_robot/`, `demo_end_to_end.py` | Software prototype and regression tests exist; latest CI passed | Review audit output and continue testing changes |
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
