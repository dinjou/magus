import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tantml:function_calls>
<invoke name="tasks">
import { tasksAPI, Task } from '../api/tasks'
import { formatDistance, formatDuration, intervalToDuration } from 'date-fns'

export default function TaskHistory() {
  const queryClient = useQueryClient()
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  const { data: tasks = [], isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => tasksAPI.list(),
  })

  const deleteMutation = useMutation({
    mutationFn: tasksAPI.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Task> }) =>
      tasksAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      setEditingTask(null)
    },
  })

  const formatDurationSeconds = (seconds: number) => {
    const duration = intervalToDuration({ start: 0, end: seconds * 1000 })
    const hours = duration.hours || 0
    const minutes = duration.minutes || 0
    return `${hours}h ${minutes}m`
  }

  const handleEdit = (task: Task) => {
    setEditingTask(task)
  }

  const handleDelete = (task: Task) => {
    if (confirm(`Delete "${task.task_type_detail.name}" task?`)) {
      deleteMutation.mutate(task.id)
    }
  }

  if (isLoading) {
    return <div className="text-text-secondary">Loading tasks...</div>
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8 text-text-secondary">
        <p>No tasks tracked yet. Start tracking to see your history!</p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-xl font-bold text-text-primary mb-4">Recent Activity</h2>
      
      <div className="space-y-2">
        {tasks.slice(0, 10).map((task) => (
          <div
            key={task.id}
            className="bg-bg-secondary p-4 rounded-lg border border-gray-600"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3 flex-1">
                <span className="text-2xl">{task.task_type_detail.emoji}</span>
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h3 className="font-medium text-text-primary">
                      {task.task_type_detail.name}
                    </h3>
                    {task.interrupted && (
                      <span className="text-xs bg-warning text-white px-2 py-0.5 rounded">
                        Interrupted
                      </span>
                    )}
                    {task.edited_by_user && (
                      <span className="text-xs bg-gray-600 text-white px-2 py-0.5 rounded">
                        Edited
                      </span>
                    )}
                  </div>
                  
                  <div className="text-sm text-text-secondary mt-1 space-y-1">
                    <div>
                      {new Date(task.start_time).toLocaleString()} →{' '}
                      {task.end_time
                        ? new Date(task.end_time).toLocaleString()
                        : 'Ongoing'}
                    </div>
                    {task.end_time && (
                      <div className="font-medium text-accent">
                        Duration: {formatDurationSeconds(task.duration)}
                      </div>
                    )}
                    {task.notes && (
                      <div className="italic text-xs">Note: {task.notes}</div>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-2 ml-4">
                <button
                  onClick={() => handleEdit(task)}
                  className="text-sm px-3 py-1 bg-gray-600 text-white rounded hover:bg-opacity-90"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(task)}
                  className="text-sm px-3 py-1 bg-error text-white rounded hover:bg-opacity-90"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Edit Modal */}
      {editingTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-bg-secondary rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-bold text-text-primary mb-4">Edit Task</h3>
            
            <form
              onSubmit={(e) => {
                e.preventDefault()
                const formData = new FormData(e.currentTarget)
                updateMutation.mutate({
                  id: editingTask.id,
                  data: {
                    start_time: formData.get('start_time') as string,
                    end_time: formData.get('end_time') as string,
                    notes: formData.get('notes') as string,
                  } as Partial<Task>,
                })
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-sm text-text-secondary mb-1">
                  Start Time
                </label>
                <input
                  type="datetime-local"
                  name="start_time"
                  defaultValue={new Date(editingTask.start_time)
                    .toISOString()
                    .slice(0, 16)}
                  className="w-full px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
                />
              </div>

              <div>
                <label className="block text-sm text-text-secondary mb-1">
                  End Time
                </label>
                <input
                  type="datetime-local"
                  name="end_time"
                  defaultValue={
                    editingTask.end_time
                      ? new Date(editingTask.end_time).toISOString().slice(0, 16)
                      : ''
                  }
                  className="w-full px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
                />
              </div>

              <div>
                <label className="block text-sm text-text-secondary mb-1">Notes</label>
                <textarea
                  name="notes"
                  defaultValue={editingTask.notes}
                  rows={3}
                  className="w-full px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
                />
              </div>

              <div className="flex space-x-2">
                <button
                  type="submit"
                  disabled={updateMutation.isPending}
                  className="flex-1 px-4 py-2 bg-success text-white rounded hover:bg-opacity-90 disabled:opacity-50"
                >
                  {updateMutation.isPending ? 'Saving...' : 'Save'}
                </button>
                <button
                  type="button"
                  onClick={() => setEditingTask(null)}
                  className="flex-1 px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

