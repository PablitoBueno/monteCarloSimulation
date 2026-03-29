import math
from . import statistics as _stats

class ConvergenceCriterion:
    def __init__(self, tol_rel: float = 0.01, tol_abs: float = 1e-6, max_iter: int = 10**6, min_iter: int = 100, window: int = 10, patience: int = 3):
        self.tol_rel = float(tol_rel)
        self.tol_abs = float(tol_abs)
        self.max_iter = int(max_iter)
        self.min_iter = int(min_iter)
        self.window = int(window)
        self.patience = int(patience)
        self.consecutive_hits = 0

    def should_stop(self, aggregator: _stats.StatisticsAggregator) -> bool:
        N = aggregator.N
        if N < self.min_iter:
            return False
        if N >= self.max_iter:
            return True
        mean, _, stderr, rel_err = aggregator.get_stats()
        if math.isnan(stderr) or math.isnan(mean):
            return False
        stop_condition = (rel_err < self.tol_rel) or (stderr < self.tol_abs)
        if stop_condition:
            self.consecutive_hits += 1
        else:
            self.consecutive_hits = 0
        return self.consecutive_hits >= self.patience
