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
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const ErrorAnalysisChart = ({ history }) => {
    if (!history || !history.std_error_history || history.std_error_history.length === 0) {
        return <div className="chart-placeholder">No error data available. Run simulation first.</div>;
    }

    const data = {
        labels: history.iterations,
        datasets: [
            {
                label: 'Standard Error',
                data: history.std_error_history,
                borderColor: 'rgb(255, 159, 64)',
                backgroundColor: 'rgba(255, 159, 64, 0.1)',
                fill: true,
                tension: 0.1,
                yAxisID: 'y',
            },
            {
                label: 'Relative Error (%)',
                data: history.rel_error_history,
                borderColor: 'rgb(153, 102, 255)',
                borderDash: [5, 5],
                fill: false,
                tension: 0.1,
                yAxisID: 'y1',
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Error Analysis' },
        },
        scales: {
            x: { title: { display: true, text: 'Iteration (Batch)' } },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: { display: true, text: 'Standard Error' },
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: { display: true, text: 'Relative Error (%)' },
                grid: { drawOnChartArea: false },
            },
        },
    };

    return (
        <div className="chart-container" style={{ height: '400px' }}>
            <Line data={data} options={options} />
        </div>
    );
};

export default ErrorAnalysisChart;