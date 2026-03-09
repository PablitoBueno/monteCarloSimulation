import numpy as np
from .base import CallableObjective

def build_builtin(name: str):
    name = name.lower()
    if name == "sum_squares":
        def f(x): return np.sum(np.asarray(x, dtype=float)**2, axis=1)
        return CallableObjective(f)
    if name == "sum":
        def f(x): return np.sum(np.asarray(x, dtype=float), axis=1)
        return CallableObjective(f)
    if name == "exp_sum":
        def f(x): return np.exp(np.sum(np.asarray(x, dtype=float), axis=1))
        return CallableObjective(f)
    if name == "identity_first":
        def f(x): arr = np.asarray(x, dtype=float); return arr[:,0]
        return CallableObjective(f)
    raise ValueError("unsupported builtin objective name: " + str(name))
