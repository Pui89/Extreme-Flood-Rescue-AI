# Free Flood Imagery Sources and Training Plan

**Status: source shortlist documented; no dataset has been downloaded, licensed for this repository, or approved for training yet.**

Goal: build a free-first flood-perception dataset for the Flood Rescue AI project, including aerial/drone scenes, satellite flood extent, roads/buildings, and flood-affected environments relevant to severe events such as those in Nepal. Never pay for data or download large archives automatically.

## Candidate sources

| Source | Imagery / labels | Licence and access status | Planned use and caveats |
|---|---|---|---|
| [LADI — Low Altitude Disaster Imagery](https://registry.opendata.aws/ladi/) and [documentation](https://github.com/LADI-Dataset/ladi-overview) | Real low-altitude oblique airborne disaster imagery with human/machine annotations, covering disaster responses from 2015–2023 | Registry lists CC BY 4.0; retain attribution and verify the specific files and documentation before use | Strong candidate for aerial disaster-scene perception. It is not a water-depth dataset, and not every image is necessarily a flood scene. |
| [FloodNet supervised dataset](https://github.com/BinaLab/FloodNet-Supervised_v1.0) | 2,343 high-resolution UAV images captured after Hurricane Harvey, with scene segmentation labels including flooded/non-flooded roads and buildings, water, trees and vehicles | Repository states Community Data License Agreement (CDLA) Permissive 1.0; read and comply with its terms and attribution/citation requirements | Candidate for aerial flood scene understanding and segmentation. It is post-flood imagery; labels do not provide calibrated water depth in metres. |
| [Sen1Floods11](https://github.com/cloudtostreet/Sen1Floods11) | Sentinel-1 SAR satellite tiles with flood/water masks and official train/validation/test split files | Public download is documented, but the dataset's governing reuse terms must be confirmed from upstream documentation before commercial reuse | Candidate for satellite flood-extent segmentation. SAR imagery is not ordinary camera imagery and cannot alone tell the robot's local water depth. Upstream documentation describes a roughly 14 GB full download, so start with a small approved subset. |
| [STURM-Flood](https://zenodo.org/records/12748983) | Open-access Sentinel-1 and Sentinel-2 tiles with water masks covering 60 global flood events | Open access is stated; verify the record's specific licence and conditions before reuse | Candidate for satellite water-extent learning and cross-event testing. Satellite tiles do not directly label robot-scale depth or safe movement. |
| [OpenAerialMap](https://imagery.hotosm.org/) | Community-contributed aerial/satellite imagery with item-level metadata | Platform describes imagery as openly licensed and CC-BY compatible; verify each item's actual licence, attribution and permitted use | Search for Nepal flood-response imagery and relevant river/floodplain scenes. Check item-level permissions and whether labels are available. |
| [Nepal flood event imagery and maps — Sentinel Asia](https://sentinel-asia.org/EO/2024/article20240730NP.html) | Event-specific satellite images and flood-proxy products for Nepal, including Kathmandu/Bagmati-region events in 2024 | **Reference/source-discovery only until each download's licence and reuse permission are confirmed** | Valuable for finding real Nepal event examples. Do not assume every partner product can be freely reused or redistributed; some are analysis products rather than labelled training images. |
| [UNOSAT Nepal flood extent product](https://unosat.org/products/3983) | Sentinel-1-derived flood-extent map and downloadable geospatial files for Koshi and Madhesh, Nepal, September 2024 | Product-specific terms apply; confirm the current UNOSAT terms and source-image rights before reuse | Useful for geographic context and map evaluation. A map or polygon is not a ground-level rescue-robot photo, and its preliminary analysis may not be field-validated. |

## Nepal and extreme-water-level requirements

Use Nepal flood events to improve geographic diversity, terrain, river behaviour, debris, damaged roads, and settlement scenarios. However:

- Do not label an image “6 m”, “10 m” or “15 m deep” based only on visual appearance.
- Real water-depth labels require a trusted gauge, surveyed reference, documented depth product, or other defensible measurement linked to the image's location and time.
- Satellite flood masks support **extent** mapping, not a direct per-pixel depth measurement unless paired with a validated depth product.
- Keep separate tasks for (1) satellite flood extent, (2) aerial/ground flood-scene perception, (3) people/animals/vehicles/buildings/roads, and (4) water depth/flow estimation.
- Severe-flood and Himalayan scenes should be held out by event/location for robust testing, not randomly mixed with nearly identical frames from the same event.

## Free-first dataset acceptance checklist

Before any image or label is added to training:

- [ ] No cost, subscription, paid API, or cloud-GPU requirement.
- [ ] Verify the actual image/dataset licence, commercial reuse rights if needed, attribution and redistribution restrictions.
- [ ] Record source URL, image ID, author/provider, licence, download date, event/date/location, and file checksum.
- [ ] Record modality (ground RGB, UAV RGB, satellite optical, SAR, map/vector) and whether the image is real, simulated or synthetic.
- [ ] Record label provenance and annotation confidence. Do not invent labels from captions or appearance.
- [ ] Check duplicates and split by event/location/video/source to reduce leakage.
- [ ] Keep a final test split untouched until model and thresholds are selected.
- [ ] Do not redistribute the original files unless the terms permit it.

## Initial evaluation protocol

After data approval, make group-aware train/validation/test splits (target 70/15/15 only if dataset size and upstream split permit). Preserve official splits where available and document deviations.

Report metrics per task:
- Water segmentation: IoU/mIoU, precision, recall, and false-water / missed-water error.
- Scene perception: per-class precision/recall and mAP when valid object boxes exist.
- Water depth: MAE/RMSE only where trustworthy numeric depth ground truth exists.
- Rescue navigation: evaluate in simulation separately; imagery training alone does not validate physical robot safety or capability.

## Project boundary

This source plan does not claim that the robot can operate at any real-world flood depth. The project's 0–15 m slider is a simulation scenario range; it is not a physical rating. Ground-robot motion must remain blocked at the current 5.5 m safety boundary and above. Any amphibious platform, boat or drone capability requires its own engineering design and validation.

## Best-robot training priorities: coordinated ground + boat + drone system

The best design is a **coordinated multi-platform rescue system**, not one robot expected to cross every flood depth. Each platform needs a separate perception and safety envelope.

### Priority 1 — drone / aerial perception (start here)

Use [FloodNet](https://github.com/BinaLab/FloodNet-Supervised_v1.0) for its labelled aerial classes and [LADI](https://registry.opendata.aws/ladi/) for low-altitude disaster-scene diversity. Build a small, licence-approved subset first. Train/benchmark water, flooded road, building, vehicle, tree and visible-person/animal classes only when appropriate labels actually exist. Do not infer people or animals labels where the source does not provide them.

### Priority 2 — ground robot perception

Create a separate ground-camera dataset from openly licensed, item-level verified images of flooded streets, debris, road edges, people, animals and obstacles. Search [OpenAerialMap](https://imagery.hotosm.org/) for suitable low-angle/oblique views, but only accept images whose item metadata supports the intended use. Satellite images and aerial views must not be presented as ground-camera training examples. If the first licensed source set lacks ground-view images, record that gap instead of silently filling it with unlicensed images.

### Priority 3 — boat perception and navigation

Use separate water-level camera scenes for floating debris, submerged/hidden road edges, people/animals in water, banks, current indicators and safe landing points. Public flood imagery may support visible-scene perception, but it rarely supplies reliable current velocity, depth, boat stability or payload labels. Test navigation and stability in simulation and controlled trials, not by claiming image training proves safe operation.

### Priority 4 — Nepal / Himalayan extreme-event holdout

The [Nepal Flood 2026 building inventory](https://huggingface.co/datasets/hotosm/nepal_flood_2026) is listed under CC BY 4.0, but it is geospatial building-footprint/density data—not a labelled flood-photo dataset. Use it for map context and geospatial evaluation, with attribution, not for RGB object-detection training.

Some imagery released for the 2026 Nepal flood by Vantor was made available under **CC BY-NC 4.0** according to HOT. That is non-commercial: exclude it from the commercial/product training corpus unless a separate commercial licence is obtained. It may be considered only for a clearly separate non-commercial experiment after reviewing exact image terms. See [HOT's Nepal flood imagery note](https://www.hotosm.org/en/news/mapping-the-nepal-floods/).

### Depth and flow labels are a separate supervised task

For water depth, consider [SERVIR-HKH's Flood Inundation Mapping Tool](https://servir.icimod.org/science-applications/flood-inundation-mapping-tool/), which describes satellite flood extent and depth estimates at approximately 30 m horizontal resolution. Confirm data access and reuse rights for each product. This is coarse geospatial context, not robot-scale ground truth, and it must not be used as a precise depth label for individual camera pixels or a robot's exact location without validation.

### Build sequence

1. Review licences and select a small set; no paid services and no automatic large downloads.
2. Create a manifest with source URL, licence, event/location/date, modality, labels, file hash and attribution.
3. Start with aerial segmentation using FloodNet's official splits, then test on separate events where licensed labelled data exists.
4. Add ground-view and boat-view datasets only when lawful real imagery and defensible labels are available.
5. Keep Nepal/Himalayan events as location/event holdouts where enough valid labelled data exists.
6. Measure per-class precision/recall and segmentation IoU. Measure depth error only against trustworthy numeric depth labels.
7. Validate each platform independently in simulation and controlled tests. The 0–15 m scenario range remains a simulation range, not a real robot rating; the ground robot remains in safe hold at 5.5 m and above.

## Terrain-aware flood hazard assessment (new engineering requirement)

The Nepal survivor-house article is a useful scenario prompt, not proof of a building's structural properties or a validated engineering case study. Do not infer flood depth, current, foundation strength, or structural safety from a photograph alone.

The rescue system should assess **route hazards**, not just visible water depth. Treat these as separate inputs with confidence and timestamps:

- **Water:** measured/estimated depth, flow velocity and direction, sudden changes, and uncertainty. Unknown current or depth must not be treated as safe.
- **Terrain and access:** slope, bank/edge stability, road washout, hidden drops, submerged obstacles, mud, loose rocks and narrow channels.
- **Debris and structures:** floating logs/vehicles, debris dams, damaged bridges, unstable walls, partially collapsed buildings and overhead hazards. A standing building is not automatically safe to approach or enter.
- **People and animals:** visible detections, possible occlusion, safe approach distance, accessible evacuation routes and human-operator confirmation before close contact.
- **Platform limits:** distinct verified envelopes for drone wind/battery/communications, ground-robot traction/tilt/waterproofing, and boat stability/current/payload. Never assume a capability transfers between platforms.
- **Communications and localization:** GPS denial, map freshness, sensor failure, blocked radio links and loss of operator contact.

### Required decision states

1. **Proceed in simulation / controlled test:** only when required inputs are available and the route satisfies the configured test limits.
2. **Caution / request human review:** uncertainty, conflicting sensors, degraded localization, unverified map data, or possible hazards.
3. **Stop and safe-hold:** hazard threshold exceeded, sensor data stale or missing, communications lost when required, unstable terrain, or platform envelope unknown.
4. **Replan / hand off:** use another platform or route only after its own limits and the transfer path are checked.

Do not hard-code universal flood thresholds from this document. Thresholds must be explicit configuration values tied to a named platform, evidence source and test case. Unknown values should fail safe, not default to zero risk. Log the input values, uncertainty, selected state, reason and timestamp for every decision.

### Simulation test matrix (planned; not yet implemented or run)

| Scenario | Hazard to represent | Expected safety behaviour |
|---|---|---|
| Shallow water, stable mapped road | Low depth but ordinary perception uncertainty | Proceed only within the configured platform envelope; log the decision |
| Fast current despite low depth | Depth alone gives a misleading impression | Stop or request review when current is unknown or exceeds the platform limit |
| Deep water with debris | Logs, floating objects and submerged obstacles | Keep ground robot in safe-hold at the existing 5.5 m boundary and above; do not claim boat safety without separate validation |
| Eroded bank / hidden drop | Route edge is unstable or occluded | Block the route or request human review |
| Damaged bridge / standing building | Structure may look intact but stability is unknown | Do not enter or cross without an independent safety clearance |
| Sensor disagreement or stale readings | Water/terrain sensors conflict or data are outdated | Fail safe and record the reason |
| GPS or communications loss | Localization or operator link degrades | Apply the platform-specific lost-link safe state |
| Drone survey identifies an alternate path | Multi-platform handoff | Ground/boat platform must independently re-assess the route before movement |

### Verification evidence to add later

- Unit tests for missing, stale, out-of-range and conflicting hazard inputs.
- Tests that confirm each decision state and its reason are logged.
- Regression tests for the existing ground-robot 5.5 m-and-above safe-hold boundary.
- Scenario-based simulation reports with pass/fail criteria defined before running.
- Separate controlled validation for each physical platform before any real-world capability claim.

**Implementation status:** this section documents requirements and planned tests only. It does not mean terrain-aware hazard logic, sensors, or physical rescue capabilities have already been implemented or validated.
