import { useQuery } from '@tanstack/react-query'
import { analyticsAPI } from '../api/analytics'

export default function TodaysSummary() {
  const { data: summary, isLoading } = useQuery({
    queryKey: ['todaySummary'],
    queryFn: analyticsAPI.getTodaySummary,
    refetchInterval: 60000, // Refresh every minute
  })

  if (isLoading) {
    return (
      <div className="bg-bg-secondary rounded-lg p-6 mb-6">
        <h2 className="text-xl font-bold text-text-primary mb-4">Today's Summary</h2>
        <div className="text-text-secondary">Loading...</div>
      </div>
    )
  }

  if (!summary || summary.task_types.length === 0) {
    return (
      <div className="bg-bg-secondary rounded-lg p-6 mb-6">
        <h2 className="text-xl font-bold text-text-primary mb-4">Today's Summary</h2>
        <div className="text-text-secondary text-center py-4">
          No time tracked today yet. Start tracking to see your summary!
        </div>
      </div>
    )
  }

  return (
    <div className="bg-bg-secondary rounded-lg p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-text-primary">Today's Summary</h2>
        <div className="text-accent font-bold text-lg">{summary.total_tracked_formatted}</div>
      </div>

      <div className="space-y-3">
        {summary.task_types.map((taskType) => (
          <div key={taskType.task_type_id} className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-2">
                <span className="text-lg">{taskType.task_type_emoji}</span>
                <span className="text-text-primary font-medium">{taskType.task_type_name}</span>
              </div>
              <span className="text-text-secondary">{taskType.duration_formatted}</span>
            </div>
            
            {/* Progress bar */}
            <div className="w-full bg-bg-tertiary rounded-full h-2">
              <div
                className="h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${taskType.percentage}%`,
                  backgroundColor: taskType.task_type_color,
                }}
              />
            </div>
            
            <div className="flex justify-between text-xs text-text-secondary">
              <span>{taskType.percentage.toFixed(1)}% of today</span>
              {taskType.interrupted_count && taskType.interrupted_count > 0 && (
                <span className="text-warning">
                  {taskType.interrupted_count} interrupted
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

