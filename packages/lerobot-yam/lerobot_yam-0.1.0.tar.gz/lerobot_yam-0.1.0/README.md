# LeRobot YAM Plugins

This repo contains LeRobot plugins for the YAM arm, split into a shared core
package plus follower and leader plugins.

This is the top-level meta package for PyPI. Install subpackages for local
development, or install this meta package once all subpackages are published.

## Packages

| Package | Purpose |
| --- | --- |
| `yam-common` | Shared YAM utilities (motor chain, gravity comp, gripper utils) |
| `lerobot_robot_yam` | Follower robot plugin (executes actions) |
| `lerobot_teleoperator_yam_gello` | Leader teleoperator plugin (produces actions) |

## Install

Install everything in one editable command:

```bash
pip install -e .
```

If you only need one component (for example, just the follower to run a policy),
install it separately:

```bash
pip install -e ./lerobot_robot_yam
pip install -e ./lerobot_teleoperator_yam_gello
pip install -e ./yam_common
```

Note: `pip install -e .` assumes the subpackages are installable (e.g., published).
For local dev installs, use `requirements.txt`:

```bash
pip install -r ./requirements.txt
```

## Usage

See `yam.md` for end-to-end teleop and recording examples. Typical CLI use:

```bash
lerobot-teleoperate \
  --robot.type=yam_follower \
  --robot.port=can0 \
  --robot.gripper_type=crank_4310 \
  --teleop.type=yam_leader \
  --teleop.port=/dev/ttyUSB0
```

