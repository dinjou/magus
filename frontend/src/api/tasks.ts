import apiClient from './axios'
import { TaskType } from './taskTypes'

export interface Task {
  id: number
  task_type: number
  task_type_detail: TaskType
  start_time: string
  end_time: string | null
  duration: number
  interrupted: boolean
  is_manual_entry: boolean
  notes: string
  edited_by_user: boolean
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  task_type_id: number
  notes?: string
}

export const tasksAPI = {
  // List tasks
  list: async (params?: {
    start_date?: string
    end_date?: string
    task_type?: number
  }): Promise<Task[]> => {
    const response = await apiClient.get('/tasks/', { params })
    return response.data.results || response.data
  },

  // Get current task
  getCurrent: async (): Promise<Task | null> => {
    const response = await apiClient.get('/tasks/current/')
    return response.data
  },

  // Start tracking
  start: async (taskTypeId: number, notes?: string): Promise<Task> => {
    const response = await apiClient.post('/tasks/start/', {
      task_type_id: taskTypeId,
      notes: notes || '',
    })
    return response.data
  },

  // Stop tracking
  stop: async (): Promise<Task> => {
    const response = await apiClient.post('/tasks/stop/')
    return response.data
  },

  // Interrupt current and start new
  interrupt: async (taskTypeId: number, notes?: string): Promise<{
    interrupted_task: Task | null
    new_task: Task
    message: string
  }> => {
    const response = await apiClient.post('/tasks/interrupt/', {
      task_type_id: taskTypeId,
      notes: notes || '',
    })
    return response.data
  },

  // Get single task
  get: async (id: number): Promise<Task> => {
    const response = await apiClient.get(`/tasks/${id}/`)
    return response.data
  },

  // Update task
  update: async (id: number, data: Partial<Task>): Promise<Task> => {
    const response = await apiClient.patch(`/tasks/${id}/`, data)
    return response.data
  },

  // Delete task
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/tasks/${id}/`)
  },
}

