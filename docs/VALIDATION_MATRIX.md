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

## Immediate zero-cost next actions

Work in this order; do not skip ahead to hardware or operational claims.

1. **Dataset rights and integrity:** run the existing inventory and manifest audit tools on a user-approved local dataset; verify source URL, licence/permission, attribution, label meaning, hashes and duplicates. Keep downloaded data outside Git unless redistribution is expressly permitted.
2. **Freeze a clean evaluation split:** group by source, scene, capture session or physical item; keep near-duplicates out of different splits. Preserve official benchmark splits where required.
3. **Keep tasks separate:** flood-scene segmentation, person detection and obstacle detection require distinct labels, baselines and metrics. Do not use scene-segmentation labels as person labels.
4. **Record reproducible evidence:** document exact commands, environment, dataset version and split, fixed seed, per-class precision/recall, false negatives, latency, and representative failure cases. If not run, mark **NOT RUN**.
5. **Simulation before hardware:** add deterministic scenarios for missing/stale/conflicting sensor data, invalid transforms, unknown map cells, blocked routes and communication loss. Each failure must reach STOP or human review.
6. **No-cost boundary:** prefer the current local Python tools and available hardware. Do not enable paid APIs, cloud GPUs, hosted inference or subscriptions. If a future step may incur a charge, stop and ask first.

**Next milestone:** a lawful, audited dataset manifest and a baseline evaluation report—not a claim of successful flood rescue.

## Data and safety rules

- Flood segmentation is not person detection, and RGB imagery alone does not provide reliable water-depth measurements.
- Unknown terrain is not safe terrain. Missing or stale sensor data must produce STOP or human review.
- Do not send a robot into floodwater on the basis of model predictions.
- Keep raw data and weights out of Git unless rights permit redistribution.
- Mark tests **PASS**, **FAIL**, or **NOT RUN** and attach the exact run or report.
