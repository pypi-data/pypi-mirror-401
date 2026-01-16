# vvpg_robots_go2_sdk

Python SDK for VVPGRobots / Unitree Go2 (runtime: ROS2 Humble).
This package is intentionally **ROS-agnostic at install time**:
- `pip install` does NOT pull `rclpy` or ROS message packages;
- ROS dependencies must be present in the runtime (container/host) via ROS installation + overlay.

## Install

```bash
pip install vvpg_robots_go2_sdk==1.0.0
```

Usage
from vvpg_robots_go2_sdk import SportConfig, UnitreeMoveStreamer

cfg = SportConfig(topic="/api/sport/request", identity_id=0, rate_hz=20)
s = UnitreeMoveStreamer(cfg)

s.set_velocity(0.5, 0.0, 0.0)
# ...
s.stop()
s.close()