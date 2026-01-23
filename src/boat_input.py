from dataclasses import dataclass
from src.utils import clamp

@dataclass
class BoatInputState:
    throttle: float = 0.0  # 0..1
    brake: float = 0.0     # 0..1
    steer: float = 0.0     # -1..1  (left=-1, right=+1)

def update_input(
    state: BoatInputState,
    *,
    gas: bool,
    brake: bool,
    left: bool,
    right: bool,
    dt: float,
    throttle_rate: float = 2.5,
    brake_rate: float = 3.5,
    steer_rate: float = 4.0,
    return_rate: float = 6.0,
) -> BoatInputState:
    """
    Update input state with simple 'press ramps up, release returns to 0' behavior.
    dt is in seconds.
    """
    # Throttle
    if gas:
        state.throttle = clamp(state.throttle + throttle_rate * dt, 0.0, 1.0)
    else:
        state.throttle = clamp(state.throttle - return_rate * dt, 0.0, 1.0)

    # Brake
    if brake:
        state.brake = clamp(state.brake + brake_rate * dt, 0.0, 1.0)
    else:
        state.brake = clamp(state.brake - return_rate * dt, 0.0, 1.0)

    # Steer (-1..1)
    steer_target = 0.0
    if left and not right:
        steer_target = -1.0
    elif right and not left:
        steer_target = 1.0

    if steer_target == 0.0:
        # Return to center
        if state.steer > 0:
            state.steer = max(0.0, state.steer - return_rate * dt)
        elif state.steer < 0:
            state.steer = min(0.0, state.steer + return_rate * dt)
    else:
        # Move toward target
        direction = 1.0 if steer_target > state.steer else -1.0
        state.steer = clamp(state.steer + direction * steer_rate * dt, -1.0, 1.0)

    return state
