/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Discord-dark theme colors
        'bg-primary': '#2C2F33',
        'bg-secondary': '#23272A',
        'bg-tertiary': '#1E2124',
        'text-primary': '#FFFFFF',
        'text-secondary': '#B9BBBE',
        'accent': '#7289DA',
        'success': '#3A8E61',
        'error': '#B35A5A',
        'warning': '#8B7D5A',
      },
    },
  },
  plugins: [],
}

