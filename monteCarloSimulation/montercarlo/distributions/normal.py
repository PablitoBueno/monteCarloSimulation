import numpy as np
from scipy.stats import norm
from .base import Distribution

class NormalDistribution(Distribution):
    def __init__(self, mean, std):
        self.mean = np.asarray(mean, dtype=float)
        self.std = np.asarray(std, dtype=float)
        if np.any(self.std <= 0):
            raise ValueError("normal distribution requires positive std for all dimensions")
        if self.mean.ndim == 0:
            self.dim = 1
        else:
            self.dim = len(self.mean)
    def sample(self, n: int) -> np.ndarray:
        return np.random.normal(self.mean, self.std, size=(n, self.dim))
    def pdf(self, x: np.ndarray) -> np.ndarray:
        arr = np.asarray(x, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] != self.dim:
            raise ValueError("input dimensionality does not match distribution dimensionality")
        z = (arr - self.mean) / self.std
        marg = norm.pdf(z) / self.std
        dens = np.prod(marg, axis=1)
        return dens
    def ppf(self, u: np.ndarray) -> np.ndarray:
        arr = np.asarray(u, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] != self.dim:
            raise ValueError("input dimensionality does not match distribution dimensionality")
        return self.mean + self.std * norm.ppf(arr)
