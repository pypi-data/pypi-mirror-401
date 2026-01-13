import time

class PerfLogger:
    def __init__(self):
        # Use perf_counter for performance measurements - higher precision and not affected by system clock adjustments
        self.last_time = time.perf_counter_ns()
    
    def log(self, msg=""):
        # Use perf_counter for performance measurements - higher precision and not affected by system clock adjustments
        current = time.perf_counter_ns()
        delta = current - self.last_time
        print(f"{msg} Δt: {delta:.6f}s")
        self.last_time = current