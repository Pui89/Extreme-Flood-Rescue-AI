"""Fail-closed validation for RGB/thermal aerial observations.

This module validates metadata only. It does not decode imagery, detect people,
perform sensor fusion, estimate location, or command a drone or rescue platform.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SUPPORTED_MODALITIES = {"rgb", "thermal"}
MAX_FUTURE_SECONDS = 5.0


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate_observation(payload: Any, *, now: datetime | None = None,
                         max_age_seconds: float = 5.0) -> dict[str, Any]:
    """Return a conservative validation result; invalid input is never accepted.

    Required fields: schema_version, observation_id, source_id, modality,
    captured_at, image_ref, and sequence. image_ref is an opaque local/reference
    string; image bytes are deliberately outside this metadata-only contract.
    """
    errors: list[str] = []
    if not isinstance(payload, dict):
        return {"accepted": False, "status": "REJECTED", "errors": ["payload_not_object"]}

    required = ("schema_version", "observation_id", "source_id", "modality",
                "captured_at", "image_ref", "sequence")
    for key in required:
        value = payload.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"missing_or_blank:{key}")

    if payload.get("schema_version") != "1.0":
        errors.append("unsupported_schema_version")
    if payload.get("modality") not in SUPPORTED_MODALITIES:
        errors.append("unsupported_modality")
    if not isinstance(payload.get("sequence"), int) or isinstance(payload.get("sequence"), bool) or payload.get("sequence", -1) < 0:
        errors.append("invalid_sequence")

    captured = _parse_timestamp(payload.get("captured_at"))
    if captured is None:
        errors.append("invalid_or_timezone_missing_timestamp")
    else:
        reference = now or datetime.now(timezone.utc)
        if reference.tzinfo is None:
            errors.append("reference_time_requires_timezone")
        else:
            age = (reference.astimezone(timezone.utc) - captured).total_seconds()
            if age < -MAX_FUTURE_SECONDS:
                errors.append("timestamp_in_future")
            elif age > max_age_seconds:
                errors.append("stale_observation")

    location = payload.get("location")
    if location is not None:
        if not isinstance(location, dict):
            errors.append("invalid_location_object")
        else:
            lat, lon = location.get("latitude"), location.get("longitude")
            if (not isinstance(lat, (int, float)) or isinstance(lat, bool) or not -90 <= lat <= 90
                or not isinstance(lon, (int, float)) or isinstance(lon, bool) or not -180 <= lon <= 180):
                errors.append("invalid_location_coordinates")

    accepted = not errors
    return {
        "accepted": accepted,
        "status": "ACCEPTED_METADATA_ONLY" if accepted else "REJECTED",
        "errors": errors,
        "observation_id": payload.get("observation_id") if accepted else None,
        "modality": payload.get("modality") if accepted else None,
        "human_review_required": True,
        "image_content_inspected": False,
        "person_detected": None,
        "actuation_authorized": False,
    }
