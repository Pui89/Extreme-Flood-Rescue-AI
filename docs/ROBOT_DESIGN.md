# Flood Rescue AI — Low-Cost Robot Concept

## Design goal

Prototype a small, remotely supervised surface platform for collecting water-level and scene observations in a controlled environment. This is a **research concept**, not a flood-ready rescue craft.

## Concept architecture

1. **First stage — desk simulation:** use recorded images and synthetic or clearly labeled sample sensor values. No watercraft is required.
2. **Observation payload:** consider a camera and water-level sensor only after the software simulation works. Treat sensor values as unverified until calibrated.
3. **Platform:** if physical testing is later approved, use a small tethered test boat in a pool or controlled pond, with a manual recovery method. Do not test in floodwater.
4. **Local computer:** start with an existing laptop. A small edge computer is optional.
5. **Local perception:** use OpenCV and a locally run model to flag possible people, debris, or water boundaries. An image alone cannot establish water depth, current strength, or route safety.
6. **Operator dashboard:** show timestamped observations, sensor health, uncertainty, and source information.
7. **Voice alerts:** announce only supported findings, such as “sensor reading received” or “possible person detected—verify.” Speech output must not automatically dispatch rescuers.

## Free-first software

- Python, OpenCV, PyTorch, and local notebooks/scripts.
- Offline simulation and recorded sample data for early tests.
- Kokoro-82M for English speech tests; SakThai TTS for experimental Thai speech.
- GitHub for code and documentation. Do not add paid cloud services or hosted inference APIs.

Software can be free; cameras, waterproof housings, sensors, radios, batteries, propulsion, and safety equipment may cost money. Reuse available devices and do not buy hardware until simulation gives useful results.

## Staged prototype plan

- [ ] Stage 1: create a simulation with labeled example images and synthetic water-level readings.
- [ ] Stage 2: test detection performance, missing data, timestamp delays, and false alarms.
- [ ] Stage 3: show alerts and uncertainty in a local dashboard.
- [ ] Stage 4: test sensor readings in a controlled non-flood environment.
- [ ] Stage 5: only after engineering review, test a small tethered platform in a controlled pool or pond.
- [ ] Stage 6: independent safety review before any operational deployment is considered.

## Safety acceptance checks

- Missing, stale, or conflicting data is marked unknown.
- Never label a route “safe” based only on model output.
- No autonomous entry into floodwater, moving water, or hazardous environments.
- A trained incident commander retains decision authority.
- Protect location data and avoid broadcasting sensitive rescue information.

**Status:** concept and staged test plan only. It is not a validated rescue robot and must not be relied on during an emergency.
