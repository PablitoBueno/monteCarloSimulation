import math
import numpy as np
from scipy.stats import norm
from typing import Tuple, List, Any, Dict

class StatisticsAggregator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.N = 0
        self.sum_f = 0.0
        self.sum_f2 = 0.0
        # Históricos
        self.history_mean = []
        self.history_std_err = []
        self.history_rel_err = []
        self.history_ci_lower = []
        self.history_ci_upper = []
        self.history_samples = []          # todas as amostras (para histograma)
        self.current_batch = []            # última amostra (opcional)

    def update(self, f_values: np.ndarray):
        arr = np.asarray(f_values, dtype=float)
        if arr.ndim != 1:
            arr = arr.ravel()
        n = len(arr)
        if n == 0:
            return
        self.current_batch = arr.tolist()
        self.sum_f += float(np.sum(arr))
        self.sum_f2 += float(np.sum(arr**2))
        self.N += n

        mean, var_sample, stderr, rel_err = self.get_stats()
        ci_lower, ci_upper = self.confidence_interval(0.95)

        self.history_mean.append(mean)
        self.history_std_err.append(stderr)
        self.history_rel_err.append(rel_err)
        self.history_ci_lower.append(ci_lower)
        self.history_ci_upper.append(ci_upper)
        self.history_samples.extend(arr.tolist())

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

    def get_history(self) -> Dict[str, Any]:
        """Retorna todos os dados históricos para os gráficos."""
        return {
            'iterations': list(range(1, len(self.history_mean) + 1)),
            'mean_history': self.history_mean,
            'std_error_history': self.history_std_err,
            'rel_error_history': self.history_rel_err,
            'lower_ci': self.history_ci_lower,
            'upper_ci': self.history_ci_upper,
            'all_samples': self.history_samples,
            'current_batch': self.current_batch
        }