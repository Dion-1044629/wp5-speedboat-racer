from dataclasses import dataclass
import math

def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))

@dataclass
class Boat:
    x: float
    y: float
    angle: float = 0.0          # radians
    speed: float = 0.0          # pixels/sec

    max_speed: float = 420.0
    accel: float = 520.0        # px/s^2
    brake_decel: float = 900.0  # px/s^2
    drag: float = 240.0         # px/s^2
    turn_rate: float = 2.8      # rad/sec at full steer

    def update(self, throttle: float, brake: float, steer: float, dt: float) -> None:
        # Acceleration / braking / drag
        if throttle > 0.0:
            self.speed += self.accel * throttle * dt
        if brake > 0.0:
            self.speed -= self.brake_decel * brake * dt

        # Passive drag toward 0
        if self.speed > 0:
            self.speed = max(0.0, self.speed - self.drag * dt)
        elif self.speed < 0:
            self.speed = min(0.0, self.speed + self.drag * dt)

        self.speed = clamp(self.speed, 0.0, self.max_speed)

        # Turning depends a bit on speed (no turning when standing still feels better)
        speed_factor = clamp(self.speed / self.max_speed, 0.0, 1.0)
        self.angle += steer * self.turn_rate * speed_factor * dt

        # Move forward in the boat's facing direction
        vx = math.cos(self.angle) * self.speed
        vy = math.sin(self.angle) * self.speed
        self.x += vx * dt
        self.y += vy * dt
