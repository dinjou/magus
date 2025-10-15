import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import apiClient from '../api/axios'

export default function ExportSettings() {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [emailTo, setEmailTo] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const exportMutation = useMutation({
    mutationFn: async (data: { start_date?: string; end_date?: string; email_to: string }) => {
      const response = await apiClient.post('/export/csv/', data)
      return response.data
    },
    onSuccess: (data) => {
      setSuccessMessage(data.message)
      setTimeout(() => setSuccessMessage(''), 5000)
    },
  })

  const handleDownload = () => {
    const params = new URLSearchParams()
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    const queryString = params.toString() ? `?${params.toString()}` : ''
    
    // Open download in new tab
    window.open(`http://localhost:8000/api/export/download/${queryString}`, '_blank')
  }

  const handleEmailExport = (e: React.FormEvent) => {
    e.preventDefault()
    exportMutation.mutate({
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      email_to: emailTo,
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-text-primary mb-4">Export Data</h3>

        {successMessage && (
          <div className="mb-4 p-3 bg-success bg-opacity-20 border border-success rounded text-success">
            {successMessage}
          </div>
        )}

        {/* Date Range Selection */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm text-text-secondary mb-2">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
            />
          </div>
          <div>
            <label className="block text-sm text-text-secondary mb-2">End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
            />
          </div>
        </div>

        <div className="text-xs text-text-secondary mb-4">
          Leave blank to export last 30 days
        </div>

        {/* Download CSV Button */}
        <button
          type="button"
          onClick={handleDownload}
          className="w-full mb-4 px-4 py-2 bg-accent text-white rounded hover:bg-opacity-90"
        >
          Download CSV Now
        </button>

        {/* Email Export Form */}
        <div className="border-t border-gray-600 pt-4">
          <h4 className="font-medium text-text-primary mb-3">Email Export</h4>
          <form onSubmit={handleEmailExport} className="space-y-3">
            <div>
              <label className="block text-sm text-text-secondary mb-2">Email Address</label>
              <input
                type="email"
                required
                value={emailTo}
                onChange={(e) => setEmailTo(e.target.value)}
                placeholder="your@email.com"
                className="w-full px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
              />
            </div>

            <button
              type="submit"
              disabled={exportMutation.isPending}
              className="w-full px-4 py-2 bg-success text-white rounded hover:bg-opacity-90 disabled:opacity-50"
            >
              {exportMutation.isPending ? 'Sending...' : 'Send CSV via Email'}
            </button>
          </form>
        </div>

        <div className="mt-4 p-3 bg-bg-tertiary rounded text-xs text-text-secondary">
          <strong>Note:</strong> Email exports use your configured SMTP settings. In development mode,
          emails are printed to the console instead of sent.
        </div>
      </div>
    </div>
  )
}

