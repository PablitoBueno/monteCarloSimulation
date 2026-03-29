import numpy as np
from typing import Callable, Optional
from .base import Distribution

class CustomDistribution(Distribution):
    def __init__(self, sample_func: Callable[[int], np.ndarray], pdf_func: Optional[Callable[[np.ndarray], np.ndarray]] = None, ppf_func: Optional[Callable[[np.ndarray], np.ndarray]] = None):
        self.sample_func = sample_func
        self.pdf_func = pdf_func
        self.ppf_func = ppf_func
        test = sample_func(1)
        test = np.asarray(test, dtype=float)
        if test.ndim != 2:
            raise ValueError("custom sample function must return array of shape (n, d)")
        self.dim = test.shape[1]
    def sample(self, n: int) -> np.ndarray:
        return self.sample_func(n)
    def pdf(self, x: np.ndarray) -> np.ndarray:
        if self.pdf_func is None:
            raise NotImplementedError("pdf_func not provided for custom distribution")
        return self.pdf_func(x)
    def ppf(self, u: np.ndarray) -> np.ndarray:
        if self.ppf_func is None:
            raise NotImplementedError("ppf_func not provided for custom distribution")
        return self.ppf_func(u)
