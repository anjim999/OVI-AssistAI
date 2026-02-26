import axios from 'axios';

const baseURL = import.meta.env.VITE_API_R_URL || '';

const axiosClient = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default axiosClient;

