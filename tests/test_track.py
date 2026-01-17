from src.track import Checkpoint, Track, RacerProgress, update_progress, progress_value

def test_reaching_checkpoint_advances_index():
    track = Track([Checkpoint(0, 0, 10), Checkpoint(100, 0, 10)])
    prog = RacerProgress()

    # At start checkpoint
    update_progress(track, prog, x=0, y=0)
    assert prog.next_cp_index == 1
    assert prog.finished is False

def test_finishing_marks_finished():
    track = Track([Checkpoint(0, 0, 10), Checkpoint(100, 0, 10)])
    prog = RacerProgress()

    update_progress(track, prog, x=0, y=0)        # pass cp0
    update_progress(track, prog, x=100, y=0)      # pass cp1 (finish)
    assert prog.finished is True

def test_progress_value_increases_when_closer_to_next_checkpoint():
    track = Track([Checkpoint(0, 0, 10), Checkpoint(100, 0, 10)])
    prog = RacerProgress()

    # Pass first checkpoint so "next" becomes cp1
    update_progress(track, prog, x=0, y=0)
    v_far = progress_value(track, prog, x=10, y=0)   # far from cp1
    v_near = progress_value(track, prog, x=90, y=0)  # closer to cp1
    assert v_near > v_far
