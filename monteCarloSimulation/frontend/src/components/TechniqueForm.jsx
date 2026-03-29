import React from 'react';

const TechniqueForm = ({ technique, setTechnique, proposal, setProposal }) => {
    const handleTechniqueChange = (field, value) => {
        setTechnique(prev => ({ ...prev, [field]: value }));
    };

    const handleProposalChange = (field, value) => {
        setProposal(prev => ({ ...prev, [field]: value }));
    };

    const renderProposal = () => {
        if (technique.type !== 'importance') return null;
        return (
            <div className="form-section" style={{ marginTop: '10px', background: '#f9f9f9' }}>
                <h3>Proposal Distribution (for importance sampling)</h3>
                <div className="form-group">
                    <label>Type</label>
                    <select value={proposal.type} onChange={(e) => handleProposalChange('type', e.target.value)}>
                        <option value="uniform">Uniform</option>
                        <option value="normal">Normal</option>
                        <option value="custom">Custom</option>
                    </select>
                </div>
                {proposal.type === 'uniform' && (
                    <>
                        <div className="form-group">
                            <label>Low</label>
                            <input type="text" value={proposal.low || 0} onChange={(e) => handleProposalChange('low', e.target.value)} />
                        </div>
                        <div className="form-group">
                            <label>High</label>
                            <input type="text" value={proposal.high || 1} onChange={(e) => handleProposalChange('high', e.target.value)} />
                        </div>
                    </>
                )}
                {proposal.type === 'normal' && (
                    <>
                        <div className="form-group">
                            <label>Mean</label>
                            <input type="text" value={proposal.mean || 0} onChange={(e) => handleProposalChange('mean', e.target.value)} />
                        </div>
                        <div className="form-group">
                            <label>Std</label>
                            <input type="text" value={proposal.std || 1} onChange={(e) => handleProposalChange('std', e.target.value)} />
                        </div>
                    </>
                )}
                {proposal.type === 'custom' && (
                    <>
                        <div className="form-group">
                            <label>Sample Code</label>
                            <textarea rows="3" value={proposal.sample_code || ''} onChange={(e) => handleProposalChange('sample_code', e.target.value)} />
                        </div>
                        <div className="form-group">
                            <label>PDF Code (optional)</label>
                            <textarea rows="2" value={proposal.pdf_code || ''} onChange={(e) => handleProposalChange('pdf_code', e.target.value)} />
                        </div>
                    </>
                )}
            </div>
        );
    };

    return (
        <div className="form-section">
            <h2>Technique</h2>
            <div className="form-group">
                <label>Type</label>
                <select value={technique.type} onChange={(e) => handleTechniqueChange('type', e.target.value)}>
                    <option value="standard">Standard</option>
                    <option value="importance">Importance Sampling</option>
                    <option value="qmc">Quasi-Monte Carlo (QMC)</option>
                </select>
            </div>
            {renderProposal()}
        </div>
    );
};

export default TechniqueForm;