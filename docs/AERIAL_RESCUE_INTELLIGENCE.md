# Aerial Rescue Intelligence — RGB + Thermal Observation Contract

**Project placement:** capability under Extreme Flood Rescue AI. It is not a separate product and does not establish drone integration.

## Purpose

Define a vendor-neutral, metadata-first boundary for future aerial RGB and thermal observations. PUI89 develops the software layer; a compatible drone/camera platform remains an independently selected sensor source. The DJI Matrice 5T is one possible reference platform, not a dependency or a purchased/connected device.

## Current implementation

The first software slice is a Python standard-library validator in `pui89_aerial/observation.py`. It accepts metadata only for two modalities (`rgb`, `thermal`) and rejects missing identifiers, unsupported schema/modality, invalid sequence numbers, stale/future timestamps and malformed optional coordinates. Its output explicitly states that image content was not inspected, no person was detected, human review is required and actuation is not authorised.

Run the focused tests from the repository root:

```bash
python -m unittest tests.test_aerial_observation_contract -v
```

## Version 1.0 input envelope

| Field | Type | Rule |
|---|---|---|
| schema_version | string | Exactly `1.0` |
| observation_id | string | Required, non-blank, unique within source stream |
| source_id | string | Required opaque camera/source identifier |
| modality | string | `rgb` or `thermal` |
| captured_at | string | ISO-8601 timestamp with timezone |
| image_ref | string | Opaque local/reference identifier; no remote fetch implied |
| sequence | integer | Non-negative frame sequence; booleans rejected |
| location | object | Optional latitude/longitude within geographic ranges |

## Safety and evidence boundaries

- This contract validates metadata only. It does not decode images, fuse modalities, detect or identify people, estimate coordinates, or control a drone/robot.
- A thermal hotspot is only a candidate observation, not proof of a person or survivor.
- RGB and thermal frames must not be fused until clock synchronisation, calibration, field-of-view alignment and geospatial error have been measured for the actual sensor configuration.
- Stale, missing, conflicting or invalid data must remain rejected/unknown; do not convert missing data into a negative detection.
- Any future target proposal must carry source references, timestamps, uncertainty, model/version, calibration state and an explicit human-review state.
- No autonomous flight, steering, propulsion, braking, rescue action or emergency-response dispatch is authorised by this software.

## Staged development gates

1. **Metadata contract (implemented in this PR):** deterministic validation and unit tests.
2. **Offline sample-data demonstrator:** use legally reusable, provenance-recorded RGB/thermal samples; add a human-reviewed candidate display. Do not download datasets or models automatically.
3. **Sensor compatibility study:** verify vendor SDK/data access, timestamp semantics, calibration and geolocation; no hardware purchase or account/service commitment without explicit approval.
4. **Controlled integration:** only after documented permissions, safety review, repeatable tests and responder feedback.

## Verification status

The tests are authored in this PR; they must be executed in CI or locally before being described as passing. No DJI hardware, drone SDK, thermal imagery, dataset, model weights, paid API or cloud compute is used by this change. This is an executable metadata-validation component, not an aerial rescue demonstrator or validated detection system.
