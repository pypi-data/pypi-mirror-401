# leafsdk/core/mission/mission_plan_step.py
import numpy as np
import inspect
import traceback
from typing import Dict, Any, Optional, Tuple, Union, Sequence, Literal
from abc import ABC, abstractmethod

from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons
from leafsdk.utils.util import normalize_param_to_size as normalize_param
from leafsdk.utils.util import validate_waypoint_param


Tuple3D = Tuple[float, float, float]   # exact length 3


class MissionPlanStep(ABC):
    def __init__(self):
        self._is_pausable = True # Indicates if the step can be paused
        self._is_cancelable = True # Indicates if the step can be cancelled

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def description(self) -> str:
        """
        Returns a string description of the step.
        This is used for logging and debugging purposes.
        """
        pass

    @classmethod
    def init_from_dict(cls, params: Dict[str, Any]):
        sig = inspect.signature(cls.__init__)
        required_params = [
            name
            for name, p in sig.parameters.items()
            if name != "self" and p.default is inspect.Parameter.empty
        ]

        # validate required params
        missing = [p for p in required_params if p not in params]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")

        return cls(**params)

    def log_info(self):
        logger.info(f"{LogIcons.RUN} Executing step: {self.description()}")

    def is_pausable(self) -> bool:
        """Returns True if the step can be paused."""
        return self._is_pausable
    
    def is_cancelable(self) -> bool:
        """Returns True if the step can be cancelled."""
        return self._is_cancelable


class _GotoBase(MissionPlanStep):
    def __init__(
            self,
            waypoints: Union[Tuple3D, Sequence[Tuple3D]],
            yaws_deg: Union[float, Sequence[float]],
            speed: Optional[Union[float, Sequence[float]]] = 0.2,                       # 0.2 m/s,
            yaw_speed: Optional[Union[Sequence[float], Literal["sync"]]] = "sync",      # Synced with position trajectory,
            cartesian: Optional[bool] = False,
            average_deceleration: float = 0.5 # m2/s
        ):
        super().__init__()
        
        if isinstance(yaw_speed, str):
            assert yaw_speed == "sync", f"yaw_speed string value must be 'sync', got '{yaw_speed}'"

        self.waypoints = waypoints
        self.yaws_deg  = yaws_deg
        self.speed     = speed
        self.yaw_speed = yaw_speed
        self.cartesian = cartesian
        self.target_waypoint = self.waypoints[-1]  # Last waypoint is the target
        self.target_yaw = self.yaws_deg[-1]  # Last yaw is the target
        self.average_deceleration: float = average_deceleration

    def to_dict(self):
        return {
            "waypoints": self.waypoints.tolist(),
            "yaws_deg": self.yaws_deg.tolist(),
            "speed": self.speed.tolist(),
            "yaw_speed": self.yaw_speed if isinstance(self.yaw_speed, str) else self.yaw_speed.tolist(),
            "is_pausable": self._is_pausable,
            "average_deceleration": self.average_deceleration
        }

    def description(self) -> str:
        """
        Returns a string description of the step.
        This is used for logging and debugging purposes.
        """
        return f"Goto to waypoint {self.target_waypoint} with yaw {self.target_yaw}."

class GotoGPSWaypoint(_GotoBase):
    def __init__(
        self,
        waypoints: Union[Tuple3D, Sequence[Tuple3D]],
        yaws_deg: Optional[Union[float, Sequence[float]]] = 0.0,                    # 0.0 deg,
        speed: Optional[Union[float, Sequence[float]]] = 0.2,                       # 0.2 m/s,
        yaw_speed: Optional[Union[float, Sequence[float], Literal["sync"]]] = "sync",      # Synced with position trajectory,
        is_pausable: bool = True,
        average_deceleration: float = 0.5 # m2/s
    ):
        waypoints = validate_waypoint_param(waypoints)
        n = waypoints.shape[0]
        yaws_deg  = normalize_param(yaws_deg, "yaws_deg", n)
        speed     = normalize_param(speed, "speed", n)
        yaw_speed = yaw_speed if isinstance(yaw_speed, str) else normalize_param(yaw_speed, "yaw_speed", n)
        super().__init__(waypoints=waypoints, yaws_deg=yaws_deg, speed=speed, yaw_speed=yaw_speed, cartesian=False, average_deceleration=average_deceleration)
        self._is_pausable = is_pausable

    def description(self) -> str:
        return f"GotoGPSWaypoint to ({self.target_waypoint[0]}, {self.target_waypoint[1]}, {self.target_waypoint[2]}) with yaw {self.target_yaw}."


