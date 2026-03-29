from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import traceback

from ..config.loader import load_config
from ..core.statistics import StatisticsAggregator

app = FastAPI(title="Monte Carlo Engine API")

# CORS – permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConfigRequest(BaseModel):
    config: Dict[str, Any]


def print_results_dict(agg: StatisticsAggregator) -> Dict[str, Any]:
    mean, var_sample, stderr, rel_err = agg.get_stats()
    li, ls = agg.confidence_interval(0.95)
    return {
        "samples_processed": agg.N,
        "mean_estimate": mean,
        "variance_sample": var_sample,
        "standard_error": stderr,
        "relative_error_percent": rel_err,
        "95ci_lower": li,
        "95ci_upper": ls
    }


@app.post("/run")
def run_simulation(request: ConfigRequest):
    try:
        cfg = load_config_from_dict(request.config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to load configuration: {str(e)}")

    engine = cfg["engine"]
    batch_size = cfg["batch_size"]
    run_mode = cfg["run_mode"]
    n_batches = cfg["n_batches"]
    criterion = cfg["criterion"]

    try:
        if run_mode == "adaptive":
            aggregator = engine.run(batch_size=batch_size, criterion=criterion)
        elif run_mode == "fixed":
            if n_batches <= 0:
                raise ValueError("n_batches must be positive for fixed run_mode")
            aggregator = engine.run_fixed_batches(n_batches=n_batches, batch_size=batch_size)
        else:
            raise ValueError("unknown run_mode, use 'adaptive' or 'fixed'")

        result = print_results_dict(aggregator)
        history = aggregator.get_history()   # <-- NOVO
        return {"status": "success", "results": result, "history": history}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"simulation failed: {str(e)}")

    finally:
        try:
            engine.close()
        except Exception:
            pass


def load_config_from_dict(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    from ..config.loader import build_distribution, build_objective, build_convergence_criterion
    from ..core.engine import MonteCarloEngine

    if not isinstance(config_dict, dict):
        raise ValueError("config must be a JSON object")

    distribution_conf = config_dict.get("distribution")
    if distribution_conf is None:
        raise ValueError("config must contain 'distribution' section")
    distribution = build_distribution(distribution_conf)

    objective_conf = config_dict.get("objective")
    if objective_conf is None:
        raise ValueError("config must contain 'objective' section")
    objective = build_objective(objective_conf)

    technique = config_dict.get("technique", "standard").lower()

    proposal = None
    if technique == "importance":
        proposal_conf = config_dict.get("proposal_distribution")
        if proposal_conf is None:
            raise ValueError("importance sampling requires 'proposal_distribution'")
        proposal = build_distribution(proposal_conf)

    use_parallel = bool(config_dict.get("use_parallel", False))
    n_workers = config_dict.get("n_workers")
    seed = config_dict.get("seed")
    batch_size = int(config_dict.get("batch_size", 1000))
    run_mode = config_dict.get("run_mode", "adaptive").lower()
    n_batches = int(config_dict.get("n_batches", 0))

    criterion_conf = config_dict.get("convergence_criterion")
    criterion = build_convergence_criterion(criterion_conf)

    engine = MonteCarloEngine(
        distribution=distribution,
        objective=objective,
        technique=technique,
        proposal_dist=proposal,
        use_parallel=use_parallel,
        n_workers=n_workers,
        seed=seed
    )

    return {
        "engine": engine,
        "batch_size": batch_size,
        "run_mode": run_mode,
        "n_batches": n_batches,
        "criterion": criterion
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)