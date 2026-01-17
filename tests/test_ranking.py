from src.track import Checkpoint, Track, RacerProgress, update_progress
from src.ranking import RacerSnapshot, rank_racers, position_of

def test_ranking_orders_by_progress_value():
    track = Track([Checkpoint(0, 0, 10), Checkpoint(100, 0, 10)])

    p1 = RacerProgress()
    p2 = RacerProgress()

    # both pass first checkpoint
    update_progress(track, p1, 0, 0)
    update_progress(track, p2, 0, 0)

    # racer B is closer to finish
    rA = RacerSnapshot("A", x=20, y=0, prog=p1)
    rB = RacerSnapshot("B", x=80, y=0, prog=p2)

    ranked = rank_racers(track, [rA, rB])
    assert ranked[0].racer_id == "B"
    assert ranked[1].racer_id == "A"

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
