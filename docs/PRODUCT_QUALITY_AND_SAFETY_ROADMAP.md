# Product Quality and Safety Roadmap — Extreme-Flood-Rescue-AI

**Status:** development roadmap, not a safety certification, compliance claim or proof of validated real-world performance.

## Project-specific safety focus

mobile/boat/drone rescue concepts; flood depth up to 15 m is a simulated scenario parameter only; no validated buoyancy, current tolerance, passenger support or rescue performance.

**Required conservative behavior:** No approach/rescue action if depth/current envelope, localisation, obstacle/person detection, communication, battery reserve or recovery plan is unknown; a software STOP is not a physical emergency stop.



## Water operations, buoyancy, current and environmental safety gates

**Current status: NOT VALIDATED.** The repository does not establish a tested hull, displacement, freeboard, stability envelope, payload capacity, propulsion capability, water-ingress rating, fire resistance or safe operation in floodwater. The proposed 0–15 m depth range and strong-current scenarios are design/evaluation targets only. Depth alone is not a sufficient operating limit.

Before any water test or rescue-use claim, define and independently review the complete operating envelope for the exact platform and configuration.

1. **Buoyancy and stability:** document hull geometry, displacement, reserve buoyancy, freeboard, centre of gravity, payload distribution, trim, roll/pitch stability, flooding compartments and recovery after partial flooding. Test unmanned, instrumented prototypes first in a controlled facility. Do not infer passenger, victim or animal carrying capacity from a concept image or nominal displacement.
2. **Current, waves and depth:** measure and specify current speed/direction, turbulence, debris loading, wave/wake conditions, water depth, bank/obstacle clearance and visibility. Establish conservative abort limits from measured platform trials. A software scenario or the proposed 15 m depth does not establish current tolerance, pressure resistance, tether length or underwater capability.
3. **Propulsion and entanglement:** guard propellers and moving water-drive components; assess weeds, ropes, clothing, debris and body-part entrapment. Verify stopping, reverse/neutral behavior, steering authority and loss-of-control response under bounded test conditions. Keep people outside the hazard zone during unmanned tests.
4. **Water ingress and corrosion:** assess every enclosure, connector, cable entry, shaft seal, hatch, sensor window and battery compartment. Specify a test method and acceptance criteria for immersion depth, duration, water type, pressure, spray, condensation and post-test inspection. Do not assign an IP or immersion rating without applicable system-level testing. Floodwater may be contaminated; define cleaning, isolation and disposal procedures.
5. **Electrical and battery safety:** document battery chemistry, BMS, fusing, isolation, charging, connector ratings, thermal limits, short-circuit protection and emergency energy isolation. Assess salt/dirty water exposure, damaged seals, conductive contamination and post-immersion faults. Never charge, energise or handle a wet/damaged battery or electrical assembly outside a qualified procedure.
6. **Fire and thermal hazards:** assess battery thermal runaway, charging faults, propulsion stalls, wiring faults, water ingress and post-impact damage. Define detection, isolation, evacuation and responder procedures. Conduct battery abuse/fault testing only in a qualified controlled facility; do not improvise such tests.
7. **Recovery and human factors:** define retrieval points, lifting/towing loads, capsizing response, lost-link behavior, manual override, emergency stop suitability, operator visibility, communications fallback and safe recovery when propulsion is unavailable. A generic “power off” instruction may worsen a drifting boat or an aircraft emergency; safe states must be platform-specific.
8. **Multi-platform separation:** ground vehicle, surface vessel, aerial vehicle and any future submersible require separate hazard analyses, operating envelopes, communications-loss behaviors and validation records. Evidence from one platform cannot validate another.
9. **Rescue interaction:** no human or animal contact, lifting, towing or transport trial until the exact hardware has passed staged unmanned tests, independent risk review and supervised acceptance. Define entrapment, panic, cold exposure, contamination, accessibility and responder coordination hazards. AI detections are unverified alerts, not proof that a person is present or safe to approach.
10. **Evidence record:** retain hardware revision and BOM, test facility, method, instrument calibration, water/current conditions, payload, configuration, pass/fail criteria, observed failures, recovery outcomes, reviewer and explicit NOT TESTED items.

Until the relevant gates are independently evidenced, describe the project only as a software decision-support and synthetic-scenario prototype with proposed rescue-platform concepts. Do not claim waterproofing, fire resistance, buoyancy, passenger capacity, strong-current capability, 15 m operation, autonomous rescue or field readiness.

## Cross-project quality gates

1. **Requirements and hazard analysis:** define intended use, prohibited use, users, operating environment, measurable acceptance criteria, foreseeable misuse, hazards, emergency procedures and stop-work authority with qualified domain experts.
2. **Fail-safe software:** test missing, stale, conflicting, malformed, out-of-range and low-confidence inputs; communications loss; emergency stop requests; restart/power loss; safe hold; manual override; bounded logging; and recovery from faults. Never silently guess missing safety data.
3. **Reproducible evidence:** record exact commit, environment, configuration hash, test/scenario ID, expected and observed outcome, failure codes, latency where measured, reviewer and NOT RUN items. Keep synthetic, simulation, lab and field evidence separate.
4. **Independent evaluation:** freeze a lawful, licensed, human-reviewed, leakage-safe held-out dataset or scenario set before testing. Publish sample counts, class-wise performance, false positives/negatives, uncertainty and limitations. Never copy literature metrics as project results or infer results from tool presence.
5. **Physical validation:** before people-at-risk testing, require a documented risk assessment, qualified engineering review, staged tests, emergency/recovery plan, incident log, and signed acceptance criteria for the exact hardware/software configuration.
6. **Cybersecurity and privacy:** least privilege, no secrets in Git, dependency/vulnerability review, controlled updates and rollback, data minimisation, access controls, retention/deletion rules and incident response.
7. **Maintainability:** document calibration/pre-use checks, operating limits, wear parts, maintenance intervals, fault codes, operator training, spares, warranty/support assumptions and safe decommissioning.
8. **Commercial release gate:** no buyer-facing safety, accuracy, autonomy, lives-saved, reach, chemical-identification or rescue-capability claim without independent evidence for the released configuration. Include limitations and known failure modes.

## Standards and external review

Use [ISO 12100](https://www.iso.org/standard/51528.html) as a general machinery risk-assessment starting point where applicable and the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for AI risk-lifecycle practices. [ISO 10218-1:2025](https://www.iso.org/standard/73933.html) and [ISO 10218-2:2025](https://www.iso.org/standard/73934.html) address industrial robots and industrial robot applications; applicability to each PUI89 mobile, agricultural, rescue or public-facing concept must be determined by qualified specialists. Referencing a standard is not compliance or certification. Check relevant Thai and target-market laws and standards before any pilot or sale.

## Customer/buyer evidence pack

Before a pilot, prepare: intended-use statement; operating envelope; risk register and residual risks; test plan/results including failures; dataset/model/sensor provenance; hardware/software bill of materials; cybersecurity/privacy notes; installation/site requirements; operator training; maintenance/support plan; incident and rollback procedure; and clear exclusions. A polished README or simulation pass alone is not product readiness.

## Free-first policy

Prefer offline, standard-library checks and synthetic tests first. No paid API, recurring service, automatic model download, external data upload or hardware actuation is required by this roadmap. Review licences, privacy, hardware fit, maintenance cost and safety impact before adding any tool or dependency.
