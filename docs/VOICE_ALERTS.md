# Flood Rescue AI — Local Voice Alerts

## Purpose

Read out evidence-based flood and rescue-coordination messages to a human operator. Voice output is not a substitute for official alerts or trained incident command.

This is an **optional local text-to-speech (TTS) layer**. It does not add or validate the project's vision model, sensor integration, or real-world performance. No hosted inference API is required by the setup below, and no paid service should be enabled.

## Recommended models

- **English:** [Kokoro-82M on Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M) — model card lists the Apache-2.0 license.
- **Thai / multilingual experiment:** [SakThai TTS on Hugging Face](https://huggingface.co/Nanthasit/sakthai-tts-model) — model card lists MIT for this packaging and describes local GGUF CPU inference. Thai-script output is described as experimental; test pronunciation and numbers before operational use.
- Use the model files locally. Do not use Hugging Face hosted Inference Providers or other hosted APIs if the requirement is zero usage charges.

Check the current model card and any included voice/data licenses before redistribution or commercial deployment.

## Local English smoke test (Kokoro)

Install dependencies yourself in a virtual environment on a computer you control. The first run may download model files and therefore needs internet access and disk space. Runtime is local after the required files are available.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install "kokoro>=0.9.2" soundfile
```

Kokoro's official model card also lists `espeak-ng` as a dependency on Linux-based setups. Follow the model's current installation instructions for your operating system.

Create `tts_smoke_test.py`:

```python
from kokoro import KPipeline
import soundfile as sf

# 'a' selects the American English pipeline.
pipeline = KPipeline(lang_code="a")
text = "Voice system test. This is an advisory message only."

for index, (_graphemes, _phonemes, audio) in enumerate(
    pipeline(text, voice="af_heart")
):
    sf.write(f"voice_test_{index}.wav", audio, 24000)
    print(f"Saved voice_test_{index}.wav")
```

Run `python tts_smoke_test.py`, then play the WAV file locally. This is a manual test only; it does not connect TTS to the project's live detection pipeline.

## Example messages for this project

- “Flood risk indicator received. Verify the source and timestamp.”
- “Possible person detected. Human review required.”
- “Route information is uncertain. Do not rely on this suggestion without field verification.”

## Safety requirements

- Only speak alerts tied to actual sensor, forecast, or operator inputs; include timestamps and source status in the application record.
- Do not say that a person has been rescued or that a route is safe unless an authorized, verified source confirms it.
- Keep rescue decisions with trained responders. Speech synthesis must not dispatch robots or people.

## Cost and privacy checklist

- [ ] Use local inference only; do not configure a hosted inference endpoint or API key.
- [ ] Do not add billing-enabled cloud services to the workflow.
- [ ] Do not commit model weights, generated audio, private case data, credentials, or API tokens to Git.
- [ ] Test messages with recorded/simulated inputs before any field use.
- [ ] Provide a visual/text fallback if audio fails or the environment is too noisy.
- [ ] Verify language, pronunciation, latency, accessibility, and model license before deployment.

**Status:** Integration guide and smoke-test example only. The model is not automatically installed, the voice output is not yet connected to live project events, and no field-safety validation is claimed.
