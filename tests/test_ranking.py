from src.track import Checkpoint, Track, RacerProgress, update_progress
from src.ranking import RacerSnapshot, rank_racers, position_of

def test_finished_tie_breaker_earlier_finish_time_wins():
    track = Track([Checkpoint(0, 0, 10), Checkpoint(100, 0, 10)])

    pA = RacerProgress(finished=True, next_cp_index=len(track.checkpoints))
    pB = RacerProgress(finished=True, next_cp_index=len(track.checkpoints))

    rA = RacerSnapshot("A", x=0, y=0, prog=pA, finish_time=10.0)
    rB = RacerSnapshot("B", x=0, y=0, prog=pB, finish_time=20.0)

    ranked = rank_racers(track, [rB, rA])
    assert ranked[0].racer_id == "A"

def test_position_of_returns_1_for_leader():
    track = Track([Checkpoint(0, 0, 10), Checkpoint(100, 0, 10)])

    p1 = RacerProgress()
    p2 = RacerProgress()
    update_progress(track, p1, 0, 0)
    update_progress(track, p2, 0, 0)

    rA = RacerSnapshot("A", x=90, y=0, prog=p1)
    rB = RacerSnapshot("B", x=10, y=0, prog=p2)

    assert position_of(track, [rA, rB], "A") == 1
    assert position_of(track, [rA, rB], "B") == 2
