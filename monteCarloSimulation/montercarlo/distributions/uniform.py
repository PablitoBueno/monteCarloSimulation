import numpy as np
from .base import Distribution

class UniformDistribution(Distribution):
    def __init__(self, low, high):
        self.low = np.asarray(low, dtype=float)
        self.high = np.asarray(high, dtype=float)
        if np.any(self.high <= self.low):
            raise ValueError("uniform distribution requires high > low for all dimensions")
        if self.low.ndim == 0:
            self.dim = 1
        else:
            self.dim = len(self.low)
        self._volume = float(np.prod(self.high - self.low))
    def sample(self, n: int) -> np.ndarray:
        u = np.random.uniform(0.0, 1.0, size=(n, self.dim))
        return self.low + u * (self.high - self.low)
    def pdf(self, x: np.ndarray) -> np.ndarray:
        arr = np.asarray(x, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] != self.dim:
            raise ValueError("input dimensionality does not match distribution dimensionality")
        inside = np.all((arr >= self.low) & (arr <= self.high), axis=1)
        dens = np.where(inside, 1.0 / self._volume, 0.0)
        return dens
    def ppf(self, u: np.ndarray) -> np.ndarray:
        arr = np.asarray(u, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] != self.dim:
            raise ValueError("input dimensionality does not match distribution dimensionality")
        return self.low + arr * (self.high - self.low)
