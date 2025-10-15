import { useQuery } from '@tanstack/react-query'
import { taskTypesAPI } from '../api/taskTypes'
import { useCurrentTask } from '../hooks/useCurrentTask'

export default function QuickStartGrid() {
  const { currentTask, startTask, interruptTask, isStarting, isInterrupting } = useCurrentTask()

  // Get pinned task types
  const { data: taskTypes = [] } = useQuery({
    queryKey: ['taskTypes', 'pinned'],
    queryFn: () => taskTypesAPI.list(false),
    select: (data) => data.filter((t) => t.is_pinned),
  })

  const handleTaskClick = (taskTypeId: number, taskTypeName: string) => {
    if (currentTask) {
      // Ask to interrupt
      if (
        confirm(
          `Stop tracking "${currentTask.task_type_detail.name}" and start "${taskTypeName}"?`
        )
      ) {
        interruptTask({ taskTypeId })
      }
    } else {
      startTask({ taskTypeId })
    }
  }

  if (taskTypes.length === 0) {
    return (
      <div className="text-center py-8 text-text-secondary">
        <p>No pinned tasks. Go to Settings to pin your favorite tasks!</p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-xl font-bold text-text-primary mb-4">Quick Start</h2>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mb-6">
        {taskTypes.map((taskType) => (
          <button
            key={taskType.id}
            onClick={() => handleTaskClick(taskType.id, taskType.name)}
            disabled={isStarting || isInterrupting}
            className={`
              relative p-4 rounded-lg border-2 transition-all
              ${
                currentTask
                  ? 'bg-bg-tertiary border-gray-700 opacity-60'
                  : 'bg-bg-secondary border-gray-600 hover:border-accent hover:bg-bg-tertiary'
              }
              disabled:cursor-not-allowed
              flex flex-col items-center justify-center space-y-2
              min-h-[100px]
            `}
            style={{
              borderColor: !currentTask ? taskType.color : undefined,
            }}
          >
            <span className="text-3xl">{taskType.emoji}</span>
            <span className="text-sm font-medium text-text-primary text-center">
              {taskType.name}
            </span>
            {currentTask && (
              <span className="text-xs text-text-secondary">Tap to switch</span>
            )}
          </button>
        ))}
      </div>
    </div>
  )
}

