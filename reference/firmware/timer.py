"""Countdown behavior, independent of GPIO and wall-clock time."""
class Timer:
    def __init__(self, duration_ms=25*60*1000):
        self.duration_ms = duration_ms
        self.remaining_ms = duration_ms
        self.mode = "idle"

    def tap(self):
        if self.mode in ("idle", "done"):
            self.remaining_ms = self.duration_ms
            self.mode = "running"
        elif self.mode == "running":
            self.mode = "paused"
        else:
            self.mode = "running"

    def reset(self):
        self.remaining_ms = self.duration_ms
        self.mode = "idle"

    def advance(self, elapsed_ms):
        if elapsed_ms < 0:
            raise ValueError("elapsed time must not be negative")
        if self.mode == "running":
            self.remaining_ms = max(0, self.remaining_ms - elapsed_ms)
            if self.remaining_ms == 0:
                self.mode = "done"

    def lights(self):
        # Red, amber, green; at most one illuminated branch.
        return {"idle": (0,0,1), "running": (1,0,0),
                "paused": (0,1,0), "done": (0,0,1)}[self.mode]
