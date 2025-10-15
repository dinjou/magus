import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import CurrentTaskCard from '../components/CurrentTaskCard'
import QuickStartGrid from '../components/QuickStartGrid'
import TaskHistory from '../components/TaskHistory'

export default function DashboardPage() {
  const { logout } = useAuthStore()

  const handleLogout = async () => {
    await logout()
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-accent">MAGUS</h1>
          <div className="flex items-center space-x-4">
            <Link
              to="/settings"
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90"
            >
              Settings
            </Link>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-error text-white rounded hover:bg-opacity-90"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Currently Tracking Card */}
        <CurrentTaskCard />

        {/* Quick Start Grid */}
        <QuickStartGrid />

        {/* Task History */}
        <TaskHistory />
      </div>
    </div>
  )
}

