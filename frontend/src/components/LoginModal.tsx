import React, { useEffect, useState } from 'react'
import { api, setTokens } from '../api/client'

interface LoginModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [isOtpStep, setIsOtpStep] = useState(false)
  const [firstName, setFirstName] = useState('')
  const [middleName, setMiddleName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [otp, setOtp] = useState('')
  const [otpEmail, setOtpEmail] = useState('')
  const [otpTimer, setOtpTimer] = useState(60)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [info, setInfo] = useState<string | null>(null)
  const [showForgotPassword, setShowForgotPassword] = useState(false)
  const [forgotEmail, setForgotEmail] = useState('')
  const [forgotStatus, setForgotStatus] = useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = useState<{
    email?: string
    password?: string
    confirmPassword?: string
    firstName?: string
    lastName?: string
  }>({})

  // OTP countdown
  useEffect(() => {
    if (!isOtpStep) return
    if (otpTimer <= 0) return
    const id = setInterval(() => {
      setOtpTimer((t) => (t > 0 ? t - 1 : 0))
    }, 1000)
    return () => clearInterval(id)
  }, [isOtpStep, otpTimer])

  // Reset form state whenever the modal is opened
  useEffect(() => {
    if (isOpen) {
      setIsLogin(true)
      setIsOtpStep(false)
      setFirstName('')
      setMiddleName('')
      setLastName('')
      setEmail('')
      setPassword('')
      setConfirmPassword('')
      setOtp('')
      setOtpEmail('')
      setOtpTimer(60)
      setError(null)
      setInfo(null)
      setShowForgotPassword(false)
      setForgotEmail('')
      setForgotStatus(null)
      setFieldErrors({})
    }
  }, [isOpen])

  if (!isOpen) return null

  function validate(): boolean {
    // In OTP step we only validate OTP
    if (isOtpStep) {
      if (!otp.trim() || otp.trim().length !== 6) {
        setError('Please enter the 6-digit OTP code')
        return false
      }
      return true
    }

    const errs: {
      email?: string
      password?: string
      confirmPassword?: string
      firstName?: string
      lastName?: string
    } = {}

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = 'Enter a valid email address'
    }

    if (!isLogin) {
      // Signup validation
      if (!firstName.trim()) {
        errs.firstName = 'First name is required'
      }
      if (!lastName.trim()) {
        errs.lastName = 'Last name is required'
      }
      
      // Password complexity validation ONLY for signup
      const strongPass = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/
      if (!strongPass.test(password)) {
        errs.password = 'Min 8 chars, 1 uppercase, 1 number, 1 special'
      }
      if (password !== confirmPassword) {
        errs.confirmPassword = 'Passwords do not match'
      }
    } else {
      // Login validation - only check if password is not empty
      if (!password.trim()) {
        errs.password = 'Password is required'
      }
    }

    setFieldErrors(errs)
    return Object.keys(errs).length === 0
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setInfo(null)
    setForgotStatus(null)
    if (!validate()) {
      setLoading(false)
      return
    }
    try {
      // OTP verification step
      if (isOtpStep) {
        const formData = new URLSearchParams()
        formData.append('email', otpEmail || email)
        formData.append('otp', otp.trim())
        await api.post('/auth/verify-otp', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })

        // After successful OTP, auto-login
        const res = await api.post('/auth/login', { email: otpEmail || email, password })
        setTokens(res.data.access_token, res.data.refresh_token)
        onSuccess()
        onClose()
        // Reset state
        setIsOtpStep(false)
        setOtp('')
        setOtpEmail('')
        setOtpTimer(60)
        setFirstName('')
        setMiddleName('')
        setLastName('')
        setEmail('')
        setPassword('')
        setConfirmPassword('')
      } else if (isLogin) {
        const res = await api.post('/auth/login', { email, password })
        setTokens(res.data.access_token, res.data.refresh_token)
        onSuccess()
        onClose()
        // Reset form
        setEmail('')
        setPassword('')
      } else {
        // Derive a username from first & last name for backend
        const derivedUsername = `${firstName.trim()}${lastName.trim()}`.replace(/\s+/g, '').slice(0, 30) || 'user'

        await api.post('/auth/signup', {
          email,
          username: derivedUsername,
          password
        })

        // Move to OTP step inside the same modal
        setOtpEmail(email)
        setIsOtpStep(true)
        setOtp('')
        setOtpTimer(60)
        setInfo('We sent a 6-digit verification code to your email. Enter it below to complete signup.')
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
        const serverMessage = err.response.data?.detail || err.response.data?.message || errorMessage
        
        // For login, normalize password-related errors to "Invalid password"
        if (isLogin && (serverMessage.toLowerCase().includes('password') || 
                        serverMessage.toLowerCase().includes('incorrect') ||
                        err.response.status === 401)) {
          errorMessage = 'Invalid password'
        } else {
          errorMessage = serverMessage
        }
      } else if (err?.request) {
        // Request made but no response
        errorMessage = 'Network error: Could not connect to server. Please make sure the backend is running.'
      } else {
        // Something else
        errorMessage = err?.message || errorMessage
      }
      
      // Clear field errors when showing general error
      setFieldErrors({})
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose}>
      <div 
        className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-6 text-white">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">
              {isOtpStep ? 'Verify OTP' : isLogin ? 'Login' : 'Sign Up'}
            </h2>
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
        <form className="p-6 space-y-4 bg-white dark:bg-slate-800" onSubmit={handleSubmit} noValidate>
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}
          {info && (
            <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 px-4 py-3 rounded-lg text-sm">
              {info}
            </div>
          )}

          {/* OTP STEP */}
          {isOtpStep ? (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Email
                </label>
                <input
                  className="w-full border rounded-lg px-4 py-2 bg-gray-100 dark:bg-slate-900/60 text-gray-900 dark:text-white"
                  type="email"
                  value={otpEmail || email}
                  disabled
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  OTP Code
                </label>
                <input
                  className="w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-center tracking-widest text-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 border-gray-300 dark:border-gray-600"
                  type="text"
                  maxLength={6}
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  placeholder="••••••"
                  required
                />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Code expires in{' '}
                  <span className="font-semibold">
                    0:{otpTimer.toString().padStart(2, '0')}
                  </span>
                </p>
              </div>
            </>
          ) : (
            <>
              {/* SIGNUP / LOGIN FIELDS */}
              {!isLogin && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      First Name
                    </label>
                    <input
                      className={`w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                        fieldErrors.firstName ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                      }`}
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                      required
                      placeholder="First name"
                    />
                    {fieldErrors.firstName && (
                      <p className="text-xs text-red-600 dark:text-red-400 mt-1">{fieldErrors.firstName}</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Middle Name (optional)
                    </label>
                    <input
                      className="w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 border-gray-300 dark:border-gray-600"
                      value={middleName}
                      onChange={(e) => setMiddleName(e.target.value)}
                      placeholder="Middle name"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Last Name
                    </label>
                    <input
                      className={`w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                        fieldErrors.lastName ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                      }`}
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                      required
                      placeholder="Last name"
                    />
                    {fieldErrors.lastName && (
                      <p className="text-xs text-red-600 dark:text-red-400 mt-1">{fieldErrors.lastName}</p>
                    )}
                  </div>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
                <input
                  className={`w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                    fieldErrors.email ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                  }`}
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="your.email@example.com"
                />
                {fieldErrors.email && <p className="text-xs text-red-600 dark:text-red-400 mt-1">{fieldErrors.email}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
                <input
                  className={`w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                    fieldErrors.password ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                  }`}
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Enter your password"
                />
                {fieldErrors.password && (
                  <p className="text-xs text-red-600 dark:text-red-400 mt-1">{fieldErrors.password}</p>
                )}
                {/* Only show password complexity hint during signup */}
                {!isLogin && (
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Min 8 chars, 1 uppercase, 1 number, 1 special
                  </p>
                )}
              </div>

              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Confirm Password
                  </label>
                  <input
                    className={`w-full border rounded-lg px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                      fieldErrors.confirmPassword ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                    }`}
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    placeholder="Re-enter your password"
                  />
                  {fieldErrors.confirmPassword && (
                    <p className="text-xs text-red-600 dark:text-red-400 mt-1">{fieldErrors.confirmPassword}</p>
                  )}
                </div>
              )}
            </>
          )}

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-3 rounded-lg font-semibold hover:from-emerald-700 hover:to-teal-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            disabled={loading}
          >
            {loading
              ? isOtpStep
                ? 'Verifying...'
                : isLogin
                  ? 'Signing in...'
                  : 'Creating account...'
              : isOtpStep
                ? 'Verify OTP'
                : isLogin
                  ? 'Sign In'
                  : 'Create Account'}
          </button>

          {/* Forgot password link - always visible during login, above signup link */}
          {!isOtpStep && isLogin && !showForgotPassword && (
            <div className="text-center">
              <button
                type="button"
                onClick={() => {
                  setShowForgotPassword(true)
                  setForgotEmail(email)
                  setForgotStatus(null)
                  setError(null)
                  setFieldErrors({})
                }}
                className="text-sm text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 hover:underline font-medium"
              >
                Forgot password?
              </button>
            </div>
          )}

          {!isOtpStep && (
            <div className="text-center">
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin)
                  setError(null)
                  setInfo(null)
                  setFieldErrors({})
                  setShowForgotPassword(false)
                  setForgotStatus(null)
                }}
                className="text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 text-sm font-medium"
              >
                {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
              </button>
            </div>
          )}

          {/* Forgot Password Flow (inline) */}
          {!isOtpStep && isLogin && showForgotPassword && (
            <div className="mt-4 border-t border-gray-200 dark:border-slate-700 pt-4 space-y-3">
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  Forgot your password? Enter your email and we'll send you a reset link.
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setShowForgotPassword(false)
                    setForgotEmail('')
                    setForgotStatus(null)
                    setError(null)
                  }}
                  className="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                >
                  Back to login
                </button>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Email
                </label>
                <input
                  className="w-full border rounded-lg px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 border-gray-300 dark:border-gray-600"
                  type="email"
                  value={forgotEmail}
                  onChange={(e) => setForgotEmail(e.target.value)}
                  placeholder="your.email@example.com"
                />
              </div>
              <button
                type="button"
                onClick={async () => {
                  try {
                    setForgotStatus(null)
                    if (!forgotEmail.trim()) {
                      setForgotStatus('Please enter your email.')
                      return
                    }
                    const formData = new URLSearchParams()
                    formData.append('email', forgotEmail.trim().toLowerCase())
                    await api.post('/auth/forgot-password', formData, {
                      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                    })
                    setForgotStatus('If the email exists, a reset link has been sent.')
                  } catch (err: any) {
                    setForgotStatus(
                      err?.response?.data?.detail || 'Failed to send reset link. Please try again.'
                    )
                  }
                }}
                className="w-full bg-slate-100 dark:bg-slate-700 text-gray-900 dark:text-white px-4 py-2 rounded-md hover:bg-slate-200 dark:hover:bg-slate-600 text-sm font-medium"
              >
                Send Reset Link
              </button>
              {forgotStatus && (
                <p className="text-xs text-center text-gray-700 dark:text-gray-200">{forgotStatus}</p>
              )}
            </div>
          )}
        </form>
      </div>
    </div>
  )
}

export default LoginModal

