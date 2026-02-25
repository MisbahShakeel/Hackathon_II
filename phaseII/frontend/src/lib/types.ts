export interface User {
  id: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}