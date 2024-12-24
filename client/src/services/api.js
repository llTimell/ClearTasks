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




export const createTask = async (task) => {
  try {
    const response = await axios.post(`${API_URL}/tasks/create`, task);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getTasks = async () => {
  try {
    const response = await axios.get(`${API_URL}/tasks`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteTask = async (title) => {
  try {
    const response = await axios.delete(`${API_URL}/tasks/delete/${title}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateTaskStatus = async (title, status) => {
  try {
    const response = await axios.put(`${API_URL}/tasks/update/${title}`, { status });
    return response.data;
  } catch (error) {
    throw error;
  }
};