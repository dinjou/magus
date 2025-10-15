import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tasksAPI } from '../api/tasks'

export function useCurrentTask() {
  const queryClient = useQueryClient()

  // Get current task
  const { data: currentTask, isLoading } = useQuery({
    queryKey: ['currentTask'],
    queryFn: tasksAPI.getCurrent,
    refetchInterval: 5000, // Refresh every 5 seconds for live timer
  })

  // Start task
  const startMutation = useMutation({
    mutationFn: ({ taskTypeId, notes }: { taskTypeId: number; notes?: string }) =>
      tasksAPI.start(taskTypeId, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['currentTask'] })
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  // Stop task
  const stopMutation = useMutation({
    mutationFn: tasksAPI.stop,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['currentTask'] })
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  // Interrupt (stop current, start new)
  const interruptMutation = useMutation({
    mutationFn: ({ taskTypeId, notes }: { taskTypeId: number; notes?: string }) =>
      tasksAPI.interrupt(taskTypeId, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['currentTask'] })
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  return {
    currentTask,
    isLoading,
    startTask: startMutation.mutate,
    stopTask: stopMutation.mutate,
    interruptTask: interruptMutation.mutate,
    isStarting: startMutation.isPending,
    isStopping: stopMutation.isPending,
    isInterrupting: interruptMutation.isPending,
  }
}

