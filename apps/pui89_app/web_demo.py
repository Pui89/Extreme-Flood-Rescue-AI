"""Streamlit front end for the Flood Rescue AI decision-support API.

Uploaded images are preview-only. This demo sends manually entered example
observations to the existing API; it does not run a trained vision model.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import requests
import streamlit as st

st.set_page_config(page_title="Flood Rescue AI | Field Review Demo", page_icon="🌊", layout="wide")

st.title("🌊 Flood Rescue AI")
st.caption("Interactive research demo · Flood reconnaissance · Human-supervised review")
st.warning(
    "Research prototype only. This dashboard does not identify victims from uploaded images, "
    "certify routes as safe, dispatch rescuers, or control a robot. Use official emergency services "
    "and trained rescue personnel for real incidents."
)

with st.sidebar:
    st.header("API connection")
    api_url = st.text_input("API base URL", value="http://127.0.0.1:8000").rstrip("/")
    st.markdown("[API documentation](http://127.0.0.1:8000/docs)")
    st.caption("Start the API in one terminal, then this dashboard in another.")

left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("1 · Scene evidence")
    uploaded = st.file_uploader("Optional flood-scene image (preview only)", type=["png", "jpg", "jpeg", "webp"])
    if uploaded is not None:
        st.image(uploaded, caption="Reference image only — no image inference is performed", use_container_width=True)
    st.markdown("**Sensor status**")
    rgb_available = st.checkbox("RGB camera available", value=True)
    thermal_available = st.checkbox("Thermal camera available", value=True)
    lidar_valid = st.checkbox("LiDAR/depth data valid", value=True)
    timestamp_skew_ms = st.slider("Sensor timestamp difference (ms)", min_value=0, max_value=250, value=12, step=1)
    st.markdown("**Flood conditions**")
    water_depth_m = st.slider("Estimated water depth (m)", min_value=0.0, max_value=1.5, value=0.20, step=0.05)
    current_speed_mps = st.slider("Estimated current speed (m/s)", min_value=0.0, max_value=2.0, value=0.15, step=0.05)

with right:
    st.subheader("2 · Candidate observation")
    use_candidate = st.checkbox("Include one possible-person track", value=True)
    track_id = st.text_input("Track ID", value="person-candidate-01")
    visual_confidence = st.slider("Visual evidence score (manual example)", 0.0, 1.0, 0.88, 0.01)
    thermal_support = st.checkbox("Thermal sensor corroborates this track", value=True)
    track_stability_frames = st.slider("Stable tracking frames", min_value=0, max_value=30, value=8)
    distance_m = st.number_input("Estimated distance (m)", min_value=0.0, max_value=500.0, value=6.2, step=0.5)
    st.caption("These are manually entered demonstration values, not model predictions or calibrated probabilities.")

candidate_list = []
if use_candidate:
    candidate_list.append({
        "track_id": track_id.strip() or "candidate-01",
        "visual_confidence": visual_confidence,
        "thermal_support": thermal_support,
        "track_stability_frames": track_stability_frames,
        "distance_m": distance_m,
    })

payload = {
    "rgb_available": rgb_available,
    "thermal_available": thermal_available,
    "lidar_valid": lidar_valid,
    "timestamp_skew_ms": timestamp_skew_ms,
    "water_depth_m": water_depth_m,
    "current_speed_mps": current_speed_mps,
    "candidates": candidate_list,
}

st.subheader("3 · Review the evidence")
with st.expander("View request payload sent to the API"):
    st.json(payload)

if st.button("Analyze example scene", type="primary", use_container_width=True):
    try:
        response = requests.post(f"{api_url}/analyze", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        st.session_state["flood_rescue_last_result"] = result
        st.session_state["flood_rescue_last_payload"] = payload
        st.session_state["flood_rescue_timestamp"] = datetime.now(timezone.utc).isoformat()
    except requests.RequestException as exc:
        st.error(f"Could not reach the API at {api_url}. Start the API first. Details: {exc}")

result = st.session_state.get("flood_rescue_last_result")
if result:
    st.divider()
    st.subheader("4 · Decision-support output")
    status = result.get("status", "UNKNOWN")
    route_status = result.get("route_status", "NOT_EVALUATED")
    a, b, c = st.columns(3)
    a.metric("Analysis status", status)
    b.metric("Route review", route_status)
    c.metric("Robot commands sent", "No")
    reasons = result.get("sensor_reasons", []) + result.get("hazard_reasons", [])
    if reasons:
        st.error("Warnings: " + ", ".join(reasons))
    else:
        st.info("No configured sensor/hazard warning was triggered by these example inputs. This does not certify a route as safe.")
    reviews = result.get("candidate_reviews", [])
    if reviews:
        st.markdown("**Candidate evidence review**")
        st.dataframe(reviews, use_container_width=True, hide_index=True)
    elif use_candidate is False:
        st.info("No candidate track was submitted.")
    st.markdown("**Full API response**")
    st.json(result)
    report = {
        "created_at_utc": st.session_state.get("flood_rescue_timestamp"),
        "demo_only": True,
        "image_inference_performed": False,
        "request": st.session_state.get("flood_rescue_last_payload"),
        "response": result,
    }
    st.download_button(
        "Download example review (JSON)",
        data=json.dumps(report, indent=2),
        file_name="flood_rescue_review_demo.json",
        mime="application/json",
    )

st.divider()
st.caption(
    "Safety boundary: all thresholds are illustrative defaults. Human responders retain decision authority. "
    "A missing detection is not evidence that an area is clear, and a candidate score is not proof of a victim."
)
