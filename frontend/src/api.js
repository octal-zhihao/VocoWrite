import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Django后端的URL
  timeout: 10000,
});

export default api;