class GotoLocalPosition(_GotoBase):
    def __init__(
        self,
        waypoints: Union[Tuple3D, Sequence[Tuple3D]],
        yaws_deg: Optional[Union[float, Sequence[float]]] = 0.0,                    # 0.0 deg,
        speed: Optional[Union[float, Sequence[float]]] = 0.2,                       # 0.2 m/s,
        yaw_speed: Optional[Union[float, Sequence[float], Literal["sync"]]] = "sync",      # Synced with position trajectory,
        is_pausable: bool = True,
        average_deceleration: float = 0.5 # m2/s
    ):
        waypoints = validate_waypoint_param(waypoints)
        n = waypoints.shape[0]
        yaws_deg  = normalize_param(yaws_deg, "yaws_deg", n)
        speed     = normalize_param(speed, "speed", n)
        yaw_speed = yaw_speed if isinstance(yaw_speed, str) else normalize_param(yaw_speed, "yaw_speed", n)
        super().__init__(waypoints=waypoints, yaws_deg=yaws_deg, speed=speed, yaw_speed=yaw_speed, cartesian=True, average_deceleration=average_deceleration)
        self._is_pausable = is_pausable

    def description(self) -> str:
        return f"GotoLocalPosition to ({self.target_waypoint[0]}, {self.target_waypoint[1]}, {self.target_waypoint[2]}) with yaw {self.target_yaw}."


class YawAbsolute(_GotoBase):
    def __init__(
        self,
        yaws_deg: Union[float, Sequence[float]],
        yaw_speed: Optional[Union[float, Sequence[float]]] = 30.0,    # 30.0 deg/s,
        is_pausable: bool = True,
        average_deceleration: float = 0.5 # m2/s
    ):
        n = len(yaws_deg)
        waypoints = [(0.0, 0.0, 0.0)]*n
        speed = np.ones((n,))
        yaws_deg  = normalize_param(yaws_deg, "yaws_deg", n)
        speed     = normalize_param(speed, "speed", n)
        yaw_speed = normalize_param(yaw_speed, "yaw_speed", n)
        super().__init__(waypoints=waypoints, yaws_deg=yaws_deg, speed=speed, yaw_speed=yaw_speed, cartesian=True, average_deceleration=average_deceleration)
        self._is_pausable = is_pausable

    def to_dict(self):
        return {
            "yaws_deg": self.yaws_deg.tolist(),
            "yaw_speed": self.yaw_speed.tolist(),
            "is_pausable": self._is_pausable,
            "average_deceleration": self.average_deceleration
        }

    def description(self) -> str:
        return f"YawAbsolute to yaw {self.target_yaw}."

