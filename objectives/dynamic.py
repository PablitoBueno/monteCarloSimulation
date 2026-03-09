import numpy as np, math
from typing import Callable
from .base import CallableObjective
from .builtin import build_builtin
from scipy.stats import norm

def safe_eval_lambda(lambda_str: str) -> Callable:
    try:
        obj = eval(lambda_str, {"np": np, "math": math, "norm": norm})
        if not callable(obj):
            raise ValueError("evaluated object is not callable")
        return obj
    except Exception as e:
        raise ValueError("failed to eval lambda/function string: " + str(e))

def build_objective(conf: dict):
    if not isinstance(conf, dict):
        raise ValueError("objective configuration must be an object")
    otype = conf.get("type", "").lower()
    if otype == "builtin":
        name = conf.get("name", "").lower()
        return build_builtin(name)
    if otype == "lambda":
        lambda_str = conf.get("lambda")
        if not isinstance(lambda_str, str):
            raise ValueError("lambda objective requires a string under 'lambda'")
        func = safe_eval_lambda(lambda_str)
        def wrapper(x):
            res = func(np.asarray(x, dtype=float))
            arr = np.asarray(res, dtype=float).ravel()
            return arr
        return CallableObjective(wrapper)
    if otype == "code":
        code = conf.get("code")
        if not isinstance(code, str):
            raise ValueError("code objective requires 'code' string defining function 'objective_func(x)'")
        local_ns = {}
        try:
            exec(code, {"np": np, "math": math, "norm": norm}, local_ns)
            user_func = local_ns.get("objective_func")
            if user_func is None:
                raise ValueError("code must define objective_func(x)")
            def wrapper(x):
                res = user_func(np.asarray(x, dtype=float))
                return np.asarray(res, dtype=float).ravel()
            return CallableObjective(wrapper)
        except Exception as e:
            raise ValueError("failed to compile objective code: " + str(e))
    raise ValueError("unsupported objective type: " + str(otype))
