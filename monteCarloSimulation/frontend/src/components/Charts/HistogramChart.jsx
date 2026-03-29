import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const HistogramChart = ({ samples }) => {
    if (!samples || samples.length === 0) {
        return <div className="chart-placeholder">No sample data available. Run simulation first.</div>;
    }

    // Use a subset for performance (e.g., last 10k samples)
    const displaySamples = samples.length > 10000 ? samples.slice(-10000) : samples;

    // Create histogram bins
    const min = Math.min(...displaySamples);
    const max = Math.max(...displaySamples);
    const numBins = 30;
    const binWidth = (max - min) / numBins;
    const bins = Array(numBins).fill(0);
    displaySamples.forEach(value => {
        const binIndex = Math.min(Math.floor((value - min) / binWidth), numBins - 1);
        bins[binIndex]++;
    });

    const labels = Array(numBins).fill().map((_, i) =>
        (min + i * binWidth).toFixed(3)
    );

    const data = {
        labels,
        datasets: [{
            label: 'Frequency',
            data: bins,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Distribution of Objective Function Values' },
        },
        scales: {
            x: { title: { display: true, text: 'Objective Value' } },
            y: { title: { display: true, text: 'Frequency' } },
        },
    };

    return (
        <div className="chart-container" style={{ height: '400px' }}>
            <Bar data={data} options={options} />
        </div>
    );
};

export default HistogramChart;