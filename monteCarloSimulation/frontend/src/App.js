import React, { useState } from 'react';
import Layout from './components/Layout';
import DistributionForm from './components/DistributionForm';
import ObjectiveForm from './components/ObjectiveForm';
import TechniqueForm from './components/TechniqueForm';
import ConvergenceForm from './components/ConvergenceForm';
import ResultsTabs from './components/ResultsTabs';
import { runSimulation } from './services/api';

function App() {
    // State for all form fields
    const [distribution, setDistribution] = useState({
        type: 'uniform',
        low: 0,
        high: 1
    });
    const [objective, setObjective] = useState({
        type: 'builtin',
        name: 'sum_squares'
    });
    const [technique, setTechnique] = useState({
        type: 'standard'
    });
    const [proposal, setProposal] = useState({
        type: 'uniform',
        low: 0,
        high: 1
    });
    const [runMode, setRunMode] = useState('adaptive');
    const [nBatches, setNBatches] = useState(40);
    const [criterion, setCriterion] = useState({
        batch_size: 1000,
        tol_rel: 0.01,
        tol_abs: 1e-6,
        max_iter: 1000000,
        min_iter: 100,
        window: 10,
        patience: 3,
        use_parallel: false,
        n_workers: undefined,
        seed: undefined
    });

    const [results, setResults] = useState(null);
    const [history, setHistory] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const buildConfig = () => {
        // ... (exact same as before, no changes needed)
        // Build distribution config
        const distConfig = { type: distribution.type };
        if (distribution.type === 'uniform') {
            distConfig.low = parseScalarOrArray(distribution.low);
            distConfig.high = parseScalarOrArray(distribution.high);
        } else if (distribution.type === 'normal') {
            distConfig.mean = parseScalarOrArray(distribution.mean);
            distConfig.std = parseScalarOrArray(distribution.std);
        } else if (distribution.type === 'custom') {
            distConfig.sample_code = distribution.sample_code;
            distConfig.pdf_code = distribution.pdf_code;
            distConfig.ppf_code = distribution.ppf_code;
        }

        // Build objective config
        const objConfig = { type: objective.type };
        if (objective.type === 'builtin') {
            objConfig.name = objective.name;
        } else if (objective.type === 'lambda') {
            objConfig.lambda = objective.lambda;
        } else if (objective.type === 'code') {
            objConfig.code = objective.code;
        }

        // Build technique and proposal
        const techniqueType = technique.type;
        const config = {
            distribution: distConfig,
            objective: objConfig,
            technique: techniqueType,
            batch_size: criterion.batch_size,
            run_mode: runMode,
            use_parallel: criterion.use_parallel,
            seed: criterion.seed,
        };

        if (techniqueType === 'importance') {
            const proposalConfig = { type: proposal.type };
            if (proposal.type === 'uniform') {
                proposalConfig.low = parseScalarOrArray(proposal.low);
                proposalConfig.high = parseScalarOrArray(proposal.high);
            } else if (proposal.type === 'normal') {
                proposalConfig.mean = parseScalarOrArray(proposal.mean);
                proposalConfig.std = parseScalarOrArray(proposal.std);
            } else if (proposal.type === 'custom') {
                proposalConfig.sample_code = proposal.sample_code;
                proposalConfig.pdf_code = proposal.pdf_code;
            }
            config.proposal_distribution = proposalConfig;
        }

        if (criterion.use_parallel && criterion.n_workers) {
            config.n_workers = criterion.n_workers;
        }

        if (runMode === 'fixed') {
            config.n_batches = nBatches;
        } else {
            config.convergence_criterion = {
                tol_rel: criterion.tol_rel,
                tol_abs: criterion.tol_abs,
                max_iter: criterion.max_iter,
                min_iter: criterion.min_iter,
                window: criterion.window,
                patience: criterion.patience
            };
        }

        return config;
    };

    const parseScalarOrArray = (value) => {
        if (typeof value === 'string') {
            try {
                const parsed = JSON.parse(value);
                return parsed;
            } catch {
                const num = parseFloat(value);
                return isNaN(num) ? value : num;
            }
        }
        return value;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResults(null);
        setHistory(null);
        try {
            const config = buildConfig();
            const data = await runSimulation(config);
            if (data.status === 'success') {
                setResults(data.results);
                setHistory(data.history);
            } else {
                setError('Unexpected response format');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <form onSubmit={handleSubmit}>
                <DistributionForm distribution={distribution} setDistribution={setDistribution} />
                <ObjectiveForm objective={objective} setObjective={setObjective} />
                <TechniqueForm
                    technique={technique}
                    setTechnique={setTechnique}
                    proposal={proposal}
                    setProposal={setProposal}
                />
                <ConvergenceForm
                    criterion={criterion}
                    setCriterion={setCriterion}
                    runMode={runMode}
                    setRunMode={setRunMode}
                    nBatches={nBatches}
                    setNBatches={setNBatches}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Running...' : 'Run Simulation'}
                </button>
            </form>
            <ResultsTabs
                results={results}
                history={history}
                error={error}
                loading={loading}
            />
        </Layout>
    );
}

export default App;