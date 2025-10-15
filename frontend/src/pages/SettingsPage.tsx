import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { taskTypesAPI, TaskType, TaskTypeCreate } from '../api/taskTypes'
import { useAuthStore } from '../store/authStore'

export default function SettingsPage() {
  const queryClient = useQueryClient()
  const { logout } = useAuthStore()
  
  const [showArchived, setShowArchived] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState<TaskTypeCreate>({
    name: '',
    emoji: '📊',
    color: '#3A8E61',
    is_pinned: false,
  })

  // Fetch task types
  const { data: taskTypes = [], isLoading } = useQuery({
    queryKey: ['taskTypes', showArchived],
    queryFn: () => taskTypesAPI.list(showArchived),
  })

  // Create mutation
  const createMutation = useMutation({
    mutationFn: taskTypesAPI.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['taskTypes'] })
      setIsCreating(false)
      resetForm()
    },
  })

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<TaskTypeCreate> }) =>
      taskTypesAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['taskTypes'] })
      setEditingId(null)
      resetForm()
    },
  })

  // Archive mutation
  const archiveMutation = useMutation({
    mutationFn: taskTypesAPI.archive,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['taskTypes'] })
    },
  })

  // Toggle pin mutation
  const togglePinMutation = useMutation({
    mutationFn: taskTypesAPI.togglePin,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['taskTypes'] })
    },
  })

  // Unarchive mutation
  const unarchiveMutation = useMutation({
    mutationFn: taskTypesAPI.unarchive,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['taskTypes'] })
    },
  })

  const resetForm = () => {
    setFormData({
      name: '',
      emoji: '📊',
      color: '#3A8E61',
      is_pinned: false,
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (editingId) {
      updateMutation.mutate({ id: editingId, data: formData })
    } else {
      createMutation.mutate(formData)
    }
  }

  const startEdit = (taskType: TaskType) => {
    setEditingId(taskType.id)
    setFormData({
      name: taskType.name,
      emoji: taskType.emoji,
      color: taskType.color,
      is_pinned: taskType.is_pinned,
    })
    setIsCreating(true)
  }

  const cancelEdit = () => {
    setIsCreating(false)
    setEditingId(null)
    resetForm()
  }

  const handleLogout = async () => {
    await logout()
    window.location.href = '/login'
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-accent text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-accent">Settings</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-error text-white rounded hover:bg-opacity-90"
          >
            Logout
          </button>
        </div>

        {/* Task Types Section */}
        <div className="bg-bg-secondary rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-text-primary">Task Types</h2>
            <button
              onClick={() => setIsCreating(true)}
              className="px-4 py-2 bg-accent text-white rounded hover:bg-opacity-90"
            >
              + New Task Type
            </button>
          </div>

          {/* Create/Edit Form */}
          {isCreating && (
            <div className="mb-6 p-4 bg-bg-tertiary rounded-lg">
              <h3 className="text-lg font-bold text-text-primary mb-4">
                {editingId ? 'Edit Task Type' : 'Create New Task Type'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-2">
                      Name
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-600 bg-bg-primary text-text-primary rounded focus:outline-none focus:ring-2 focus:ring-accent"
                      placeholder="Task name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-2">
                      Emoji
                    </label>
                    <input
                      type="text"
                      value={formData.emoji}
                      onChange={(e) => setFormData({ ...formData, emoji: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-600 bg-bg-primary text-text-primary rounded focus:outline-none focus:ring-2 focus:ring-accent"
                      placeholder="📊"
                      maxLength={10}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-2">
                      Color
                    </label>
                    <input
                      type="color"
                      value={formData.color}
                      onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                      className="w-full h-10 border border-gray-600 bg-bg-primary rounded cursor-pointer"
                    />
                  </div>

                  <div className="flex items-end">
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.is_pinned}
                        onChange={(e) =>
                          setFormData({ ...formData, is_pinned: e.target.checked })
                        }
                        className="w-4 h-4 text-accent bg-bg-primary border-gray-600 rounded focus:ring-accent"
                      />
                      <span className="text-text-secondary">Pin to quick grid</span>
                    </label>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <button
                    type="submit"
                    disabled={createMutation.isPending || updateMutation.isPending}
                    className="px-4 py-2 bg-success text-white rounded hover:bg-opacity-90 disabled:opacity-50"
                  >
                    {editingId ? 'Update' : 'Create'}
                  </button>
                  <button
                    type="button"
                    onClick={cancelEdit}
                    className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-opacity-90"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Show Archived Toggle */}
          <div className="mb-4">
            <label className="flex items-center space-x-2 text-text-secondary">
              <input
                type="checkbox"
                checked={showArchived}
                onChange={(e) => setShowArchived(e.target.checked)}
                className="w-4 h-4 text-accent bg-bg-primary border-gray-600 rounded focus:ring-accent"
              />
              <span>Show archived task types</span>
            </label>
          </div>

          {/* Task Types List */}
          <div className="space-y-2">
            {taskTypes.map((taskType) => (
              <div
                key={taskType.id}
                className={`p-4 rounded-lg border ${
                  taskType.is_archived ? 'bg-bg-tertiary border-gray-700' : 'bg-bg-primary border-gray-600'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <span className="text-2xl">{taskType.emoji}</span>
                    <div>
                      <h3 className={`font-medium ${taskType.is_archived ? 'text-text-secondary' : 'text-text-primary'}`}>
                        {taskType.name}
                        {taskType.is_pinned && (
                          <span className="ml-2 text-xs bg-accent text-white px-2 py-1 rounded">
                            Pinned
                          </span>
                        )}
                        {taskType.is_archived && (
                          <span className="ml-2 text-xs bg-gray-600 text-white px-2 py-1 rounded">
                            Archived
                          </span>
                        )}
                      </h3>
                      <div className="flex items-center space-x-2 mt-1">
                        <div
                          className="w-4 h-4 rounded"
                          style={{ backgroundColor: taskType.color }}
                        />
                        <span className="text-xs text-text-secondary">{taskType.color}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    {!taskType.is_archived ? (
                      <>
                        <button
                          onClick={() => togglePinMutation.mutate(taskType.id)}
                          className="px-3 py-1 text-sm bg-accent text-white rounded hover:bg-opacity-90"
                        >
                          {taskType.is_pinned ? 'Unpin' : 'Pin'}
                        </button>
                        <button
                          onClick={() => startEdit(taskType)}
                          className="px-3 py-1 text-sm bg-gray-600 text-white rounded hover:bg-opacity-90"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => {
                            if (confirm(`Archive "${taskType.name}"?`)) {
                              archiveMutation.mutate(taskType.id)
                            }
                          }}
                          className="px-3 py-1 text-sm bg-error text-white rounded hover:bg-opacity-90"
                        >
                          Archive
                        </button>
                      </>
                    ) : (
                      <button
                        onClick={() => {
                          if (confirm(`Unarchive "${taskType.name}"?`)) {
                            unarchiveMutation.mutate(taskType.id)
                          }
                        }}
                        className="px-3 py-1 text-sm bg-success text-white rounded hover:bg-opacity-90"
                      >
                        Unarchive
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

