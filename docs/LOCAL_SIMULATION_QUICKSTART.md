# Local Flood Rescue Simulation (No Dependencies)

This is the first runnable, local-only robotics demonstration for Flood Rescue AI. It uses only the Python standard library; it does not download model weights, install packages, call APIs, use a cloud GPU, or connect to hardware.

## Evidence status

- **Implemented by this demo:** deterministic grid map, shortest-path planning around synthetic blocked cells, simulated rover movement, synthetic possible-person markers, event log, JSON/CSV export, and an injected communications-loss safe-stop scenario.
- **Simulated results:** outputs from running this script on the generated grid. These validate only the script's stated grid behavior.
- **Not implemented or validated here:** camera perception, trained victim detector, flood physics, ROS 2/Gazebo integration, SLAM, depth/LiDAR, real-time control, physical robot, or field rescue performance.
- **Proposed next:** connect the simulator interface to Gazebo Sim / ROS 2 after the pure-Python baseline and tests are reproducible.

## Interactive visual demo

A separate browser-native visual version is available at [`demos/visual_flood_sim.html`](../demos/visual_flood_sim.html). It uses synthetic cells and markers and needs no Python packages.

From the repository root on Windows, you can double-click `demos\\visual_flood_sim.html` to open it in a browser. If your browser restricts local files, run this built-in Python web server from the repository root:

```bat
python -m http.server 8000
```

Then open `http://localhost:8000/demos/visual_flood_sim.html` and stop the server with Ctrl+C when finished. This is local-only and does not use a hosted API or cloud service.

The page supports one-step movement, autoplay/pause, reset, and injected communication-loss/unknown-hazard stop scenarios. The visual demo is separate from the Python CLI simulator and does not replace its automated tests.

## Windows setup

Install Python 3.10 or newer from the official Python distribution if it is not already installed. No third-party package is required for this demo.

Open **Command Prompt** and run:

```bat
git clone https://github.com/Pui89/Flood-Rescue-AI.git
cd Flood-Rescue-AI
python --version
python scripts\flood_rescue_sim.py
```

If you already cloned the repository, do not clone it again. Open Command Prompt in the existing repository folder and run:

```bat
python scripts\flood_rescue_sim.py
```

The command creates `runs\flood_rescue_sim.json` and `runs\flood_rescue_sim.csv`. The JSON contains the scenario and limitations; the CSV contains step-by-step simulated events.

## Repeatable runs and fault injection

```bat
python scripts\flood_rescue_sim.py --seed 7 --out runs\baseline
python scripts\flood_rescue_sim.py --seed 7 --fail-comms-at 2 --out runs\comms_failure
python -m unittest discover -s tests -v
```

The seed makes the synthetic confidence numbers repeatable. The timestamp in the JSON naturally changes between runs. The communication failure is injected by the simulator and is not a real radio test.

## Reading the map

- `S`: start; `R`: rover's final simulated position; `G`: observation waypoint.
- `P`: synthetic possible-person marker; `~`: blocked water; `#`: blocked debris/structure.
- `?`: unknown cell that must remain unknown; `*`: planned path; `.`: unclassified free cell.

The simulated person markers are scripted scenario labels, not output from an AI vision model. Reaching an observation waypoint is not a rescue and does not prove that the route is safe in a real flood.

## Safety boundary

Use only for software development and learning. Do not connect this script to motor drivers or deploy a physical robot in floodwater. Any later physical test must start on dry, level, controlled ground with an independent emergency stop, an observer, and a documented risk assessment.