class GotoRelative(_GotoBase):
    def __init__(
        self,
        waypoints: Union[Tuple3D, Sequence[Tuple3D]],
        yaws_deg: Optional[Union[float, Sequence[float]]] = 0.0,                    # 0.0 deg,
        speed: Optional[Union[float, Sequence[float]]] = 0.2,                       # 0.2 m/s,
        yaw_speed: Optional[Union[float, Sequence[float], Literal["sync"]]] = "sync",      # Synced with position trajectory,
        is_pausable: bool = True,
        average_deceleration: float = 0.5   # m2/s
    ):
        waypoints = validate_waypoint_param(waypoints)
        n = waypoints.shape[0]
        yaws_deg  = normalize_param(yaws_deg, "yaws_deg", n)
        speed     = normalize_param(speed, "speed", n)
        yaw_speed = yaw_speed if isinstance(yaw_speed, str) else normalize_param(yaw_speed, "yaw_speed", n)
        super().__init__(waypoints=waypoints, yaws_deg=yaws_deg, speed=speed, yaw_speed=yaw_speed, cartesian=True, average_deceleration=average_deceleration)
        self._is_pausable = is_pausable

    def description(self) -> str:
        return f"GotoRelative to position ({self.target_waypoint[0]}, {self.target_waypoint[1]}, {self.target_waypoint[2]}) with yaw {self.target_yaw}."

class YawRelative(_GotoBase):
    def __init__(
        self,
        yaws_deg: Union[float, Sequence[float]],
        yaw_speed: Optional[Union[float, Sequence[float]]] = 30.0,    # 30.0 deg/s,
        is_pausable: bool = True,
        average_deceleration: float = 0.5   # m2/s
    ):
        n = len(yaws_deg)
        waypoints = [(0.0, 0.0, 0.0)]*n
        speed = np.ones((n,))
        yaws_deg  = normalize_param(yaws_deg, "yaws_deg", n)
        speed     = normalize_param(speed, "speed", n)
        yaw_speed = normalize_param(yaw_speed, "yaw_speed", n)
        super().__init__(waypoints=waypoints, yaws_deg=yaws_deg, speed=speed, yaw_speed=yaw_speed, cartesian=True, average_deceleration=average_deceleration)
        self._is_pausable = is_pausable

    def to_dict(self):
        return {
            "yaws_deg": self.yaws_deg.tolist(),
            "yaw_speed": self.yaw_speed.tolist(),
            "average_deceleration": self.average_deceleration
        }

    def description(self) -> str:
        return f"YawRelative to yaw {self.target_yaw}."

class Takeoff(MissionPlanStep):
    def __init__(self, alt: Optional[float] = 1.0):
        super().__init__()
        self._is_pausable = False  # Takeoff step cannot be paused
        self._is_cancelable = False  # Takeoff step cannot be cancelled
        self.alt = alt

    def to_dict(self):
        return {"alt": self.alt}
    
    def description(self) -> str:
        """
        Returns a string description of the step.
        This is used for logging and debugging purposes.
        """
        return f"Takeoff to altitude {self.alt}m."
    

class Wait(MissionPlanStep):
    def __init__(self, duration: float):
        super().__init__()
        self.duration = duration
        self.tick = 0 # Used to track the start time of the wait
        self._is_pausable = False

    def to_dict(self):
        return {"duration": self.duration}

    def description(self) -> str:
        """
        Returns a string description of the step.
        This is used for logging and debugging purposes.
        """
        return f"Wait for {self.duration} seconds."
    

class Land(MissionPlanStep):
    def __init__(self):
        super().__init__()
        self._is_pausable = False
        self._is_cancelable = False

    def to_dict(self):
        return {}
        
    def description(self) -> str:
        """
        Returns a string description of the step.
        This is used for logging and debugging purposes.
        """
        return "Land."
    

def step_from_dict(step_type: str, params: dict) -> MissionPlanStep:
    step_classes = {
        "Takeoff": Takeoff,
        "GotoGPSWaypoint": GotoGPSWaypoint,
        "GotoLocalPosition": GotoLocalPosition,
        "GotoRelative": GotoRelative,
        "YawAbsolute": YawAbsolute,
        "YawRelative": YawRelative,
        "Wait": Wait,
        "Land": Land,
        # Add more here
    }
    cls = step_classes.get(step_type)
    if cls is None:
        raise ValueError(f"Unknown mission_plan_step type: {step_type}")
    
    return cls.init_from_dict(params)