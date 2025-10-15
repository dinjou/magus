import { useAuthStore } from '../store/authStore'

export default function DashboardPage() {
  const { user, logout } = useAuthStore()

  const handleLogout = async () => {
    await logout()
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-accent">MAGUS</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-error text-white rounded hover:bg-opacity-90"
          >
            Logout
          </button>
        </div>

        <div className="bg-bg-secondary p-6 rounded-lg">
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            Welcome, {user?.username}!
          </h2>
          <p className="text-text-secondary mb-4">
            You're successfully logged in to MAGUS.
          </p>
          
          <div className="mt-6 p-4 bg-success bg-opacity-20 border border-success rounded">
            <p className="text-success font-medium">✓ Sprint 1 Complete!</p>
            <p className="text-text-secondary text-sm mt-2">
              Authentication system is working. Task tracking features coming in Sprint 2+.
            </p>
          </div>
          
          <div className="mt-6 space-y-2 text-sm text-text-secondary">
            <p><strong>User ID:</strong> {user?.id}</p>
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Joined:</strong> {new Date(user?.date_joined || '').toLocaleDateString()}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

