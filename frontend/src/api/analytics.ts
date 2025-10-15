import apiClient from './axios'

export interface TaskTypeSummary {
  task_type_id: number
  task_type_name: string
  task_type_emoji: string
  task_type_color: string
  total_duration: number
  duration_formatted: string
  percentage: number
  task_count?: number
  interrupted_count?: number
}

export interface TodaySummary {
  date: string
  total_tracked: number
  total_tracked_formatted: string
  task_types: TaskTypeSummary[]
}

export interface DailyData {
  date: string
  total_duration: number
  total_formatted: string
}

export interface WeeklyBreakdown {
  start_date: string
  end_date: string
  daily_data: DailyData[]
  task_types: TaskTypeSummary[]
  total_tracked: number
  total_tracked_formatted: string
}

export interface HeatmapDay {
  date: string
  hours: number
  level: number
}

export interface HeatmapData {
  start_date: string
  end_date: string
  heatmap: HeatmapDay[]
}

export const analyticsAPI = {
  // Get today's summary
  getTodaySummary: async (): Promise<TodaySummary> => {
    const response = await apiClient.get('/analytics/summary/')
    return response.data
  },

  // Get daily breakdown
  getDailyBreakdown: async (date?: string): Promise<TodaySummary> => {
    const params = date ? `?date=${date}` : ''
    const response = await apiClient.get(`/analytics/daily/${params}`)
    return response.data
  },

  // Get weekly breakdown
  getWeeklyBreakdown: async (startDate?: string, endDate?: string): Promise<WeeklyBreakdown> => {
    const params = new URLSearchParams()
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    const queryString = params.toString() ? `?${params.toString()}` : ''
    const response = await apiClient.get(`/analytics/weekly/${queryString}`)
    return response.data
  },

  // Get monthly breakdown
  getMonthlyBreakdown: async (startDate?: string, endDate?: string): Promise<TodaySummary> => {
    const params = new URLSearchParams()
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    const queryString = params.toString() ? `?${params.toString()}` : ''
    const response = await apiClient.get(`/analytics/monthly/${queryString}`)
    return response.data
  },

  // Get heatmap data
  getHeatmapData: async (startDate?: string, endDate?: string): Promise<HeatmapData> => {
    const params = new URLSearchParams()
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    const queryString = params.toString() ? `?${params.toString()}` : ''
    const response = await apiClient.get(`/analytics/heatmap/${queryString}`)
    return response.data
  },
}

