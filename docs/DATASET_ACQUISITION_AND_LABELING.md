# Free dataset sourcing, annotation and training plan

Last reviewed: 18 October 2026

## Cost and rights rules

- Use downloads and local tools only. Do not call paid APIs, hosted training services, paid notebooks or cloud GPUs.
- Do not commit downloaded image archives, model weights, credentials or private data to Git.
- A public download is not automatically cleared for reuse. Record the dataset's own licence and attribution requirements before use.
- A source is eligible for the training manifest only after a person confirms the licence/terms. Do not mark a dataset approved merely because it is downloadable.
- Keep original source labels separate from our labels. Human review is required before labels are marked `human_verified`.

## Candidate sources

| Source | Useful for | Labels and limits | Licence / decision |
|---|---|---|---|
| [FloodNet supervised dataset](https://github.com/BinaLab/FloodNet-Supervised_v1.0) | Aerial post-flood scene understanding; water, flooded/non-flooded buildings and roads, trees, vehicles, pools, grass | 2,343 images with semantic segmentation labels and published train/validation/test partitions. This is not a ground-level rescue-person dataset; the listed classes do not include people. | Repository states Community Data License Agreement (permissive). Read the [CDLA-Permissive 1.0 terms](https://cdla.io/permissive-1-0/) and preserve citation/attribution. Candidate for flood-hazard segmentation after local licence review. |
| [DECIDE Floodwater Dataset](https://decide.ugent.be/datasets/floodwater/) | Aerial water segmentation; useful for flood-extent mapping | 231,024 frames with SAM2-assisted pseudo-labels split by source video (train/validation/test), plus a separate 700-image manually annotated evaluation set. Labels indicate visible water, not necessarily floodwater; pseudo-labels are not independent manual ground truth. | Dataset/code page states GPL-3.0. Review obligations before redistribution or reuse. Candidate for water segmentation; do not mix its evaluation set into training. |
| [FloodIMG paper and dataset description](https://pmc.ncbi.nlm.nih.gov/articles/PMC10164831/) | Flood-related image segmentation research | More than 9,200 images described in the paper. Images were collected from multiple sources, including social media and government sites; rights may vary by image/source. | Do not bulk-reuse until item-level source rights and terms are verified. Article being open access does not automatically relicense every image. |
| [FloodNet NYC sensor data](https://www.floodnet.nyc/methodology) | Flood-depth/event context and sensor-data experiments | Mostly sensor/time-series data, not an image detection dataset. | Public access; review the project's data access terms before reuse. |

## Recommended local workflow

1. Download FloodNet only from the linked project source; keep its original train/validation/test assignment. Do not randomly mix images across splits.
2. Record source URL, dataset version/date, licence URL/status, attribution, archive checksum and local extraction path in a local manifest.
3. Review image/mask pairs visually. Do not invent person boxes from the flood-hazard segmentation masks.
4. For a separate rescue-person detector, identify a distinct, rights-cleared person-in-disaster dataset. FloodNet alone cannot train or validate a person detector because its published classes do not include people.
5. Use a free local annotator such as [CVAT Community](https://github.com/cvat-ai/cvat) or [Label Studio Community](https://github.com/HumanSignal/label-studio) only after checking their current self-hosted setup and licence. No hosted paid tier is required.
6. Have a human reviewer check class definitions, missing objects, boundaries and difficult/occluded examples. Preserve the original annotations and log every correction.
7. For any new dataset, split by incident/location/video/flight/source group—not by individual frame—to reduce leakage. Keep the test set untouched until model selection is complete.
8. Train locally with an open-source framework and a compatible, licence-cleared checkpoint. If local hardware cannot handle training, pause rather than silently use a paid cloud GPU.
9. Report the dataset version, source counts, split counts, label-review protocol, model/checkpoint licence, command, software versions, hardware, seed, precision/recall/IoU as appropriate, false negatives, latency and failure examples.

## Label policy

- `unreviewed`: downloaded or imported; label correctness unknown.
- `review_needed`: an annotator has proposed labels but no independent check is complete.
- `human_verified`: a reviewer has checked the image and labels against the documented class guide.
- `excluded`: rights unclear, corrupt, duplicate, irrelevant or unsuitable.

Never treat a downloaded dataset's original labels as human-verified by this project without actually reviewing them. Preserve the source's original labels and provenance.

## Status

No dataset has been downloaded, relabelled, or trained by this documentation change. FloodNet is a suitable candidate for **flood-hazard segmentation**, not sufficient by itself for rescue-person detection. Metrics must wait until a compatible model is trained and evaluated on a fixed, held-out set.
