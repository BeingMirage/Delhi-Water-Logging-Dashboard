import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const getWards = async () => {
    const response = await axios.get(`${API_URL}/wards`);
    return response.data;
};

export const getWardDetail = async (id) => {
    const response = await axios.get(`${API_URL}/ward/${id}`);
    return response.data;
};

export const getMapData = async () => {
    const response = await axios.get(`${API_URL}/map-data`);
    return response.data;
};
