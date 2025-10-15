import { create } from 'zustand'

interface ThemeState {
  theme: 'dark' | 'light'
  toggleTheme: () => void
  setTheme: (theme: 'dark' | 'light') => void
}

export const useTheme = create<ThemeState>((set) => ({
  theme: (localStorage.getItem('magus-theme') as 'dark' | 'light') || 'dark',
  toggleTheme: () =>
    set((state) => {
      const newTheme = state.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('magus-theme', newTheme)
      return { theme: newTheme }
    }),
  setTheme: (theme) => {
    localStorage.setItem('magus-theme', theme)
    set({ theme })
  },
}))

