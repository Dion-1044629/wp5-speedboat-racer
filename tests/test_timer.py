from src.timer import CountdownTimer

def test_timer_counts_down():
    t = CountdownTimer(total_seconds=10)
    t.update(1.5)
    assert 8.4 <= t.remaining <= 8.6  # tolerant for float ops

def test_timer_never_goes_below_zero_and_is_done():
    t = CountdownTimer(total_seconds=1)
    t.update(5.0)
    assert t.remaining == 0.0
    assert t.is_done is True
