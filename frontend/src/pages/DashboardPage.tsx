import { Link } from 'react-router-dom'
import CurrentTaskCard from '../components/CurrentTaskCard'
import QuickStartGrid from '../components/QuickStartGrid'
import TaskHistory from '../components/TaskHistory'
import TodaysSummary from '../components/TodaysSummary'

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="container mx-auto px-4 py-6 max-w-6xl">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
          <Link to="/dashboard" className="flex items-center space-x-3 no-underline hover:opacity-80 transition-opacity">
            <img src="/favicon.ico" alt="MAGUS" className="w-8 h-8" />
            <h1 className="text-4xl font-bold text-accent">MAGUS</h1>
          </Link>
          <div className="flex items-center gap-2 flex-wrap">
            <Link
              to="/analytics"
              className="px-4 py-2 bg-accent text-white rounded hover:bg-opacity-90 transition-all text-sm sm:text-base whitespace-nowrap"
            >
              Analytics
            </Link>
            <Link
              to="/settings"
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90 transition-all text-sm sm:text-base whitespace-nowrap"
            >
              Settings
            </Link>
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

