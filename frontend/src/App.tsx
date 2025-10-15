import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-bg-primary text-text-primary">
          <div className="container mx-auto px-4 py-8">
            <h1 className="text-4xl font-bold text-accent mb-4">MAGUS</h1>
            <p className="text-text-secondary">
              Personal time tracking and life analytics platform
            </p>
            <p className="mt-4 text-success">✓ Frontend setup complete!</p>
            <p className="text-text-secondary text-sm mt-2">
              React + TypeScript + Vite + TailwindCSS + TanStack Query
            </p>
          </div>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App

