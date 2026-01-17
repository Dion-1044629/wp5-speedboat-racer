from dataclasses import dataclass
import math

def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))

@dataclass(frozen=True)
class Checkpoint:
    x: float
    y: float
    radius: float = 60.0  # pixels

@dataclass(frozen=True)
class Track:
    checkpoints: list[Checkpoint]

    def __post_init__(self) -> None:
        if len(self.checkpoints) < 2:
            raise ValueError("Track needs at least 2 checkpoints (start + finish).")

@dataclass
class RacerProgress:
    next_cp_index: int = 0
    finished: bool = False

def distance(ax: float, ay: float, bx: float, by: float) -> float:
    return math.hypot(ax - bx, ay - by)

def update_progress(track: Track, prog: RacerProgress, x: float, y: float) -> RacerProgress:
    """
    Check if racer reached the next checkpoint (in order). If so, advance.
    When the last checkpoint is reached, mark finished.
    """
    if prog.finished:
        return prog

    cp = track.checkpoints[prog.next_cp_index]
    if distance(x, y, cp.x, cp.y) <= cp.radius:
        prog.next_cp_index += 1
        if prog.next_cp_index >= len(track.checkpoints):
            prog.finished = True
            prog.next_cp_index = len(track.checkpoints)  # clamp for safety
    return prog

def progress_value(track: Track, prog: RacerProgress, x: float, y: float) -> float:
    """
    Returns a sortable number for ranking:
    - Higher means further in race.
    - Base is how many checkpoints have been passed.
    - Adds a fractional part based on how close you are to the next checkpoint.
    """
    if prog.finished:
        # Put finished racers clearly ahead of non-finished; still sortable if multiple finish.
        return float(len(track.checkpoints)) + 1.0

    idx = prog.next_cp_index
    base = float(idx)

    # Fraction toward next checkpoint
    next_cp = track.checkpoints[idx]
    dist_to_next = distance(x, y, next_cp.x, next_cp.y)

    if idx == 0:
        # No "previous" checkpoint; just use a simple closeness score
        frac = clamp(1.0 - dist_to_next / 800.0, 0.0, 0.999)
        return base + frac

    prev_cp = track.checkpoints[idx - 1]
    seg_len = max(1.0, distance(prev_cp.x, prev_cp.y, next_cp.x, next_cp.y))
    frac = clamp(1.0 - dist_to_next / seg_len, 0.0, 0.999)

    return base + frac
