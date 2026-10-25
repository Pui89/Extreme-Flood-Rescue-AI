# Local Agentic AI Options — Extreme Flood Rescue AI

1. Keep the existing standard-library project agent, world-state tracker and safety supervisor as the always-available baseline. Multi-agent grid outputs are toy scenario evidence, not flood physics.

2. If an LLM would help summarize scenarios or draft mission alternatives, evaluate Ollama with a small, already-present, licence-reviewed model. Do not run a pull/download command automatically.

3. Use LangGraph only if the workflow needs explicit stateful branches for sensor checks, target evidence, hazard review, communications and operator approval. Use smolagents only for tightly allowlisted read-only tools; avoid unrestricted code execution. PydanticAI is a reasonable alternative for structured typed proposals and test-model-based evaluation.

4. Simulate the same fixed scenarios with and without the agent. Record false negatives, false alarms, UNKNOWN/abstention cases, safe-hold outcomes, latency and memory. A better-written plan is not proof of improved rescue performance.

## Free/open-source agent options

| Resource | What it contributes | Licence / cost boundary | Local availability check |
|---|---|---|---|
| [smolagents](https://github.com/huggingface/smolagents) | Small tool-using agent framework; supports local Transformers/Ollama model paths. | Apache-2.0 library. A hosted model, tool, sandbox or external service may introduce separate costs. Code-executing agents are high risk; use only the minimal tool-calling path. | Python module \`smolagents\` |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Explicit, stateful agent/workflow graphs, branching, retries and review checkpoints. | MIT-licensed library. Keep orchestration local; hosted observability/deployment products are optional and are not part of this plan. | Python module \`langgraph\` |
| [PydanticAI](https://github.com/pydantic/pydantic-ai) | Typed agent I/O, validation-friendly interfaces and test/evaluation helpers. | MIT-licensed library. Provider choice determines whether inference is local or billed. Built-in test models are for workflow tests, not real inference. | Python module \`pydantic_ai\` |
| [Ollama](https://github.com/ollama/ollama) | Local model runtime on a supported desktop. | MIT-licensed runtime; each downloaded model has its own licence and size. Do not use hosted providers or pull weights without an explicit resource/licence check. | Executable \`ollama\` |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Local inference runtime for supported GGUF models; useful as an alternative to Ollama. | MIT-licensed runtime; model weights and bundled components retain their own terms. Building from source can require disk and build tools. | Executable \`llama-cli\` or \`llama-server\` |

The probe checks only whether a local Python module or executable appears to exist; it does **not** download anything, launch a server, inspect model weights or verify model licences. Both frameworks and runtimes are optional.

## Recommended implementation pattern

Use the existing project-specific rule-based agent as the baseline. If the workload later justifies it, place a local agent framework around this controlled pipeline:

\`\`\`text
read-only evidence tools
    -> specialist proposal(s)
    -> typed schema / provenance validation
    -> deterministic project safety supervisor
    -> human review or UNKNOWN / SAFE_HOLD
    -> reproducible report
\`\`\`

Keep the following boundaries:
- No paid API keys, cloud inference, hosted agents or network-search tools are required by this design.
- No automatic \`pip install\`, model pull, model download, container build or server startup.
- Only explicitly allowlisted, read-only tools; no general shell, arbitrary Python execution, filesystem mutation or self-modifying agent.
- Enforce bounded tool calls/retries, explicit timeouts, schema validation and auditable input references.
- Treat LLM output as untrusted proposals. The deterministic supervisor outranks every agent.
- Never let an agent publish motor, cutter, propulsion, navigation, flight, boat, screening-enforcement or other actuator commands.
- Capture model ID/version/licence, prompt/config revision, evidence hashes, latency, resource use, failures and reviewer outcome when an actual model test is later run.

## Cost-safe adoption gates

1. **Now:** use the existing standard-library agent and unit tests; no framework installation needed.
2. **Later:** run the optional-resource checker. Compare the current deterministic baseline first and verify free disk, RAM and GPU memory.
3. **Choose one framework, not all three.** Try LangGraph when explicit graph/state behaviour is needed; try smolagents for a small allowlisted tool loop; try PydanticAI for strict typed interfaces and evaluation.
4. **Choose one local inference runtime at most initially** (Ollama *or* llama.cpp), then manually review the exact model licence and download size before acquiring weights.
5. **Keep model inference optional in CI.** Use deterministic fake/test models for unit tests; do not require model weights or network access for core tests.

No framework or runtime is installed by this documentation change. Software licences do not waive the separate terms of model weights, datasets, plugins, or dependent tools.

## Project-specific agent roles

- **Sensor-health agent:** Check freshness, validity and communications; report UNKNOWN when required data are missing.
- **Reconnaissance evidence agent:** Summarize operator-provided detections and image/depth evidence without pretending a model has run.
- **Hazard reviewer:** Check the declared simulation scenario, obstacles and hazard flags; never infer real water depth from a generic image.
- **Mission planner:** Propose, but do not execute, a simulation-only search sequence for human review.
- **Safety supervisor and evidence reporter:** Force safe-hold for missing/stale/conflicting inputs and save repeatable scenario evidence.

## Safety boundary

No agent may send navigation, propulsion, drone, boat or rescue-actuator commands. Simulated depth labels—including 0–15 m scenarios—do not validate real-world depth, buoyancy, waterproofing, current handling or rescue capacity.


## Run the current local agentic workflow

The current coordinator is intentionally model-optional. To execute its existing deterministic project agent against a synthetic example, run this from the repository root:

    python -m tools.run_agentic_workflow --input examples/agentic_workflow.synthetic.json

Or pipe JSON into it in Windows Command Prompt:

    type examples\agentic_workflow.synthetic.json | python -m tools.run_agentic_workflow

It prints one JSON report containing the project decision, validation trace, evidence SHA-256 and explicit flags stating that no network, model inference, execution or actuator command was used. A result called \`PROPOSAL_READY_FOR_HUMAN_REVIEW\` means a proposal was created; it is **not** a robot-ready or approved action. Inspect the nested \`decision.status\`, \`decision.recommendation\`, \`issues\` and \`trace\`.

The example input is synthetic software-test data only. Values are not real detector outputs, physical sensor measurements, validated water depths, or authorization to operate a robot. Do not use these examples for real harvesting, rescue or screening decisions.
