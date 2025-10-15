import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register, isLoading, error } = useAuthStore()
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
  })

  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setValidationErrors({})
    
    // Client-side validation
    const errors: Record<string, string> = {}
    
    if (formData.password !== formData.password2) {
      errors.password2 = "Passwords don't match"
    }
    
    if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters'
    }
    
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors)
      return
    }

    try {
      await register(formData)
      navigate('/dashboard')
    } catch (err) {
      if ((err as any).response?.data) {
        setValidationErrors((err as any).response.data)
      }
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
    // Clear validation error for this field
    if (validationErrors[e.target.name]) {
      setValidationErrors({
        ...validationErrors,
        [e.target.name]: '',
      })
    }
  }

  return (
    <div className="min-h-screen bg-bg-primary flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="text-center text-4xl font-bold text-accent">MAGUS</h1>
          <h2 className="mt-6 text-center text-3xl font-bold text-text-primary">
            Create your account
          </h2>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-error bg-opacity-20 border border-error text-text-primary px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-text-secondary mb-2">
                Username *
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-text-primary bg-bg-secondary rounded focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm"
                placeholder="Username"
              />
              {validationErrors.username && (
                <p className="mt-1 text-sm text-error">{validationErrors.username}</p>
              )}
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-text-secondary mb-2">
                Email *
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-text-primary bg-bg-secondary rounded focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm"
                placeholder="Email address"
              />
              {validationErrors.email && (
                <p className="mt-1 text-sm text-error">{validationErrors.email}</p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium text-text-secondary mb-2">
                  First name
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-text-primary bg-bg-secondary rounded focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm"
                  placeholder="First name"
                />
              </div>

              <div>
                <label htmlFor="last_name" className="block text-sm font-medium text-text-secondary mb-2">
                  Last name
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-text-primary bg-bg-secondary rounded focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm"
                  placeholder="Last name"
                />
              </div>
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-text-secondary mb-2">
                Password *
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-text-primary bg-bg-secondary rounded focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm"
                placeholder="Password (min 8 characters)"
              />
              {validationErrors.password && (
                <p className="mt-1 text-sm text-error">{validationErrors.password}</p>
              )}
            </div>

            <div>
              <label htmlFor="password2" className="block text-sm font-medium text-text-secondary mb-2">
                Confirm password *
              </label>
              <input
                id="password2"
                name="password2"
                type="password"
                required
                value={formData.password2}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-500 text-text-primary bg-bg-secondary rounded focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm"
                placeholder="Confirm password"
              />
              {validationErrors.password2 && (
                <p className="mt-1 text-sm text-error">{validationErrors.password2}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded text-white bg-accent hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Creating account...' : 'Sign up'}
            </button>
          </div>

          <div className="text-center">
            <Link to="/login" className="text-accent hover:text-opacity-80">
              Already have an account? Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}

