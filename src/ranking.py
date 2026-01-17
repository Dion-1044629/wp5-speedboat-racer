from dataclasses import dataclass
from src.track import Track, RacerProgress, progress_value

@dataclass
class RacerSnapshot:
    racer_id: str
    x: float
    y: float
    prog: RacerProgress

def rank_racers(track: Track, racers: list[RacerSnapshot]) -> list[RacerSnapshot]:
    """
    Returns racers sorted from 1st to last based on progress_value (descending).
    """
    return sorted(
        racers,
        key=lambda r: progress_value(track, r.prog, r.x, r.y),
        reverse=True,
    )

def position_of(track: Track, racers: list[RacerSnapshot], racer_id: str) -> int:
    ranked = rank_racers(track, racers)
    for i, r in enumerate(ranked, start=1):
        if r.racer_id == racer_id:
            return i
    raise ValueError(f"Unknown racer_id: {racer_id}")
