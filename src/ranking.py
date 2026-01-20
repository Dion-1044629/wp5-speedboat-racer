from dataclasses import dataclass
from src.track import Track, RacerProgress, progress_value

@dataclass
class RacerSnapshot:
    racer_id: str
    x: float
    y: float
    prog: RacerProgress
    finish_time: float | None = None


def rank_racers(track: Track, racers: list[RacerSnapshot]) -> list[RacerSnapshot]:
    """
    Sorted from 1st to last.
    Primary: progress_value (descending)
    Tie-breaker (when finished): earlier finish_time wins.
    """
    def key(r: RacerSnapshot):
        pv = progress_value(track, r.prog, r.x, r.y)
        finished_flag = 1 if r.prog.finished else 0
        ft = r.finish_time if r.finish_time is not None else 1e9  # large = "not finished"
        # With reverse=True: bigger finished_flag, bigger pv, bigger (-ft) => earlier finish wins
        return (finished_flag, pv, -ft)

    return sorted(racers, key=key, reverse=True)

def position_of(track: Track, racers: list[RacerSnapshot], racer_id: str) -> int:
    ranked = rank_racers(track, racers)
    for i, r in enumerate(ranked, start=1):
        if r.racer_id == racer_id:
            return i
    raise ValueError(f"Unknown racer_id: {racer_id}")
