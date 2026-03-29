import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const ConvergenceChart = ({ history }) => {
    if (!history || !history.mean_history || history.mean_history.length === 0) {
        return <div className="chart-placeholder">No convergence data available. Run simulation first.</div>;
    }

    const data = {
        labels: history.iterations,
        datasets: [
            {
                label: 'Mean Estimate',
                data: history.mean_history,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                fill: true,
                tension: 0.1,
            },
            {
                label: 'Upper CI (95%)',
                data: history.upper_ci,
                borderColor: 'rgba(255, 99, 132, 0.5)',
                borderDash: [5, 5],
                fill: false,
                tension: 0.1,
            },
            {
                label: 'Lower CI (95%)',
                data: history.lower_ci,
                borderColor: 'rgba(255, 99, 132, 0.5)',
                borderDash: [5, 5],
                fill: false,
                tension: 0.1,
            }
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Convergence of Monte Carlo Simulation' },
            tooltip: { mode: 'index', intersect: false },
        },
        scales: {
            x: { title: { display: true, text: 'Iteration (Batch)' } },
            y: { title: { display: true, text: 'Estimated Mean' } },
        },
    };

    return (
        <div className="chart-container" style={{ height: '400px' }}>
            <Line data={data} options={options} />
        </div>
    );
};

export default ConvergenceChart;