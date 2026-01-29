#leafsdk/core/utils/logstyle.py

import numpy as np


# ---- Normalize helper ----
def normalize_param_to_size(param, name: str, n: int) -> np.ndarray:
    arr = np.asarray(param, dtype=float)
    if arr.ndim == 0:  # scalar
        return np.full(n, float(arr))
    elif arr.ndim == 1:
        if arr.shape[0] != n:
            raise ValueError(f"{name} must have length {n}, got {arr.shape[0]}")
        return arr
    else:
        raise ValueError(f"{name} must be scalar or 1D sequence, got shape {arr.shape}")
    
# ---- Waypoint validation helper ----
def validate_waypoint_param(param) -> np.ndarray:
    waypoints = np.asarray(param, dtype=float)

    if waypoints.ndim == 1:
        if waypoints.shape[0] != 3:
            raise ValueError(f"Single waypoint must have exactly 3 values, got {waypoints.shape[0]}")
        waypoints = waypoints[np.newaxis, :]  # shape -> (1, 3)
    elif waypoints.ndim == 2:
        if waypoints.shape[1] != 3:
            raise ValueError(f"Each waypoint must have exactly 3 values, got shape {waypoints.shape[1]}")
    else:
        raise ValueError(f"Waypoints must be a sequence with shape (3,) or (N,3), got shape {waypoints.shape}")
    
    return waypoints