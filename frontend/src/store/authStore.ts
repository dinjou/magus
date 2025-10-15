import { create } from 'zustand'
import { authAPI, User } from '../api/auth'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  
  // Actions
  setUser: (user: User | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  login: (username: string, password: string) => Promise<void>
  register: (data: any) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  setUser: (user) => set({ user, isAuthenticated: !!user }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),

  login: async (username, password) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authAPI.login({ username, password })
      
      // Store tokens
      localStorage.setItem('access_token', response.tokens.access)
      localStorage.setItem('refresh_token', response.tokens.refresh)
      
      // Set user
      set({ user: response.user, isAuthenticated: true, isLoading: false })
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Login failed'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  register: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authAPI.register(data)
      
      // Store tokens
      localStorage.setItem('access_token', response.tokens.access)
      localStorage.setItem('refresh_token', response.tokens.refresh)
      
      // Set user
      set({ user: response.user, isAuthenticated: true, isLoading: false })
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Registration failed'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  logout: async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear tokens
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      
      // Clear user
      set({ user: null, isAuthenticated: false })
    }
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      set({ isAuthenticated: false, user: null })
      return
    }

    set({ isLoading: true })
    try {
      const user = await authAPI.getCurrentUser()
      set({ user, isAuthenticated: true, isLoading: false })
    } catch (error) {
      // Token invalid, clear it
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      set({ user: null, isAuthenticated: false, isLoading: false })
    }
  },
}))

