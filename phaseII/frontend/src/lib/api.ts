import axios, { AxiosResponse } from 'axios';
import { User, Todo, TodoCreate, TodoUpdate } from './types';
import { authClient } from './auth-client';

const API_BASE_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token from custom JWT implementation
api.interceptors.request.use(async (config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Custom Auth API for authentication
export const authAPI = {
  register: async (email: string, password: string) => {
    return await authClient.signUp.email({
      email,
      password,
      callbackURL: '/dashboard'
    });
  },

  login: async (email: string, password: string) => {
    return await authClient.signIn.email({
      email,
      password,
      callbackURL: '/dashboard'
    });
  },

  getMe: async (): Promise<User> => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No active session');
    }

    try {
      // Decode JWT to get user info
      const payload = JSON.parse(atob(token.split('.')[1]));
      return {
        id: payload.sub,
        email: payload.email || '', // Note: email is not currently in the JWT payload
        is_active: true,
        created_at: payload.iat ? new Date(payload.iat * 1000).toISOString() : new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error decoding token:', error);
      throw new Error('Invalid token');
    }
  },

  logout: async () => {
    await authClient.signOut();
  }
};

// Todo API
export const todoAPI = {
  getAll: (): Promise<AxiosResponse<Todo[]>> =>
    api.get('/api/todos'),

  getById: (id: string): Promise<AxiosResponse<Todo>> =>
    api.get(`/api/todos/${encodeURIComponent(id)}`),

  create: (todoData: TodoCreate): Promise<AxiosResponse<Todo>> =>
    api.post('/api/todos', todoData),

  update: (id: string, todoData: TodoUpdate): Promise<AxiosResponse<Todo>> =>
    api.put(`/api/todos/${encodeURIComponent(id)}`, todoData),

  delete: (id: string): Promise<AxiosResponse<any>> =>
    api.delete(`/api/todos/${encodeURIComponent(id)}`)
};

export default api;