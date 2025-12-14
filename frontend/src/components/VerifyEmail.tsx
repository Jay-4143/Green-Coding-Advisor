import React, { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import apiClient from '../api/client'

const VerifyEmail: React.FC = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (token) {
      verifyEmail()
    } else {
      setError('No verification token provided')
    }
  }, [token])

  const verifyEmail = async () => {
    if (!token) return
    
    setLoading(true)
    setError(null)
    setMessage(null)

    try {
      const formData = new URLSearchParams()
      formData.append('token', token)
      await apiClient.post('/auth/verify-email', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      setMessage('Email verified successfully! You can now log in.')
      setTimeout(() => {
        navigate('/login')
      }, 3000)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Email verification failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-6">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl p-8 max-w-md w-full border border-gray-100 dark:border-slate-700">
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Verify Email</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">We’re confirming your account.</p>
        </div>
        {loading && (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
          </div>
        )}
        {message && (
          <div className="p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-lg text-green-800 dark:text-green-300">
            {message}
          </div>
        )}
        {error && (
          <div className="p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-800 dark:text-red-300">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default VerifyEmail

