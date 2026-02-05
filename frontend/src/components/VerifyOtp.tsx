import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

const VerifyOtp: React.FC = () => {
  const [email, setEmail] = useState('')
  const [otp, setOtp] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setMessage(null)

    try {
      const formData = new URLSearchParams()
      formData.append('email', email.trim().toLowerCase())
      formData.append('otp', otp.trim())
      await apiClient.post('/auth/verify-otp', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      setMessage('OTP verified successfully! You can now log in.')
      setTimeout(() => navigate('/login'), 2000)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'OTP verification failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-6">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl p-8 max-w-md w-full border border-gray-100 dark:border-slate-700">
        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Verify Account</h2>
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-6">
          Enter the 6-digit code sent to your email to verify your account.
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              OTP Code
            </label>
            <input
              type="text"
              maxLength={6}
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white tracking-widest text-center"
              required
            />
          </div>
          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-800 dark:text-red-300 text-sm">
              {error}
            </div>
          )}
          {message && (
            <div className="p-3 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-lg text-green-800 dark:text-green-300 text-sm">
              {message}
            </div>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Verify'}
          </button>
        </form>
        <p className="mt-4 text-sm text-gray-600 dark:text-gray-300 text-center">
          Didn’t get the code? Check your spam folder or request a new one by re-signing up.
        </p>
      </div>
    </div>
  )
}

export default VerifyOtp


