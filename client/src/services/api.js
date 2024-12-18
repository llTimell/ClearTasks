import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const login = async ({ username, password }) => {
  try {
    const response = await axios.post(`${API_URL}/auth/login`, { username, password });
    return response;
  } catch (error) {
    throw error;
  }
};

export const register = async ({ username, email, password }) => {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, {
      username,
      email,
      password,
    });
    return response;
  } catch (error) {
    throw error;
  }
};
