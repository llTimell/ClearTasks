import axios from 'axios'

const API = axios.create({baseURL:"http://localhost:8000" });

export const login = (credentials) => API.post('/auth/login', credentials);

export const createTask = (task) => API.post('/tasks/create', task);
