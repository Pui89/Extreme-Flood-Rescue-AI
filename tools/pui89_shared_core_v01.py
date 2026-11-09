"""Map synthetic Flood Rescue adapter output to Shared AI Core v0.1."""
from __future__ import annotations
from datetime import datetime

SCHEMA_VERSION = "0.1.0"

def _timestamp(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be valid ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include a timezone")
    return value

def build_flood_v01_records(envelope):
    """Translate only the existing synthetic review envelope; never create routes/actions."""
    if not isinstance(envelope, dict):
        raise ValueError("envelope must be an object")
    evidence = envelope.get("evidence")
    observations = envelope.get("observations")
    if not isinstance(evidence, dict) or not isinstance(observations, list) or not observations:
        raise ValueError("envelope must contain evidence and observations")
    source_id = evidence.get("source_id")
    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("evidence.source_id must be a non-empty string")
    observed_at = _timestamp(evidence.get("timestamp"))
    created_at = _timestamp(envelope.get("agent_message", {}).get("timestamp"))
    if evidence.get("evidence_kind") != "synthetic":
        raise ValueError("Flood v0.1 mapping accepts synthetic evidence only")

    observation = {
        "schema_version": SCHEMA_VERSION,
        "observation_id": source_id,
        "observed_at": observed_at,
        "source": {
            "source_id": source_id,
            "source_type": "simulation",
            "device_or_system": "PUI89 Flood Rescue synthetic scenario adapter",
        },
        "modality": "other",
        "payload": {
            "domain": "extreme_flood_rescue",
            "scenario_observations": observations,
            "limitations": envelope.get("limitations", []),
        },
        "quality": {
            "status": "unknown",
            "notes": "Synthetic scenario fixture; no real flood sensor measurement is represented.",
        },
        "uncertainty": {
            "description": "Scenario inputs do not establish real water depth, current, obstacle, or rescue conditions.",
        },
        "provenance": {"recorded_at": observed_at, "dataset_or_file": evidence.get("source_ref", "")},
    }
    proposal = {
        "schema_version": SCHEMA_VERSION,
        "proposal_id": f"flood-human-review:{envelope.get('request_id', source_id)}",
        "created_at": created_at,
        "objective": "Request human review of the synthetic flood scenario context.",
        "actions": [{
            "action_id": f"review:{source_id}",
            "description": "Review the scenario assumptions and identify missing evidence; do not issue movement or rescue commands.",
            "risk_level": "unknown",
            "preconditions": [
                "Confirm that all inputs are synthetic scenario data.",
                "Obtain independently verified local conditions before any operational decision.",
            ],
            "expected_effect": "A human reviewer records whether the scenario assumptions are adequate or requests more evidence.",
            "hazards": [
                "Real flood depth and current may differ materially from the scenario.",
                "No rescue capability, route safety, buoyancy, or 15 m operating capability is established.",
            ],
            "evidence_refs": [source_id],
        }],
        "authority": {
            "mode": "advisory_only",
            "human_approval_required": True,
            "execution_authorized": False,
        },
        "uncertainties": [
            "Synthetic simulation context only; no live sensing or model inference.",
            "No route planning, rescue command, or physical actuation is provided.",
        ],
    }
    return {"observation": observation, "action_proposal": proposal}
