import React, { useState } from 'react'
import { api, setTokens } from '../api/client'

interface LoginModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = useState<{email?: string; username?: string; password?: string}>({})

  if (!isOpen) return null

  function validate(): boolean {
    const errs: {email?: string; username?: string; password?: string} = {}
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = 'Enter a valid email address'
    }
    if (!isLogin && username.trim().length < 3) {
      errs.username = 'Username must be at least 3 characters'
    }
    const strongPass = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/
    if (!strongPass.test(password)) {
      errs.password = 'Min 8 chars, 1 uppercase, 1 number, 1 special'
    }
    setFieldErrors(errs)
    return Object.keys(errs).length === 0
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    if (!validate()) {
      setLoading(false)
      return
    }
    try {
      if (isLogin) {
        const res = await api.post('/auth/login', { email, password })
        setTokens(res.data.access_token, res.data.refresh_token)
        onSuccess()
        onClose()
        // Reset form
        setEmail('')
        setPassword('')
      } else {
        await api.post('/auth/signup', { email, username, password })
        // Auto-login
        const res = await api.post('/auth/login', { email, password })
        setTokens(res.data.access_token, res.data.refresh_token)
        onSuccess()
        onClose()
        // Reset form
        setEmail('')
        setUsername('')
        setPassword('')
      }
    } catch (err: any) {
      console.error(`${isLogin ? 'Login' : 'Signup'} error:`, err)
      console.error('Full error object:', {
        message: err?.message,
        code: err?.code,
        response: err?.response,
        request: err?.request,
        config: err?.config
      })
      
      // Better error handling
      let errorMessage = `${isLogin ? 'Login' : 'Signup'} failed`
      
      if (err?.response) {
        // Server responded with error
        errorMessage = err.response.data?.detail || err.response.data?.message || errorMessage
      } else if (err?.request) {
        // Request made but no response
        errorMessage = 'Network error: Could not connect to server. Please make sure the backend is running.'
      } else {
        // Something else
        errorMessage = err?.message || errorMessage
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose}>
      <div 
        className="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-6 text-white">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">{isLogin ? 'Login' : 'Sign Up'}</h2>
            <button
              onClick={onClose}
              className="text-white/80 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Form */}
        <form className="p-6 space-y-4" onSubmit={handleSubmit} noValidate>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              className={`w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                fieldErrors.email ? 'border-red-500' : 'border-gray-300'
              }`}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="your.email@example.com"
            />
            {fieldErrors.email && <p className="text-xs text-red-600 mt-1">{fieldErrors.email}</p>}
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                className={`w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                  fieldErrors.username ? 'border-red-500' : 'border-gray-300'
                }`}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                placeholder="Choose a username"
              />
              {fieldErrors.username && <p className="text-xs text-red-600 mt-1">{fieldErrors.username}</p>}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              className={`w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                fieldErrors.password ? 'border-red-500' : 'border-gray-300'
              }`}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
            {fieldErrors.password && <p className="text-xs text-red-600 mt-1">{fieldErrors.password}</p>}
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-3 rounded-lg font-semibold hover:from-emerald-700 hover:to-teal-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            disabled={loading}
          >
            {loading ? (isLogin ? 'Signing in...' : 'Creating account...') : (isLogin ? 'Sign In' : 'Create Account')}
          </button>

          <div className="text-center">
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin)
                setError(null)
                setFieldErrors({})
              }}
              className="text-emerald-600 hover:text-emerald-700 text-sm font-medium"
            >
              {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default LoginModal

