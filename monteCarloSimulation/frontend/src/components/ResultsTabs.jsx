import React, { useState } from 'react';
import ResultsDisplay from './ResultsDisplay';
import ConvergenceChart from './Charts/ConvergenceChart';
import HistogramChart from './Charts/HistogramChart';
import ErrorAnalysisChart from './Charts/ErrorAnalysisChart';

const ResultsTabs = ({ results, history, error, loading }) => {
    const [activeTab, setActiveTab] = useState('results');

    if (loading) {
        return <div className="results-tabs loading">Processing results...</div>;
    }

    if (error) {
        return <div className="results-tabs error">Error: {error}</div>;
    }

    if (!results && !history) return null;

    const tabs = [
        { id: 'results', label: '📊 Results' },
        { id: 'convergence', label: '📈 Convergence' },
        { id: 'distribution', label: '📉 Distribution' },
        { id: 'error', label: '⚠️ Error Analysis' }
    ];

    return (
        <div className="results-tabs">
            <div className="tabs-header">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            <div className="tab-content">
                {activeTab === 'results' && <ResultsDisplay results={results} error={error} loading={loading} />}
                {activeTab === 'convergence' && <ConvergenceChart history={history} />}
                {activeTab === 'distribution' && <HistogramChart samples={history?.all_samples} />}
                {activeTab === 'error' && <ErrorAnalysisChart history={history} />}
            </div>
        </div>
    );
};

export default ResultsTabs;