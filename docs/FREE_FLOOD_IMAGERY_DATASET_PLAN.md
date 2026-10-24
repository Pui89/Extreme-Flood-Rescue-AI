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
| [Nepal flood event imagery and maps — Sentinel Asia](https://sentinel-asia.org/EO/2024/article20240730NP.html) | Event-specific satellite images and flood-proxy products for Nepal, including Kathmandu/B bagmati-region events in 2024 | **Reference/source-discovery only until each download's licence and reuse permission are confirmed** | Valuable for finding real Nepal event examples. Do not assume every partner product can be freely reused or redistributed; some are analysis products rather than labelled training images. |
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
