import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import apiClient from '../api/axios'

interface APIKey {
  id: number
  name: string
  key_prefix: string
  created_at: string
  last_used: string | null
  is_active: boolean
}

export default function APIKeySettings() {
  const queryClient = useQueryClient()
  const [newKeyName, setNewKeyName] = useState('')
  const [generatedKey, setGeneratedKey] = useState<string | null>(null)
  const [showKey, setShowKey] = useState(false)

  const { data: apiKeys = [] } = useQuery({
    queryKey: ['apiKeys'],
    queryFn: async () => {
      const response = await apiClient.get('/api-keys/')
      return response.data.results || response.data
    },
  })

  const createMutation = useMutation({
    mutationFn: async (name: string) => {
      const response = await apiClient.post('/api-keys/', { name })
      return response.data
    },
    onSuccess: (data) => {
      setGeneratedKey(data.api_key)
      setShowKey(true)
      setNewKeyName('')
      queryClient.invalidateQueries({ queryKey: ['apiKeys'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/api-keys/${id}/`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['apiKeys'] })
    },
  })

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    if (newKeyName.trim()) {
      createMutation.mutate(newKeyName)
    }
  }

  const copyToClipboard = () => {
    if (generatedKey) {
      navigator.clipboard.writeText(generatedKey)
      alert('API key copied to clipboard!')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-text-primary mb-4">API Keys</h3>
        <p className="text-text-secondary text-sm mb-4">
          Generate API keys for automation and third-party integrations.
        </p>

        {/* Generated Key Display */}
        {showKey && generatedKey && (
          <div className="mb-6 p-4 bg-success bg-opacity-20 border border-success rounded">
            <div className="font-bold text-success mb-2">⚠️ API Key Generated!</div>
            <div className="text-sm text-text-secondary mb-3">
              This key will only be shown once. Save it now!
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={generatedKey}
                readOnly
                className="flex-1 px-3 py-2 bg-bg-primary border border-success rounded text-text-primary font-mono text-sm"
              />
              <button
                onClick={copyToClipboard}
                className="px-4 py-2 bg-success text-white rounded hover:bg-opacity-90"
              >
                Copy
              </button>
            </div>
            <button
              onClick={() => setShowKey(false)}
              className="mt-3 text-sm text-text-secondary hover:text-text-primary"
            >
              I've saved it, close this
            </button>
          </div>
        )}

        {/* Create New Key */}
        <form onSubmit={handleCreate} className="mb-6">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              placeholder="Key name (e.g., 'iOS Shortcuts', 'Home Automation')"
              className="flex-1 px-3 py-2 bg-bg-primary border border-gray-600 rounded text-text-primary"
            />
            <button
              type="submit"
              disabled={createMutation.isPending || !newKeyName.trim()}
              className="px-4 py-2 bg-accent text-white rounded hover:bg-opacity-90 disabled:opacity-50"
            >
              {createMutation.isPending ? 'Generating...' : 'Generate Key'}
            </button>
          </div>
        </form>

        {/* Existing Keys */}
        <div className="space-y-2">
          {apiKeys.length === 0 ? (
            <div className="text-center py-8 text-text-secondary">
              No API keys yet. Generate one to get started!
            </div>
          ) : (
            apiKeys.map((key: APIKey) => (
              <div
                key={key.id}
                className="flex items-center justify-between p-4 bg-bg-tertiary rounded"
              >
                <div>
                  <div className="font-medium text-text-primary">{key.name}</div>
                  <div className="text-sm text-text-secondary font-mono">
                    {key.key_prefix}...
                  </div>
                  <div className="text-xs text-text-secondary mt-1">
                    Created: {new Date(key.created_at).toLocaleDateString()}
                    {key.last_used && ` • Last used: ${new Date(key.last_used).toLocaleDateString()}`}
                  </div>
                </div>
                <button
                  onClick={() => {
                    if (confirm(`Revoke API key "${key.name}"?`)) {
                      deleteMutation.mutate(key.id)
                    }
                  }}
                  className="px-3 py-1 bg-error text-white rounded hover:bg-opacity-90 text-sm"
                >
                  Revoke
                </button>
              </div>
            ))
          )}
        </div>

        {/* API Documentation Link */}
        <div className="mt-6 p-4 bg-bg-tertiary rounded">
          <h4 className="font-medium text-text-primary mb-2">Using API Keys</h4>
          <p className="text-sm text-text-secondary mb-3">
            Include your API key in the Authorization header:
          </p>
          <code className="block bg-bg-primary p-3 rounded text-xs text-text-primary font-mono overflow-x-auto">
            curl -H "Authorization: Api-Key your_key_here" http://localhost:8000/api/tasks/current/
          </code>
          <a
            href="http://localhost:8000/api/docs/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-3 text-accent hover:text-opacity-80 text-sm"
          >
            View Full API Documentation →
          </a>
        </div>
      </div>
    </div>
  )
}

