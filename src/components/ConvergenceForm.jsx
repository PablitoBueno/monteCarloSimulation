import React from 'react';

const ConvergenceForm = ({ criterion, setCriterion, runMode, setRunMode, nBatches, setNBatches }) => {
    const handleCriterionChange = (field, value) => {
        setCriterion(prev => ({ ...prev, [field]: value }));
    };

    return (
        <div className="form-section">
            <h2>Run Configuration</h2>
            <div className="form-group">
                <label>Run Mode</label>
                <select value={runMode} onChange={(e) => setRunMode(e.target.value)}>
                    <option value="adaptive">Adaptive (convergence based)</option>
                    <option value="fixed">Fixed number of batches</option>
                </select>
            </div>
            {runMode === 'fixed' && (
                <div className="form-group">
                    <label>Number of Batches</label>
                    <input
                        type="number"
                        value={nBatches}
                        onChange={(e) => setNBatches(parseInt(e.target.value) || 0)}
                        min="1"
                    />
                </div>
            )}
            <div className="form-group">
                <label>Batch Size</label>
                <input
                    type="number"
                    value={criterion.batch_size}
                    onChange={(e) => handleCriterionChange('batch_size', parseInt(e.target.value) || 1000)}
                    min="1"
                />
            </div>
            {runMode === 'adaptive' && (
                <>
                    <h3>Convergence Criterion</h3>
                    <div className="form-group">
                        <label>Tolerance Relative (%)</label>
                        <input
                            type="number"
                            step="0.001"
                            value={criterion.tol_rel}
                            onChange={(e) => handleCriterionChange('tol_rel', parseFloat(e.target.value))}
                        />
                    </div>
                    <div className="form-group">
                        <label>Tolerance Absolute</label>
                        <input
                            type="number"
                            step="1e-6"
                            value={criterion.tol_abs}
                            onChange={(e) => handleCriterionChange('tol_abs', parseFloat(e.target.value))}
                        />
                    </div>
                    <div className="form-group">
                        <label>Max Iterations</label>
                        <input
                            type="number"
                            value={criterion.max_iter}
                            onChange={(e) => handleCriterionChange('max_iter', parseInt(e.target.value) || 1000000)}
                        />
                    </div>
                    <div className="form-group">
                        <label>Min Iterations</label>
                        <input
                            type="number"
                            value={criterion.min_iter}
                            onChange={(e) => handleCriterionChange('min_iter', parseInt(e.target.value) || 100)}
                        />
                    </div>
                    <div className="form-group">
                        <label>Window</label>
                        <input
                            type="number"
                            value={criterion.window}
                            onChange={(e) => handleCriterionChange('window', parseInt(e.target.value) || 10)}
                        />
                    </div>
                    <div className="form-group">
                        <label>Patience</label>
                        <input
                            type="number"
                            value={criterion.patience}
                            onChange={(e) => handleCriterionChange('patience', parseInt(e.target.value) || 3)}
                        />
                    </div>
                </>
            )}
            <div className="form-group">
                <label>Use Parallel</label>
                <input
                    type="checkbox"
                    checked={criterion.use_parallel || false}
                    onChange={(e) => handleCriterionChange('use_parallel', e.target.checked)}
                />
            </div>
            {criterion.use_parallel && (
                <div className="form-group">
                    <label>Number of Workers (optional)</label>
                    <input
                        type="number"
                        value={criterion.n_workers || ''}
                        onChange={(e) => handleCriterionChange('n_workers', parseInt(e.target.value) || undefined)}
                        min="1"
                    />
                </div>
            )}
            <div className="form-group">
                <label>Seed (optional)</label>
                <input
                    type="number"
                    value={criterion.seed || ''}
                    onChange={(e) => handleCriterionChange('seed', parseInt(e.target.value) || undefined)}
                />
            </div>
        </div>
    );
};

export default ConvergenceForm;