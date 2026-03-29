from typing import Callable, Optional
import numpy as np
import math
import multiprocessing as mp
from scipy.stats import qmc
from ..distributions.base import Distribution
from ..objectives.base import ObjectiveFunction
from .statistics import StatisticsAggregator
from .convergence import ConvergenceCriterion

class MonteCarloEngine:
    def __init__(self, distribution: Distribution, objective: ObjectiveFunction, technique: str = 'standard', proposal_dist: Optional[Distribution] = None, use_parallel: bool = False, n_workers: Optional[int] = None, seed: Optional[int] = None):
        self.distribution = distribution
        self.objective = objective
        self.technique = technique.lower()
        self.proposal = proposal_dist
        self.use_parallel = bool(use_parallel)
        self.seed = seed
        if seed is not None:
            np.random.seed(int(seed))
        if self.technique == 'importance' and self.proposal is None:
            raise ValueError("importance sampling requires a proposal distribution")
        if self.technique == 'qmc':
            if not hasattr(self.distribution, 'ppf'):
                raise RuntimeError("distribution must implement ppf for qmc")
            self.sobol = qmc.Sobol(d=self.distribution.dim, scramble=True, seed=seed)
            self._qmc_used = 0
        else:
            self.sobol = None
        self.pool = None
        self.n_workers = n_workers
        if self.use_parallel:
            procs = n_workers if n_workers is not None else mp.cpu_count()
            if procs < 1:
                procs = 1
            try:
                self.pool = mp.Pool(processes=procs)
            except Exception:
                self.pool = None
                self.use_parallel = False

    def close(self):
        if self.pool is not None:
            try:
                self.pool.close()
                self.pool.join()
            except Exception:
                pass
            self.pool = None

    def _generate_samples(self, n: int):
        if n <= 0:
            return np.zeros((0, self.distribution.dim))
        if self.technique == 'standard':
            return self.distribution.sample(n)
        if self.technique == 'importance':
            return self.proposal.sample(n)
        if self.technique == 'qmc':
            if self.sobol is None:
                raise RuntimeError("sobol not initialized")
            u = self.sobol.random(n)
            self._qmc_used += n
            try:
                samples = self.distribution.ppf(u)
            except Exception as e:
                raise RuntimeError("distribution ppf failed for qmc: " + str(e))
            return samples
        raise ValueError("unknown technique")

    def _evaluate(self, samples):
        if samples.size == 0:
            return np.array([], dtype=float)
        if self.use_parallel and self.pool is not None:
            n = len(samples)
            procs = self.pool._processes if hasattr(self.pool, "_processes") else 1
            chunk_size = max(1, n // procs)
            chunks = [samples[i:i+chunk_size] for i in range(0, n, chunk_size)]
            try:
                results = self.pool.map(self.objective.evaluate, chunks)
                return np.concatenate([np.asarray(r, dtype=float).ravel() for r in results])
            except Exception:
                return self.objective.evaluate(samples)
        else:
            return self.objective.evaluate(samples)

    def _compute_weights(self, samples):
        if self.technique != 'importance':
            return np.ones(len(samples), dtype=float)
        p = self.distribution.pdf(samples)
        q = self.proposal.pdf(samples)
        p = np.asarray(p, dtype=float)
        q = np.asarray(q, dtype=float)
        if p.shape != q.shape:
            raise ValueError("pdf shapes do not match between target and proposal")
        weights = np.zeros_like(p, dtype=float)
        zero_q = (q == 0)
        if np.any(zero_q):
            problematic = (zero_q) & (p > 0)
            if np.any(problematic):
                raise ValueError("proposal pdf is zero where target pdf is positive; importance sampling invalid for some samples")
            weights[~zero_q] = p[~zero_q] / q[~zero_q]
            weights[zero_q] = 0.0
        else:
            weights = p / q
        return weights

    def run(self, batch_size: int = 1000, criterion: Optional[ConvergenceCriterion] = None, callback: Optional[Callable] = None) -> StatisticsAggregator:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        aggregator = StatisticsAggregator()
        if criterion is None:
            criterion = ConvergenceCriterion(max_iter=10**6)
        try:
            while not criterion.should_stop(aggregator):
                samples = self._generate_samples(batch_size)
                values = self._evaluate(samples)
                weights = self._compute_weights(samples)
                weighted_values = values * weights
                aggregator.update(weighted_values)
                if callback is not None:
                    try:
                        callback(aggregator)
                    except Exception:
                        pass
            return aggregator
        finally:
            pass

    def run_fixed_batches(self, n_batches: int, batch_size: int) -> StatisticsAggregator:
        if n_batches < 0 or batch_size <= 0:
            raise ValueError("n_batches must be non-negative and batch_size positive")
        aggregator = StatisticsAggregator()
        for _ in range(n_batches):
            samples = self._generate_samples(batch_size)
            values = self._evaluate(samples)
            weights = self._compute_weights(samples)
            weighted_values = values * weights
            aggregator.update(weighted_values)
        return aggregator
