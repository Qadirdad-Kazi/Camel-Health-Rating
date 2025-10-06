import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email, password) => 
    api.post('/api/auth/login', { email, password }),
  
  register: (userData) => 
    api.post('/api/auth/register', userData),
  
  getCurrentUser: () => 
    api.get('/api/auth/me').then(res => res.data),
};

// Prediction API
export const predictionAPI = {
  predict: (formData) => 
    api.post('/api/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  
  predictAnonymous: (formData) => 
    api.post('/api/predict-anonymous', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  
  getImageDetails: (imageId) => 
    api.get(`/api/image/${imageId}`).then(res => res.data),
};

// Feedback API
export const feedbackAPI = {
  submitFeedback: (feedbackData) => 
    api.post('/api/feedback', feedbackData),
  
  getImageFeedback: (imageId) => 
    api.get(`/api/feedback/${imageId}`).then(res => res.data),
  
  getFeedbackStats: (imageId) => 
    api.get(`/api/feedback-stats/${imageId}`).then(res => res.data),
};

// History API
export const historyAPI = {
  getUserHistory: (params = {}) => 
    api.get('/api/history', { params }).then(res => res.data),
  
  getUserStats: () => 
    api.get('/api/history/stats').then(res => res.data),
  
  deleteImage: (imageId) => 
    api.delete(`/api/history/${imageId}`),
};

export default api;
