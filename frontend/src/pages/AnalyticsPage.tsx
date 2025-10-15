import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts'
import { analyticsAPI } from '../api/analytics'

type ViewMode = 'today' | 'week' | 'month'

export default function AnalyticsPage() {
  const [viewMode, setViewMode] = useState<ViewMode>('today')

  // Fetch data based on view mode
  const { data: todayData } = useQuery({
    queryKey: ['analytics', 'today'],
    queryFn: analyticsAPI.getTodaySummary,
    enabled: viewMode === 'today',
  })

  const { data: weekData } = useQuery({
    queryKey: ['analytics', 'week'],
    queryFn: () => analyticsAPI.getWeeklyBreakdown(),
    enabled: viewMode === 'week',
  })

  const { data: monthData } = useQuery({
    queryKey: ['analytics', 'month'],
    queryFn: () => analyticsAPI.getMonthlyBreakdown(),
    enabled: viewMode === 'month',
  })

  const currentData = viewMode === 'today' ? todayData : viewMode === 'week' ? weekData : monthData

  // Prepare chart data
  const chartData = currentData?.task_types?.map((tt: any) => ({
    name: tt.task_type_name,
    value: tt.total_duration / 3600, // Convert to hours
    duration: tt.duration_formatted,
    emoji: tt.task_type_emoji,
    color: tt.task_type_color,
  })) || []

  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
          <Link to="/dashboard" className="flex items-center space-x-3 no-underline hover:opacity-80 transition-opacity">
            <img src="/favicon.ico" alt="MAGUS" className="w-8 h-8" />
            <h1 className="text-4xl font-bold text-accent">Analytics</h1>
          </Link>
          <div className="flex items-center gap-2 flex-wrap">
            <Link
              to="/dashboard"
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90 text-sm sm:text-base whitespace-nowrap"
            >
              Dashboard
            </Link>
            <Link
              to="/settings"
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90 text-sm sm:text-base whitespace-nowrap"
            >
              Settings
            </Link>
          </div>
        </div>

        {/* View Mode Selector */}
        <div className="flex space-x-2 mb-6">
          <button
            onClick={() => setViewMode('today')}
            className={`px-4 py-2 rounded ${
              viewMode === 'today'
                ? 'bg-accent text-white'
                : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
            }`}
          >
            Today
          </button>
          <button
            onClick={() => setViewMode('week')}
            className={`px-4 py-2 rounded ${
              viewMode === 'week'
                ? 'bg-accent text-white'
                : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
            }`}
          >
            This Week
          </button>
          <button
            onClick={() => setViewMode('month')}
            className={`px-4 py-2 rounded ${
              viewMode === 'month'
                ? 'bg-accent text-white'
                : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
            }`}
          >
            This Month
          </button>
        </div>

        {/* Summary Stats */}
        {currentData && (
          <div className="bg-bg-secondary rounded-lg p-6 mb-6">
            <div className="text-center">
              <div className="text-text-secondary text-sm mb-2">Total Time Tracked</div>
              <div className="text-4xl font-bold text-accent">
                {currentData.total_tracked_formatted || '0h 0m'}
              </div>
              {weekData && viewMode === 'week' && (
                <div className="text-text-secondary text-sm mt-2">
                  {weekData.start_date} to {weekData.end_date}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Charts */}
        {chartData.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Bar Chart */}
            <div className="bg-bg-secondary rounded-lg p-6">
              <h3 className="text-lg font-bold text-text-primary mb-4">Time by Task</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <XAxis dataKey="name" stroke="#B9BBBE" fontSize={12} />
                  <YAxis stroke="#B9BBBE" fontSize={12} label={{ value: 'Hours', angle: -90, position: 'insideLeft' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#23272A', border: '1px solid #40444B' }}
                    labelStyle={{ color: '#FFFFFF' }}
                    itemStyle={{ color: '#B9BBBE' }}
                  />
                  <Bar dataKey="value" fill="#7289DA">
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Pie Chart */}
            <div className="bg-bg-secondary rounded-lg p-6">
              <h3 className="text-lg font-bold text-text-primary mb-4">Time Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={(entry) => `${entry.emoji} ${entry.name}`}
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#23272A', border: '1px solid #40444B' }}
                    itemStyle={{ color: '#B9BBBE' }}
                    formatter={(value: number) => `${value.toFixed(2)}h`}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        ) : (
          <div className="bg-bg-secondary rounded-lg p-12 text-center">
            <div className="text-text-secondary text-lg">
              No data available for this period
            </div>
            <div className="text-text-secondary text-sm mt-2">
              Start tracking your time to see analytics!
            </div>
          </div>
        )}

        {/* Detailed Breakdown */}
        {chartData.length > 0 && (
          <div className="bg-bg-secondary rounded-lg p-6 mt-6">
            <h3 className="text-lg font-bold text-text-primary mb-4">Detailed Breakdown</h3>
            <div className="space-y-2">
              {currentData?.task_types?.map((taskType: any) => (
                <div
                  key={taskType.task_type_id}
                  className="flex items-center justify-between p-3 bg-bg-tertiary rounded"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{taskType.task_type_emoji}</span>
                    <div>
                      <div className="font-medium text-text-primary">
                        {taskType.task_type_name}
                      </div>
                      {taskType.task_count && (
                        <div className="text-xs text-text-secondary">
                          {taskType.task_count} {taskType.task_count === 1 ? 'session' : 'sessions'}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-accent">{taskType.duration_formatted}</div>
                    <div className="text-xs text-text-secondary">{taskType.percentage.toFixed(1)}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

