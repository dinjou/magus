import { useState, useEffect } from 'react'
import { useCurrentTask } from '../hooks/useCurrentTask'
import { formatDistanceToNow } from 'date-fns'

export default function CurrentTaskCard() {
  const { currentTask, stopTask, isStopping } = useCurrentTask()
  const [elapsed, setElapsed] = useState('')

  useEffect(() => {
    if (!currentTask) return

    const updateElapsed = () => {
      const start = new Date(currentTask.start_time)
      const duration = formatDistanceToNow(start, { includeSeconds: true })
      setElapsed(duration)
    }

    updateElapsed()
    const interval = setInterval(updateElapsed, 1000)

    return () => clearInterval(interval)
  }, [currentTask])

  if (!currentTask) {
    return null
  }

  const handleStop = () => {
    if (confirm('Stop tracking this task?')) {
      stopTask()
    }
  }

  return (
    <div className="bg-gradient-to-r from-accent to-blue-600 rounded-lg p-6 shadow-lg mb-6">
      <div className="text-white">
        <div className="text-sm opacity-90 mb-2">Currently Tracking</div>
        
        <div className="flex items-center space-x-4 mb-4">
          <span className="text-4xl">{currentTask.task_type_detail.emoji}</span>
          <div className="flex-1">
            <h2 className="text-2xl font-bold">{currentTask.task_type_detail.name}</h2>
            <div className="flex items-center space-x-4 mt-2">
              <div className="flex items-center space-x-2">
                <svg
                  className="w-5 h-5 animate-pulse"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-lg font-mono">{elapsed}</span>
              </div>
              <div className="text-sm opacity-75">
                Started {new Date(currentTask.start_time).toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>

        <button
          onClick={handleStop}
          disabled={isStopping}
          className="w-full bg-white text-accent font-semibold py-3 px-6 rounded-lg hover:bg-opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z"
              clipRule="evenodd"
            />
          </svg>
          <span>{isStopping ? 'Stopping...' : 'Stop Tracking'}</span>
        </button>
      </div>
    </div>
  )
}

