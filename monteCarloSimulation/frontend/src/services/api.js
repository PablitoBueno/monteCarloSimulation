import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // adjust if backend runs elsewhere

export const runSimulation = async (config) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/run`, { config });
        return response.data;
    } catch (error) {
        if (error.response) {
            // Server responded with error
            throw new Error(error.response.data.detail || 'Server error');
        } else if (error.request) {
            throw new Error('No response from server. Is the backend running?');
        } else {
            throw new Error(error.message);
        }
    }
};