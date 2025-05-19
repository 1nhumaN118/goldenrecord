import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const res = await axios.post(`${API_URL}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return res.data;
};

export const getPairs = async () => {
  const res = await axios.get(`${API_URL}/predict`);
  return res.data.pairs;
};

export const sendFeedback = async (feedback: any) => {
  const res = await axios.post(`${API_URL}/feedback`, feedback);
  return res.data;
};

export const downloadReport = async () => {
  const res = await axios.get(`${API_URL}/report`, {
    responseType: 'blob'
  });
  return res;
};