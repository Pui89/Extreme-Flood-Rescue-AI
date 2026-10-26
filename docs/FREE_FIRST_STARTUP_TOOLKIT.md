# Free-First Product and Engineering Toolkit

This project is built free-first. Prefer local simulation, synthetic scenarios, standard-library checks and existing GitHub automation before installing larger robotics stacks or paying for hosted compute.

## Recommended workflow

1. **Define the scenario:** record water depth, current/flow assumptions, visibility, obstacles, communications, victim state, and the robot/boat/drone role. Separate simulated assumptions from measured environmental data.
2. **Run the safe local preflight:** `python tools/pui89_master_verify.py`. This checks syntax and inventories verification tools; it does not prove navigation or rescue capability.
3. **Test components independently:** evaluate detection, mapping/localisation, path planning, communication loss, energy limits, and fail-safe behaviour separately before testing the combined system.
4. **Use simulation before hardware:** prefer existing project tests first. Add ROS 2, Gazebo or other simulators only when a specific scenario requires them and the local machine can support them.
5. **Customer discovery:** record feedback from emergency responders and flood-affected communities, including operational constraints, safety requirements and realistic procurement/trial pathways. Do not imply operational readiness from concept visuals.

## Free-first tool choices

| Need | First choice | Guardrail |
|---|---|---|
| Code review and issue tracking | GitHub issues and pull requests | Keep design decisions and risks traceable |
| Repeatable checks | Existing GitHub Actions and local verification | Use short, dependency-light jobs |
| Scenario testing | Small deterministic synthetic cases | Synthetic results do not validate real flood performance |
| Robotics simulation | Existing tests first; ROS 2/Gazebo only when needed | Check platform support, disk/RAM and install costs before setup |
| Evidence reports | Versioned JSON/Markdown reports | Include assumptions, failed cases and software versions |
| Public project page | GitHub Pages or existing site | Clearly label concepts and simulated imagery |

## Cost and safety rules

- No paid API, cloud GPU, subscription, or automatic model download is required by this guide.
- Never connect an unvalidated autonomy stack to a real rescue mission.
- Test loss of GPS, network, power, sensor inputs, and safe stopping/recovery paths explicitly.
- Use synthetic or permissioned data; document provenance and licence terms.
- Treat 1–6 m water-depth scenarios as test targets, not proven operating limits, unless backed by suitable measurements and validated hardware tests.

## Definition of done for each upgrade

Document the requirement, scenario, expected result, actual result, failure handling and remaining risk. Passing software checks does not certify a robot for life-safety operations.
