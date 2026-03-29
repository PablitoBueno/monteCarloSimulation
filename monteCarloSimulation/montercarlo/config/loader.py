import json
from ..distributions.uniform import UniformDistribution
from ..distributions.normal import NormalDistribution
from ..distributions.custom import CustomDistribution
from ..objectives.dynamic import build_objective
from ..core.engine import MonteCarloEngine
from ..core.convergence import ConvergenceCriterion

def build_distribution(conf: dict):
    if not isinstance(conf, dict):
        raise ValueError("distribution configuration must be an object")
    dtype = conf.get("type", "").lower()
    if dtype == "uniform":
        low = conf.get("low", 0.0)
        high = conf.get("high", 1.0)
        return UniformDistribution(low=low, high=high)
    if dtype == "normal":
        mean = conf.get("mean", 0.0)
        std = conf.get("std", 1.0)
        return NormalDistribution(mean=mean, std=std)
    if dtype == "custom":
        sample_code = conf.get("sample_code")
        pdf_code = conf.get("pdf_code")
        ppf_code = conf.get("ppf_code")
        if sample_code is None:
            raise ValueError("custom distribution requires 'sample_code'")
        local_ns = {}
        try:
            exec(sample_code, {"np": __import__('numpy'), "math": __import__('math'), "norm": __import__('scipy').stats.norm}, local_ns)
            sample_func = local_ns.get("sample_func")
            if sample_func is None:
                raise ValueError("sample_code must define sample_func(n)")
        except Exception as e:
            raise ValueError("failed to compile sample_code: " + str(e))
        pdf_func = None
        ppf_func = None
        if pdf_code is not None:
            try:
                exec(pdf_code, {"np": __import__('numpy'), "math": __import__('math'), "norm": __import__('scipy').stats.norm}, local_ns)
                pdf_func = local_ns.get("pdf_func")
                if pdf_func is None:
                    raise ValueError("pdf_code must define pdf_func(x)")
            except Exception as e:
                raise ValueError("failed to compile pdf_code: " + str(e))
        if ppf_code is not None:
            try:
                exec(ppf_code, {"np": __import__('numpy'), "math": __import__('math'), "norm": __import__('scipy').stats.norm}, local_ns)
                ppf_func = local_ns.get("ppf_func")
                if ppf_func is None:
                    raise ValueError("ppf_code must define ppf_func(u)")
            except Exception as e:
                raise ValueError("failed to compile ppf_code: " + str(e))
        return CustomDistribution(sample_func=sample_func, pdf_func=pdf_func, ppf_func=ppf_func)
    raise ValueError("unsupported distribution type: " + str(dtype))

def build_convergence_criterion(conf: dict):
    if conf is None:
        return ConvergenceCriterion()
    return ConvergenceCriterion(
        tol_rel=conf.get("tol_rel", 0.01),
        tol_abs=conf.get("tol_abs", 1e-6),
        max_iter=conf.get("max_iter", 10**6),
        min_iter=conf.get("min_iter", 100),
        window=conf.get("window", 10),
        patience=conf.get("patience", 3)
    )

def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if not isinstance(cfg, dict):
        raise ValueError("config file must contain a JSON object at root")
    distribution_conf = cfg.get("distribution")
    if distribution_conf is None:
        raise ValueError("config must contain 'distribution' section")
    distribution = build_distribution(distribution_conf)
    objective_conf = cfg.get("objective")
    if objective_conf is None:
        raise ValueError("config must contain 'objective' section")
    objective = build_objective(objective_conf)
    technique = cfg.get("technique", "standard").lower()
    proposal = None
    if technique == "importance":
        proposal_conf = cfg.get("proposal_distribution")
        if proposal_conf is None:
            raise ValueError("importance sampling requires 'proposal_distribution' section")
        proposal = build_distribution(proposal_conf)
    use_parallel = bool(cfg.get("use_parallel", False))
    n_workers = cfg.get("n_workers")
    seed = cfg.get("seed")
    batch_size = int(cfg.get("batch_size", 1000))
    run_mode = cfg.get("run_mode", "adaptive").lower()
    n_batches = int(cfg.get("n_batches", 0))
    criterion_conf = cfg.get("convergence_criterion")
    criterion = build_convergence_criterion(criterion_conf)
    engine = MonteCarloEngine(distribution=distribution, objective=objective, technique=technique, proposal_dist=proposal, use_parallel=use_parallel, n_workers=n_workers, seed=seed)
    return {
        "engine": engine,
        "batch_size": batch_size,
        "run_mode": run_mode,
        "n_batches": n_batches,
        "criterion": criterion
    }
