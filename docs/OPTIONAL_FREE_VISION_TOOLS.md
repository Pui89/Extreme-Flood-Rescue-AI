# Optional Free Vision and 3D Perception Resources

These tools support perception research and local evaluation; they do not validate rescue capability, waterproofing, buoyancy or operation at any specific real-world flood depth.

## Recommended order

1. **OpenCV** — local image decoding/quality checks, frame comparisons and QA overlays for day/night, rain, glare, blur and camera degradation.
2. **Open3D** — optional tools for genuine depth images, point clouds, registration and 3D scene inspection. Use only when compatible sensor data or a simulation produces the inputs.
3. **CVAT Community** — optional self-hosted annotation/review for licensed images and footage, including labels for people, animals, debris and visible hazards.
4. **OpenVINO** — later CPU-inference benchmark if an actual model benefits on the target system.
5. **Tesseract OCR** — low priority; only useful when extracting visible text such as warning signs, not detecting people or measuring water depth.

## Free-resource register

| Resource | Local check | Licence note | Official source |
|---|---|---|---|
| OpenCV Python (cv2) | Python module | OpenCV 4.5.0+ is Apache-2.0; older releases have different terms and bundled dependencies may differ. | [Licence](https://opencv.org/license/) · [Project](https://github.com/opencv/opencv) |
| Open3D | Python module (open3d) | MIT. Check the exact release and bundled dependencies. | [Project and licence](https://www.open3d.org/) |
| CVAT Community | Manual/self-hosted service check | Community core is MIT; review FFmpeg and third-party asset/dependency licences too. | [Community repository](https://github.com/cvat-ai/cvat) · [Licence overview](https://docs.cvat.ai/docs/getting_started/overview/) |
| OpenVINO | Python module (openvino) | Apache-2.0 toolkit; model weights retain their own licences. | [Official repository](https://github.com/openvinotoolkit/openvino) |
| Tesseract OCR engine | tesseract executable | Apache-2.0; language data and distribution packages have their own details. | [Official documentation](https://tesseract-ocr.github.io/tessdoc/) |

## Check what is already available

Run from the repository root:

    python tools/check_optional_resources.py

The command emits JSON to the terminal and checks only local module metadata/PATH entries. It makes no network requests, installs no packages and downloads no model weights. A resource marked **manual_check** (such as CVAT Community) is deliberately not treated as installed or running.

## Simulation and safety boundary

Test each perception path against explicit conditions: water-level scenario, camera height/view, rain/night, glare, occlusion, sensor dropout and communication delay. Open3D point-cloud geometry does not measure water depth unless it is derived from a calibrated sensor and validated frame of reference. An OpenCV image-quality statistic is not a rescue-success metric. A scenario label such as 0–15 m is not proof of vehicle capability. Keep outputs advisory, preserve an operator-approved safe-hold path and report negative as well as positive cases.

No dependency is added to the core install. No install, model inference or benchmark is performed by the probe.