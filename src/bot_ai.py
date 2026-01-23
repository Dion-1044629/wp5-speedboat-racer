import math
from dataclasses import dataclass
from src.track import Track, RacerProgress
from src.utils import clamp

def wrap_angle(a: float) -> float:
    # normalize to [-pi, pi]
    while a > math.pi:
        a -= 2 * math.pi
    while a < -math.pi:
        a += 2 * math.pi
    return a

@dataclass
class BotDecision:
    throttle: float  # 0..1
    brake: float     # 0..1
    steer: float     # -1..1

def bot_decide(track: Track, prog: RacerProgress, x: float, y: float, angle: float, speed: float) -> BotDecision:
    """
    Very simple waypoint-following:
    - Aim at next checkpoint center
    - Steer toward it
    - Throttle most of the time, brake a bit if turning sharply
    """
    if prog.finished:
        return BotDecision(throttle=0.0, brake=1.0, steer=0.0)

    idx = min(prog.next_cp_index, len(track.checkpoints) - 1)
    cp = track.checkpoints[idx]

    desired = math.atan2(cp.y - y, cp.x - x)
    diff = wrap_angle(desired - angle)

    steer = clamp(diff / 0.9, -1.0, 1.0)  # scale to full steer around ~0.9 rad
    turn_hard = abs(diff) > 0.7

    throttle = 1.0 if not turn_hard else 0.6
    brake = 0.0 if not turn_hard else 0.2

    # if very close, ease off a bit to prevent orbiting
    dist = math.hypot(cp.x - x, cp.y - y)
    if dist < cp.radius * 0.8:
        throttle = 0.4
        brake = 0.0

    return BotDecision(throttle=throttle, brake=brake, steer=steer)
