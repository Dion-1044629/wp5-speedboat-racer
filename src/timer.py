from dataclasses import dataclass

@dataclass
class CountdownTimer:
    total_seconds: float
    remaining: float | None = None

    def __post_init__(self) -> None:
        if self.remaining is None:
            self.remaining = float(self.total_seconds)

    def update(self, dt: float) -> None:
        self.remaining = max(0.0, self.remaining - dt)

    @property
    def is_done(self) -> bool:
        return self.remaining <= 0.0

    def as_text(self) -> str:
        seconds = int(self.remaining)
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"
