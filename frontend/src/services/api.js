import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Thay đổi nếu backend chạy trên port khác

export const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${API_URL}/register`, userData);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};

export const loginUser = async () => {
    try {
        const response = await axios.post(`${API_URL}/login`);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};
