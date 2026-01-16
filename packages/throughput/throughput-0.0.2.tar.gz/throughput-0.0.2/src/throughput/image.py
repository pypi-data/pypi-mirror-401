import time
from contextlib import contextmanager
from collections import defaultdict

class WallClock:
    def __init__(self):
        self.timings = defaultdict(list)
    
    @contextmanager
    def __call__(self, name):
        t0 = time.perf_counter()
        yield
        elapsed = time.perf_counter() - t0
        self.timings[name].append(elapsed)
    
    def mean(self, name):
        times = self.timings[name]
        return sum(times) / len(times) if times else 0.0
    
    def median(self, name):
        times = sorted(self.timings[name])
        n = len(times)
        if n == 0:
            return 0.0
        if n % 2 == 1:
            return times[n // 2]
        return (times[n // 2 - 1] + times[n // 2]) / 2
    
    def total(self, name):
        return sum(self.timings[name])
    
    def count(self, name):
        return len(self.timings[name])
    
    def reset(self, name=None):
        if name is None:
            self.timings.clear()
        else:
            self.timings[name].clear()
    
    def throughput(self, name, pixels=1920*1080):
        """Returns megapixels per second based on median time"""
        med_time = self.median(name)
        return pixels * 1e-6 / med_time if med_time > 0 else float('inf')
    
    def summary(self, pixels=1920*1080):
        for name in self.timings:
            print(f"{name}: median={self.median(name)*1000:.2f}ms, "
                  f"mean={self.mean(name)*1000:.2f}ms, "
                  f"throughput={self.throughput(name, pixels):.2f} MP/s")

wallclock = WallClock()