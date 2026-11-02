# Sprout 🌱

**A Spot-inspired quadruped robot, built entirely in simulation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Build Status](https://github.com/shantanuparabumd/sprout/actions/workflows/main.yml/badge.svg)


https://github.com/user-attachments/assets/f2344df4-ac7d-424a-8175-407aeae86478

Sprout was designed in SolidWorks, exported to URDF, and brought to life in Gazebo on ROS Noetic.
Every step is pre-solved with inverse kinematics and replayed at 200 Hz, and you drive it from your keyboard.

## Demo

https://github.com/shantanuparabumd/quad_robo/assets/112659509/1dbaa1dd-f1ca-4bd2-8f20-401817f208e4

## How it works

| Stage | What happens | Where |
|---|---|---|
| **CAD** | Body, hip, upper leg, shin and camera modelled in SolidWorks | `cad/` |
| **URDF** | Exported with SW2URDF: 12 revolute joints, 3 per leg | `urdf/`, `meshes/` |
| **Inverse kinematics** | Leg trajectories solved with DH parameters and the Jacobian method | `tools/inverse_kinematics/`, `tools/matlab/` |
| **Gaits** | Solved joint angles stored per leg as `[thigh, leg, shin]`, one row per 200 Hz tick | `src/gait/*.json` |
| **Control** | 12 effort-based position controllers (PID) via `ros_control` | `config/control.yaml` |
| **Teleop** | Keyboard script that replays a gait on each key press | `src/gait.py` |

## Requirements

- Ubuntu 20.04 (Focal Fossa)
- ROS Noetic (`ros-noetic-desktop-full`) with `gazebo_ros`, `ros_control` and `effort_controllers`
- Python 3, plus the `keyboard` package (`pip install keyboard`), which `src/gait.py` imports

## Quick start

```bash
# 1. Build inside a catkin workspace (the package name is quad_robo)
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone https://github.com/shantanuparabumd/sprout.git quad_robo
cd ~/catkin_ws && catkin_make && source devel/setup.bash

# 2. Spawn Sprout in Gazebo with its controllers
roslaunch quad_robo final.launch

# 3. In a second terminal, drive it
rosrun quad_robo gait.py
```

### Controls

| Key | Gait | Key | Gait |
|:---:|---|:---:|---|
| `w` | walk (fast trot) | `s` | stand |
| `a` | slide (right) | `d` | slide (left) |
| `q` | turn (right) | `e` | turn (left) |
| `x` | reverse | `j` | jump forward |
| `k` | jump in place | `c` | quit |

`launch/display.launch` opens the model in RViz with joint sliders.

## Repository layout

```
├── cad/                  SolidWorks parts and assemblies (robot + arena)
├── config/               ros_control controller configuration
├── docs/media/           Images and the launch video
├── launch/               final.launch (Gazebo + controllers), display.launch (RViz), …
├── meshes/               STL meshes referenced by the URDFs
├── src/                  gait.py (keyboard teleop) and gait/*.json (solved gaits)
├── tools/
│   ├── inverse_kinematics/   Jupyter notebooks and scripts that generate the gaits
│   └── matlab/               Per-leg MATLAB kinematics
├── urdf/                 Robot (quad_robo) and arena (field) descriptions
└── worlds/               Gazebo worlds
```

## Author

**Shantanu Parab**: [@shantanuparabumd](https://github.com/shantanuparabumd)

## Documents

- [AIP Sheet](https://docs.google.com/spreadsheets/d/10HzXxKAx0vlCkuSPjUT41-QAT8gSsVI4Um7Ahq-aHGc/edit?usp=sharing)

## License

MIT, see [LICENSE](LICENSE).
