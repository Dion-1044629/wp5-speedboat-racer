from src.boat_input import BoatInputState, update_input

def test_throttle_increases_when_gas_pressed():
    s = BoatInputState()
    s = update_input(s, gas=True, brake=False, left=False, right=False, dt=0.5)
    assert s.throttle > 0.0

def test_throttle_returns_to_zero_when_released():
    s = BoatInputState(throttle=1.0)
    s = update_input(s, gas=False, brake=False, left=False, right=False, dt=1.0)
    assert s.throttle < 1.0
