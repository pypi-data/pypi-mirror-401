from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass
from typing import Optional, Tuple, Any


# Unitree Sport API IDs
API_MOVE = 1008
API_STOPMOVE = 1003
API_SWITCH_JOYSTICK = 1027


@dataclass
class SportConfig:
    topic: str = "/api/sport/request"
    identity_id: int = 0
    rate_hz: float = 20.0
    sign_x: float = 1.0
    sign_y: float = 1.0
    sign_z: float = 1.0


def _require_ros() -> Tuple[Any, Any, Any, Any, Any, Any]:
    """
    Lazy import ROS2 deps.
    Возвращает: (rclpy, Node, QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, UTRequest)
    """
    try:
        import rclpy
        from rclpy.node import Node
        from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy
        from unitree_api.msg import Request as UTRequest
        return rclpy, Node, QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, UTRequest
    except Exception as e:
        raise RuntimeError(
            "ROS2 runtime is not available for vvpg_robots_go2_sdk.\n"
            "Expected environment:\n"
            "  - ROS 2 installed (e.g. Humble) and sourced: /opt/ros/humble/setup.bash\n"
            "  - unitree_api messages available in the overlay (so `from unitree_api.msg import Request` works)\n"
            "Typical fix inside container:\n"
            "  source /opt/ros/humble/setup.bash && source /opt/overlay/install/setup.bash\n"
            "Then run your python entrypoint.\n"
            f"Original import error: {type(e).__name__}: {e}"
        ) from e


class UnitreeMoveStreamer:
    """
    Минимальный слой движения через Unitree Sport API:
      - set_velocity(x,y,z): включает streaming
      - stop(): выставляет 0 и выключает streaming
      - close(): освобождает ресурсы (и shutdown rclpy если мы его init’или)
    """

    def __init__(self, cfg: Optional[SportConfig] = None) -> None:
        self.cfg = cfg or SportConfig()

        rclpy, Node, QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, UTRequest = _require_ros()
        self._rclpy = rclpy
        self._UTRequest = UTRequest

        class _RosNode(Node):
            def __init__(self) -> None:
                super().__init__("vvpg_sdk_move_server")

        if not self._rclpy.ok():
            self._rclpy.init(args=None)
            self._owns_rclpy = True
        else:
            self._owns_rclpy = False

        self._node = _RosNode()

        qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        self._pub = self._node.create_publisher(self._UTRequest, self.cfg.topic, qos)

        self._lock = threading.Lock()
        self._vx = 0.0
        self._vy = 0.0
        self._wz = 0.0
        self._streaming = False
        self._joystick_on = False

        self._stop_evt = threading.Event()
        self._thr = threading.Thread(target=self._loop, name="unitree_move_stream", daemon=True)
        self._thr.start()

    def set_velocity(self, linear_x: float, linear_y: float, angular_z: float) -> None:
        with self._lock:
            self._vx = self.cfg.sign_x * float(linear_x)
            self._vy = self.cfg.sign_y * float(linear_y)
            self._wz = self.cfg.sign_z * float(angular_z)
            self._streaming = True

    def stop(self) -> None:
        with self._lock:
            self._vx = self._vy = self._wz = 0.0
            self._streaming = False
        self._send_stop()

    def close(self) -> None:
        self._stop_evt.set()
        self._thr.join(timeout=2.0)

        try:
            self._node.destroy_publisher(self._pub)
            self._node.destroy_node()
        except Exception:
            pass

        if self._owns_rclpy:
            try:
                self._rclpy.shutdown()
            except Exception:
                pass

    # ---------- internal ----------

    def _mk_msg(self, api_id: int, parameter_obj: Optional[dict], noreply: bool):
        m = self._UTRequest()
        m.header.identity.id = int(self.cfg.identity_id)
        m.header.identity.api_id = int(api_id)
        m.header.lease.id = 0
        m.header.policy.priority = 0
        m.header.policy.noreply = bool(noreply)
        m.parameter = "" if parameter_obj is None else json.dumps(parameter_obj, separators=(",", ":"))
        m.binary = b""
        return m

    def _publish(self, msg) -> None:
        self._pub.publish(msg)

    def _send_switch_joystick(self, enable_default_controller: bool) -> None:
        self._publish(self._mk_msg(API_SWITCH_JOYSTICK, {"data": bool(enable_default_controller)}, noreply=True))

    def _send_move(self, vx: float, vy: float, wz: float, noreply: bool) -> None:
        self._publish(self._mk_msg(API_MOVE, {"x": float(vx), "y": float(vy), "z": float(wz)}, noreply=noreply))

    def _send_stop(self) -> None:
        self._publish(self._mk_msg(API_STOPMOVE, None, noreply=True))
        self._send_move(0.0, 0.0, 0.0, noreply=True)

    def _loop(self) -> None:
        period = max(0.001, 1.0 / float(self.cfg.rate_hz))
        while not self._stop_evt.wait(period):
            with self._lock:
                if not self._streaming:
                    if self._joystick_on:
                        try:
                            self._send_move(0.0, 0.0, 0.0, noreply=True)
                            self._send_switch_joystick(True)
                        finally:
                            self._joystick_on = False
                    continue

                moving = (abs(self._vx) + abs(self._vy) + abs(self._wz)) > 1e-6
                if moving and not self._joystick_on:
                    self._send_switch_joystick(False)
                    self._joystick_on = True

                self._send_move(self._vx, self._vy, self._wz, noreply=True)
