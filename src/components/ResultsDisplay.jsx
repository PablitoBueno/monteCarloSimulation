import React from 'react';

const ResultsDisplay = ({ results, error, loading }) => {
    if (loading) {
        return <div className="results">Running simulation...</div>;
    }

    if (error) {
        return <div className="results error">Error: {error}</div>;
    }

    if (!results) {
        return null;
    }

    const { samples_processed, mean_estimate, variance_sample, standard_error, relative_error_percent, '95ci_lower': ciLower, '95ci_upper': ciUpper } = results;

    return (
        <div className="results">
            <h2>Results</h2>
            <div className="result-item"><strong>Samples Processed:</strong> {samples_processed}</div>
            <div className="result-item"><strong>Mean Estimate:</strong> {mean_estimate?.toExponential(6)}</div>
            <div className="result-item"><strong>Sample Variance:</strong> {variance_sample?.toExponential(6)}</div>
            <div className="result-item"><strong>Standard Error:</strong> {standard_error?.toExponential(6)}</div>
            <div className="result-item"><strong>Relative Error (%):</strong> {relative_error_percent?.toFixed(4)}%</div>
            <div className="result-item"><strong>95% Confidence Interval:</strong> [{ciLower?.toExponential(6)}, {ciUpper?.toExponential(6)}]</div>
        </div>
    );
};

export default ResultsDisplay;