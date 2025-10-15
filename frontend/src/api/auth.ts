import apiClient from './axios'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password2: string
  first_name?: string
  last_name?: string
}

export interface AuthResponse {
  user: {
    id: number
    username: string
    email: string
    first_name: string
    last_name: string
    date_joined: string
  }
  tokens: {
    access: string
    refresh: string
  }
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  date_joined: string
}

export const authAPI = {
  // Register new user
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/register/', data)
    return response.data
  },

  // Login
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login/', credentials)
    return response.data
  },

  // Logout
  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout/')
  },

  // Get current user
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me/')
    return response.data
  },

  // Refresh token
  refreshToken: async (refresh: string): Promise<{ access: string }> => {
    const response = await apiClient.post('/auth/refresh/', { refresh })
    return response.data
  },
}

