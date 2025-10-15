import apiClient from './axios'

export interface TaskType {
  id: number
  name: string
  emoji: string
  color: string
  is_pinned: boolean
  is_archived: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface TaskTypeCreate {
  name: string
  emoji?: string
  color?: string
  is_pinned?: boolean
  sort_order?: number
}

export const taskTypesAPI = {
  // List task types
  list: async (showArchived: boolean = false): Promise<TaskType[]> => {
    const params = showArchived ? '?show_archived=true' : ''
    const response = await apiClient.get(`/task-types/${params}`)
    return response.data
  },

  // Get single task type
  get: async (id: number): Promise<TaskType> => {
    const response = await apiClient.get(`/task-types/${id}/`)
    return response.data
  },

  // Create task type
  create: async (data: TaskTypeCreate): Promise<TaskType> => {
    const response = await apiClient.post('/task-types/', data)
    return response.data
  },

  // Update task type
  update: async (id: number, data: Partial<TaskTypeCreate>): Promise<TaskType> => {
    const response = await apiClient.patch(`/task-types/${id}/`, data)
    return response.data
  },

  // Archive task type (soft delete)
  archive: async (id: number): Promise<void> => {
    await apiClient.delete(`/task-types/${id}/`)
  },

  // Un-archive task type
  unarchive: async (id: number): Promise<TaskType> => {
    const response = await apiClient.post(`/task-types/${id}/unarchive/`)
    return response.data
  },

  // Toggle pin status
  togglePin: async (id: number): Promise<TaskType> => {
    const response = await apiClient.post(`/task-types/${id}/toggle_pin/`)
    return response.data
  },

  // Reorder task types
  reorder: async (taskTypeIds: number[]): Promise<void> => {
    await apiClient.post('/task-types/reorder/', {
      task_type_ids: taskTypeIds,
    })
  },
}

