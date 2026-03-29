import React from 'react';

const ObjectiveForm = ({ objective, setObjective }) => {
    const handleChange = (field, value) => {
        setObjective(prev => ({ ...prev, [field]: value }));
    };

    const renderParams = () => {
        switch (objective.type) {
            case 'builtin':
                return (
                    <div className="form-group">
                        <label>Name</label>
                        <select value={objective.name || 'sum_squares'} onChange={(e) => handleChange('name', e.target.value)}>
                            <option value="sum_squares">sum_squares</option>
                            <option value="sum">sum</option>
                            <option value="exp_sum">exp_sum</option>
                            <option value="identity_first">identity_first</option>
                        </select>
                    </div>
                );
            case 'lambda':
                return (
                    <div className="form-group">
                        <label>Lambda Expression (string, e.g., "lambda x: np.sum(x**2, axis=1)")</label>
                        <input
                            type="text"
                            value={objective.lambda || ''}
                            onChange={(e) => handleChange('lambda', e.target.value)}
                        />
                    </div>
                );
            case 'code':
                return (
                    <div className="form-group">
                        <label>Python Code (must define objective_func(x))</label>
                        <textarea
                            rows="5"
                            value={objective.code || ''}
                            onChange={(e) => handleChange('code', e.target.value)}
                            placeholder="def objective_func(x):&#10;    return np.sum(x**2, axis=1)"
                        />
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="form-section">
            <h2>Objective Function</h2>
            <div className="form-group">
                <label>Type</label>
                <select value={objective.type} onChange={(e) => handleChange('type', e.target.value)}>
                    <option value="builtin">Built-in</option>
                    <option value="lambda">Lambda</option>
                    <option value="code">Code</option>
                </select>
            </div>
            {renderParams()}
        </div>
    );
};

export default ObjectiveForm;