from abc import ABC, abstractmethod
import numpy as np

class ObjectiveFunction(ABC):
    @abstractmethod
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        pass

class CallableObjective(ObjectiveFunction):
    def __init__(self, func):
        self.func = func
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        return self.func(x)
