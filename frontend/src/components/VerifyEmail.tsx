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
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">Verify Email</h2>
        {loading && (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
          </div>
        )}
        {message && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-green-800">
            {message}
          </div>
        )}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default VerifyEmail

