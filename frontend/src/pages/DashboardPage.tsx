import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import CurrentTaskCard from '../components/CurrentTaskCard'
import QuickStartGrid from '../components/QuickStartGrid'
import TaskHistory from '../components/TaskHistory'
import TodaysSummary from '../components/TodaysSummary'
import ThemeToggle from '../components/ThemeToggle'

export default function DashboardPage() {
  const { logout } = useAuthStore()

  const handleLogout = async () => {
    await logout()
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen bg-bg-primary transition-colors duration-200">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-accent">MAGUS</h1>
          <div className="flex items-center space-x-2">
            <ThemeToggle />
            <Link
              to="/analytics"
              className="px-4 py-2 bg-accent text-white rounded hover:bg-opacity-90 transition-all"
            >
              Analytics
            </Link>
            <Link
              to="/settings"
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90 transition-all"
            >
              Settings
            </Link>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-error text-white rounded hover:bg-opacity-90 transition-all"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Currently Tracking Card */}
        <CurrentTaskCard />

        {/* Quick Start Grid */}
        <QuickStartGrid />

        {/* Today's Summary */}
        <TodaysSummary />

        {/* Task History */}
        <TaskHistory />
      </div>
    </div>
  )
}

