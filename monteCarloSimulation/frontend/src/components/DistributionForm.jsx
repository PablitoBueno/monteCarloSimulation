import React from 'react';

const DistributionForm = ({ distribution, setDistribution }) => {
    const handleChange = (field, value) => {
        setDistribution(prev => ({ ...prev, [field]: value }));
    };

    const renderParams = () => {
        switch (distribution.type) {
            case 'uniform':
                return (
                    <>
                        <div className="form-group">
                            <label>Low (scalar or array)</label>
                            <input
                                type="text"
                                value={distribution.low || 0}
                                onChange={(e) => handleChange('low', e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>High (scalar or array)</label>
                            <input
                                type="text"
                                value={distribution.high || 1}
                                onChange={(e) => handleChange('high', e.target.value)}
                            />
                        </div>
                    </>
                );
            case 'normal':
                return (
                    <>
                        <div className="form-group">
                            <label>Mean (scalar or array)</label>
                            <input
                                type="text"
                                value={distribution.mean || 0}
                                onChange={(e) => handleChange('mean', e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Std (scalar or array, positive)</label>
                            <input
                                type="text"
                                value={distribution.std || 1}
                                onChange={(e) => handleChange('std', e.target.value)}
                            />
                        </div>
                    </>
                );
            case 'custom':
                return (
                    <>
                        <div className="form-group">
                            <label>Sample Code (define sample_func(n))</label>
                            <textarea
                                rows="5"
                                value={distribution.sample_code || ''}
                                onChange={(e) => handleChange('sample_code', e.target.value)}
                                placeholder="def sample_func(n):&#10;    return np.random.randn(n, 1)"
                            />
                        </div>
                        <div className="form-group">
                            <label>PDF Code (optional, define pdf_func(x))</label>
                            <textarea
                                rows="3"
                                value={distribution.pdf_code || ''}
                                onChange={(e) => handleChange('pdf_code', e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>PPF Code (optional, define ppf_func(u))</label>
                            <textarea
                                rows="3"
                                value={distribution.ppf_code || ''}
                                onChange={(e) => handleChange('ppf_code', e.target.value)}
                            />
                        </div>
                    </>
                );
            default:
                return null;
        }
    };

    return (
        <div className="form-section">
            <h2>Distribution</h2>
            <div className="form-group">
                <label>Type</label>
                <select value={distribution.type} onChange={(e) => handleChange('type', e.target.value)}>
                    <option value="uniform">Uniform</option>
                    <option value="normal">Normal</option>
                    <option value="custom">Custom</option>
                </select>
            </div>
            {renderParams()}
        </div>
    );
};

export default DistributionForm;