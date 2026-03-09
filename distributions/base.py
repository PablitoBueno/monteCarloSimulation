from abc import ABC, abstractmethod
import numpy as np

class Distribution(ABC):
    @abstractmethod
    def sample(self, n: int) -> np.ndarray:
        pass
    def pdf(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError("pdf not implemented")
    def ppf(self, u: np.ndarray) -> np.ndarray:
        raise NotImplementedError("ppf not implemented")
