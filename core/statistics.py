from typing import Tuple
import math
import numpy as np
from scipy.stats import norm

class StatisticsAggregator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.N = 0
        self.sum_f = 0.0
        self.sum_f2 = 0.0
        self.history_mean = []
        self.history_std_err = []
        self.history_rel_err = []

    def update(self, f_values: np.ndarray):
        arr = np.asarray(f_values, dtype=float)
        if arr.ndim != 1:
            arr = arr.ravel()
        n = len(arr)
        if n == 0:
            return
        self.sum_f += float(np.sum(arr))
        self.sum_f2 += float(np.sum(arr**2))
        self.N += n
        mean, var_sample, stderr, rel_err = self.get_stats()
        self.history_mean.append(mean)
        self.history_std_err.append(stderr)
        self.history_rel_err.append(rel_err)

    def get_stats(self) -> Tuple[float, float, float, float]:
        if self.N == 0:
            return float('nan'), float('nan'), float('nan'), float('nan')
        mean = self.sum_f / self.N
        if self.N == 1:
            var_sample = float('nan')
            stderr = float('nan')
        else:
            var_sample = (self.sum_f2 / self.N - mean**2) * self.N / (self.N - 1)
            stderr = math.sqrt(var_sample / self.N) if var_sample >= 0 else float('nan')
        rel_err = (stderr / abs(mean) * 100.0) if (not math.isnan(stderr) and mean != 0) else float('inf')
        return mean, var_sample, stderr, rel_err

    def confidence_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        if self.N < 2:
            return float('nan'), float('nan')
        mean, var_sample, _, _ = self.get_stats()
        z = norm.ppf(1 - (1 - confidence) / 2)
        err = z * math.sqrt(var_sample / self.N)
        return mean - err, mean + err
