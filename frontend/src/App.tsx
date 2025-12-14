import React from 'react'
import { Routes, Route, NavLink, useNavigate, Link, useLocation } from 'react-router-dom'
import { api, setTokens, clearTokens } from './api/client'
import apiClient from './api/client'
import Dashboard from './components/Dashboard'
import CodeSubmission from './components/CodeSubmission'
import Leaderboard from './components/Leaderboard'
import Badges from './components/Badges'
import Teams from './components/Teams'
import Chatbot from './components/Chatbot'
import Settings from './components/Settings'
import Profile from './components/Profile'
import AdminDashboard from './components/AdminDashboard'
import VerifyEmail from './components/VerifyEmail'
import ResetPassword from './components/ResetPassword'
import ForgotPassword from './components/ForgotPassword'
import Home from './components/Home'
import About from './components/About'
import Services from './components/Services'
import Contact from './components/Contact'
import LoginModal from './components/LoginModal'
import { useTheme } from './contexts/ThemeContext'

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `px-4 py-2 rounded-md text-sm font-medium transition-colors ${
    isActive 
      ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 font-semibold' 
      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-emerald-600 dark:hover:text-emerald-400'
  }`

function Layout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  const location = useLocation()
  const { theme: _theme } = useTheme()
  const [authed, setAuthed] = React.useState<boolean>(Boolean(localStorage.getItem('access_token')))
  const [userRole, setUserRole] = React.useState<string | null>(null)
  const [showLoginModal, setShowLoginModal] = React.useState(false)
  const [showMobileMenu, setShowMobileMenu] = React.useState(false)
  const [showUserMenu, setShowUserMenu] = React.useState(false)
  const [scrollY, setScrollY] = React.useState(0)
  const [isScrolled, setIsScrolled] = React.useState(false)

  // Get background image based on current route
  const getNavbarBackground = () => {
    const backgrounds: Record<string, string> = {
      '/': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80',
      '/about': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80',
      '/services': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80',
      '/contact': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80',
    }
    return backgrounds[location.pathname] || backgrounds['/']
  }

  // Handle scroll to detect when past hero section
  React.useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY
      setScrollY(scrollPosition)
      // Change navbar to dark when scrolled past 100px (hero section)
      setIsScrolled(scrollPosition > 100)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  React.useEffect(() => {
    setAuthed(Boolean(localStorage.getItem('access_token')))
  }, [location])

  // Validate token once on mount; if invalid, clear and show login prompt
  React.useEffect(() => {
    let cancelled = false
    async function validateToken() {
      const token = localStorage.getItem('access_token')
      if (!token) {
        setAuthed(false)
        return
      }
      try {
        const response = await api.get('/auth/me')
        if (!cancelled && response.data) {
          setUserRole(response.data.role || null)
        }
      } catch {
        clearTokens()
        if (!cancelled) {
          setAuthed(false)
          setUserRole(null)
          setShowLoginModal(true)
        }
      }
    }
    validateToken()
    return () => {
      cancelled = true
    }
  }, [])

  function onLogout() {
    clearTokens()
    setAuthed(false)
    setShowUserMenu(false)
    navigate('/')
  }

  async function handleLoginSuccess() {
    setAuthed(true)
    setShowLoginModal(false)
    // Fetch user role after login
    try {
      const response = await api.get('/auth/me')
      if (response.data) {
        setUserRole(response.data.role || null)
      }
    } catch (error) {
      console.error('Failed to fetch user role:', error)
    }
    if (location.pathname === '/' || location.pathname === '/login' || location.pathname === '/signup') {
      navigate('/dashboard')
    }
  }

  // Don't show navbar on login/signup pages (they use modal now)
  const showNavbar = !['/login', '/signup'].includes(location.pathname)

  if (!showNavbar) {
    return <>{children}</>
  }

  const navbarBgImage = getNavbarBackground()
  const isPublicPage = ['/', '/about', '/services', '/contact'].includes(location.pathname)

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-gray-100">
      {/* Modern Navbar with Dynamic Background */}
      <header className={`sticky top-0 z-40 relative transition-all duration-300 ${
        isPublicPage && !isScrolled 
          ? '' 
          : 'bg-white dark:bg-slate-800 shadow-md'
      }`} style={isPublicPage && !isScrolled ? { 
        border: 'none', 
        borderBottom: 'none', 
        borderTop: 'none',
        boxShadow: 'none', 
        outline: 'none',
        marginBottom: 0,
        paddingBottom: 0
      } : {}}>
        {/* Transparent background with gradient overlay when at top of page */}
        {isPublicPage && !isScrolled && (
          <div 
            className="absolute inset-0 z-0"
            style={{
              backgroundImage: `url('${navbarBgImage}')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundAttachment: 'fixed'
            }}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-slate-900/90 via-slate-800/90 to-slate-900/90"></div>
          </div>
        )}
        
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 z-20">
              <img 
                src="/images/logo.png" 
                alt="Green Coding Advisor Logo" 
                className="h-10 w-auto"
                onError={(e) => {
                  // Fallback to gradient if image fails to load
                  const target = e.target as HTMLImageElement
                  target.style.display = 'none'
                  const fallback = target.nextElementSibling as HTMLElement
                  if (fallback) fallback.style.display = 'flex'
                }}
              />
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center hidden">
                <span className="text-white font-bold text-xl">G</span>
              </div>
              <div>
                <h1 className={`text-xl font-bold ${
                  isPublicPage && !isScrolled 
                    ? 'text-white drop-shadow-lg' 
                    : 'text-gray-900 dark:text-white'
                }`}>Green Coding Advisor</h1>
                <p className={`text-xs hidden sm:block ${
                  isPublicPage && !isScrolled 
                    ? 'text-emerald-100 drop-shadow-md' 
                    : 'text-gray-500 dark:text-gray-400'
                }`}>Sustainable Coding Platform</p>
              </div>
            </Link>

            {/* Desktop Navigation - Centered */}
            <nav className="hidden md:flex items-center space-x-1 absolute left-1/2 transform -translate-x-1/2">
              <NavLink 
                to="/" 
                className={({ isActive }) => 
                  `px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive 
                      ? (isPublicPage && !isScrolled)
                        ? 'bg-white/20 backdrop-blur-sm text-white font-semibold'
                        : 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 font-semibold'
                      : (isPublicPage && !isScrolled)
                        ? 'text-white/90 hover:bg-white/20 hover:text-white backdrop-blur-sm'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-emerald-600 dark:hover:text-emerald-400'
                  }`
                }
              >
                Home
              </NavLink>
              <NavLink 
                to="/about" 
                className={({ isActive }) => 
                  `px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive 
                      ? (isPublicPage && !isScrolled)
                        ? 'bg-white/20 backdrop-blur-sm text-white font-semibold'
                        : 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 font-semibold'
                      : (isPublicPage && !isScrolled)
                        ? 'text-white/90 hover:bg-white/20 hover:text-white backdrop-blur-sm'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-emerald-600 dark:hover:text-emerald-400'
                  }`
                }
              >
                About
              </NavLink>
              <NavLink 
                to="/services" 
                className={({ isActive }) => 
                  `px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive 
                      ? (isPublicPage && !isScrolled)
                        ? 'bg-white/20 backdrop-blur-sm text-white font-semibold'
                        : 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 font-semibold'
                      : (isPublicPage && !isScrolled)
                        ? 'text-white/90 hover:bg-white/20 hover:text-white backdrop-blur-sm'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-emerald-600 dark:hover:text-emerald-400'
                  }`
                }
              >
                Services
              </NavLink>
              <NavLink 
                to="/contact" 
                className={({ isActive }) => 
                  `px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive 
                      ? (isPublicPage && !isScrolled)
                        ? 'bg-white/20 backdrop-blur-sm text-white font-semibold'
                        : 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 font-semibold'
                      : (isPublicPage && !isScrolled)
                        ? 'text-white/90 hover:bg-white/20 hover:text-white backdrop-blur-sm'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-emerald-600 dark:hover:text-emerald-400'
                  }`
                }
              >
                Contact
              </NavLink>
            </nav>
              
            {/* Profile + Menu (Desktop) - Swapped positions */}
            {authed ? (
              <div className="flex items-center space-x-2 relative z-20">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className={`p-2 rounded-full transition-colors ${
                    (isPublicPage && !isScrolled)
                      ? 'hover:bg-white/20 text-white' 
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}
                  title="Menu"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
                <Link
                  to="/profile"
                  className={`p-2 rounded-full transition-colors ${
                    (isPublicPage && !isScrolled)
                      ? 'hover:bg-white/20 text-white' 
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}
                  title="Profile"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </Link>
                {showUserMenu && (
                  <div className="absolute right-0 top-12 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50">
                    <Link to="/dashboard" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Dashboard</Link>
                    <Link to="/submit" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Submit Code</Link>
                    <Link to="/analysis" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Analysis</Link>
                    <Link to="/leaderboard" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Leaderboard</Link>
                    <Link to="/badges" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Badges</Link>
                    <Link to="/teams" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Teams</Link>
                    <Link to="/chatbot" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Chatbot</Link>
                    <Link to="/settings" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Settings</Link>
                    {userRole === 'admin' && (
                      <>
                        <hr className="my-1 border-gray-200 dark:border-gray-700" />
                        <Link to="/admin" className="block px-4 py-2 text-sm text-emerald-600 dark:text-emerald-400 font-semibold hover:bg-emerald-50 dark:hover:bg-emerald-900/20">Admin Dashboard</Link>
                      </>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={() => setShowLoginModal(true)}
                className={`z-20 px-6 py-2 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl ${
                  (isPublicPage && !isScrolled)
                    ? 'bg-white/20 backdrop-blur-md text-white hover:bg-white/30 border-2 border-white/30'
                    : 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700'
                }`}
              >
                Login
              </button>
            )}

            {/* Mobile Menu Button - Swapped positions */}
            <div className="md:hidden flex items-center space-x-2 z-20">
              {authed ? (
                <>
                  <button
                    onClick={() => setShowMobileMenu(!showMobileMenu)}
                    className={`p-2 rounded-md transition-colors ${
                      (isPublicPage && !isScrolled)
                        ? 'hover:bg-white/20 text-white' 
                        : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }`}
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                  <Link
                    to="/profile"
                    className={`p-2 rounded-md transition-colors ${
                      (isPublicPage && !isScrolled)
                        ? 'hover:bg-white/20 text-white' 
                        : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }`}
                    title="Profile"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </Link>
                </>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
                    (isPublicPage && !isScrolled)
                      ? 'bg-white/20 backdrop-blur-md text-white hover:bg-white/30 border-2 border-white/30'
                      : 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white'
                  }`}
                >
                  Login
                </button>
              )}
            </div>
          </div>

          {/* Mobile Menu */}
          {showMobileMenu && authed && (
            <div className={`md:hidden py-4 border-t ${
              (isPublicPage && !isScrolled)
                ? 'border-white/20' 
                : 'border-gray-200 dark:border-gray-700'
            }`}>
              <nav className="flex flex-col space-y-1">
                <Link to="/dashboard" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Dashboard</Link>
                <Link to="/submit" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Submit Code</Link>
                <Link to="/analysis" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Analysis</Link>
                <Link to="/leaderboard" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Leaderboard</Link>
                <Link to="/badges" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Badges</Link>
                <Link to="/teams" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Teams</Link>
                <Link to="/chatbot" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Chatbot</Link>
                <Link to="/settings" className={`px-4 py-2 text-sm rounded-md ${
                  (isPublicPage && !isScrolled)
                    ? 'text-white/90 hover:bg-white/20'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}>Settings</Link>
                {userRole === 'admin' && (
                  <Link to="/admin" className={`px-4 py-2 text-sm font-semibold rounded-md ${
                    (isPublicPage && !isScrolled)
                      ? 'text-emerald-200 hover:bg-white/20'
                      : 'text-emerald-600 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20'
                  }`}>Admin Dashboard</Link>
                )}
              </nav>
            </div>
          )}
        </div>
      </header>

      <main>
          {children}
      </main>

      {/* Login Modal */}
      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onSuccess={handleLoginSuccess}
      />

      {/* Click outside to close user menu */}
      {showUserMenu && (
        <div
          className="fixed inset-0 z-30"
          onClick={() => setShowUserMenu(false)}
        />
      )}
    </div>
  )
}

function Page({ title, children }: { title: string; children?: React.ReactNode }) {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">{title}</h2>
      {children}
      </div>
    </div>
  )
}

function Analysis() {
  const [data, setData] = React.useState<any | null>(null)
  React.useEffect(() => {
    try {
      const raw = localStorage.getItem('last_analysis')
      if (raw) setData(JSON.parse(raw))
    } catch {}
  }, [])

  if (!data) {
    return (
      <Page title="Analysis Results">
        <p>No recent analysis found. Submit code to view results.</p>
      </Page>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-500'
    if (score >= 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <Page title="Analysis Results">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-slate-600">File</p>
            <p className="font-medium">{data.filename}</p>
          </div>
          <div>
            <p className="text-sm text-slate-600">Language</p>
            <p className="font-medium capitalize">{data.language}</p>
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-lg font-semibold text-gray-900">Green Score</h4>
            <span className="px-3 py-1 rounded-full text-sm font-medium bg-emerald-100 text-emerald-800">
              {data.greenScore}/100
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div className={`h-3 rounded-full ${getScoreColor(data.greenScore)}`} style={{ width: `${data.greenScore}%` }}></div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-blue-50 rounded-lg p-3">
            <p className="text-sm text-blue-600">Energy</p>
            <p className="text-lg font-semibold text-blue-900">{Number(data.energyConsumption).toFixed(2)} Wh</p>
          </div>
          <div className="bg-green-50 rounded-lg p-3">
            <p className="text-sm text-green-600">CO₂</p>
            <p className="text-lg font-semibold text-green-900">{Number(data.co2Emissions).toFixed(3)} g</p>
          </div>
          <div className="bg-purple-50 rounded-lg p-3">
            <p className="text-sm text-purple-600">Memory</p>
            <p className="text-lg font-semibold text-purple-900">{Number(data.memoryUsage).toFixed(1)} MB</p>
          </div>
          <div className="bg-orange-50 rounded-lg p-3">
            <p className="text-sm text-orange-600">CPU Time</p>
            <p className="text-lg font-semibold text-orange-900">{Number(data.cpuTime).toFixed(1)} ms</p>
          </div>
        </div>

        {/* Real-World Impact */}
        {(data.realWorldImpact || data.real_world_impact || data.analysis_details?.real_world_impact) && (() => {
          const impact = data.realWorldImpact || data.real_world_impact || data.analysis_details?.real_world_impact || {}
          return (
            <div className="mb-4">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Real-World Impact</h4>
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
                <p className="text-sm text-gray-700 mb-3 font-medium">
                  {impact.description || `Running this code 1M times would:`}
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {impact.light_bulb_hours && (
                    <div className="bg-white rounded-lg p-3 border border-green-200">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">💡</span>
                        <div>
                          <p className="text-xs text-gray-500">Light Bulb Hours</p>
                          <p className="text-lg font-bold text-green-700">
                            {Number(impact.light_bulb_hours).toFixed(1)} hrs
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                  {impact.tree_planting_days && (
                    <div className="bg-white rounded-lg p-3 border border-green-200">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🌳</span>
                        <div>
                          <p className="text-xs text-gray-500">Tree Planting Days</p>
                          <p className="text-lg font-bold text-green-700">
                            {Number(impact.tree_planting_days).toFixed(1)} days
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                  {impact.car_miles && (
                    <div className="bg-white rounded-lg p-3 border border-green-200">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🚗</span>
                        <div>
                          <p className="text-xs text-gray-500">Car Miles</p>
                          <p className="text-lg font-bold text-green-700">
                            {Number(impact.car_miles).toFixed(4)} miles
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )
        })()}

        {/* Full Optimized Code Section */}
        {data.optimizedCode && data.originalCode ? (
          <div className="mt-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Full Code Optimization</h4>
            
            {/* Comparison Table */}
            {data.comparisonTable && (
              <div className="mb-6 overflow-x-auto">
                <h5 className="text-md font-semibold text-gray-900 mb-3">Performance Comparison</h5>
                <table className="min-w-full bg-white border border-gray-200 rounded-lg">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">Metric</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-red-700 uppercase">Original</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-green-700 uppercase">Optimized</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase">Improvement</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {data.comparisonTable.green_score && (
                      <tr>
                        <td className="px-4 py-3 text-sm font-medium">Green Score</td>
                        <td className="px-4 py-3 text-sm text-red-600">{data.comparisonTable.green_score.original}</td>
                        <td className="px-4 py-3 text-sm text-green-600 font-semibold">{data.comparisonTable.green_score.optimized}</td>
                        <td className="px-4 py-3 text-sm text-blue-600 font-semibold">+{data.comparisonTable.green_score.improvement}</td>
                      </tr>
                    )}
                    {data.comparisonTable.energy_usage && (
                      <tr>
                        <td className="px-4 py-3 text-sm font-medium">Energy Usage</td>
                        <td className="px-4 py-3 text-sm text-red-600">{data.comparisonTable.energy_usage.original}</td>
                        <td className="px-4 py-3 text-sm text-green-600 font-semibold">{data.comparisonTable.energy_usage.optimized}</td>
                        <td className="px-4 py-3 text-sm text-blue-600">{data.comparisonTable.energy_usage.improvement}</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {/* Code Comparison */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
              <div>
                <h5 className="font-semibold text-red-700 mb-2">Original Code</h5>
                <pre className="bg-red-50 border-2 border-red-200 rounded-lg p-4 text-sm overflow-x-auto max-h-96">
                  <code className="text-red-900 font-mono whitespace-pre-wrap">{data.originalCode}</code>
                </pre>
              </div>
              <div>
                <h5 className="font-semibold text-green-700 mb-2">Optimized Code</h5>
                <pre className="bg-green-50 border-2 border-green-200 rounded-lg p-4 text-sm overflow-x-auto max-h-96">
                  <code className="text-green-900 font-mono whitespace-pre-wrap">{data.optimizedCode}</code>
                </pre>
              </div>
            </div>

            {data.expectedGreenScoreImprovement && (
              <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg">
                <p className="text-sm font-semibold text-green-900">
                  🎯 {data.expectedGreenScoreImprovement}
                </p>
              </div>
            )}
          </div>
        ) : Array.isArray(data.suggestions) && data.suggestions.length > 0 && (
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-2">Optimization Suggestions</h4>
            <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
              {data.suggestions.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-6 flex space-x-4">
          <button
            onClick={async () => {
              try {
                // Use originalCode if available, otherwise try to get code from submission ID
                let codeToUse = data.originalCode
                let languageToUse = data.language || data.detectedLanguage || 'python'
                
                // If no original code but we have a submission ID, try to fetch from submission
                if (!codeToUse && data.id) {
                  try {
                    const submissionRes = await apiClient.get(`/submissions/${data.id}`)
                    codeToUse = submissionRes.data?.code_content
                    languageToUse = submissionRes.data?.language || languageToUse
                  } catch (e) {
                    console.warn('Could not fetch submission:', e)
                  }
                }
                
                if (!codeToUse) {
                  alert('Code not available. Please submit code again to generate a report.')
                  return
                }
                
                // Generate comprehensive report using optimization endpoint
                const response = await apiClient.post(
                  `/submissions/optimize/report?format=pdf`,
                  {
                    code: codeToUse,
                    language: languageToUse,
                    region: 'usa'
                  },
                  {
                    responseType: 'blob'
                  }
                )
                
                // Download the PDF
                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', `green-coding-report-${data.filename || 'code'}-${new Date().toISOString().split('T')[0]}.pdf`)
                document.body.appendChild(link)
                link.click()
                link.remove()
                window.URL.revokeObjectURL(url)
              } catch (error: any) {
                console.error('Error downloading report:', error)
                alert(error?.response?.data?.detail || error?.message || 'Failed to download report. Please try again.')
              }
            }}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
          >
            Download PDF Report
          </button>
          <button
            onClick={async () => {
              try {
                // Use originalCode if available, otherwise try to get code from submission ID
                let codeToUse = data.originalCode
                let languageToUse = data.language || data.detectedLanguage || 'python'
                
                // If no original code but we have a submission ID, try to fetch from submission
                if (!codeToUse && data.id) {
                  try {
                    const submissionRes = await apiClient.get(`/submissions/${data.id}`)
                    codeToUse = submissionRes.data?.code_content
                    languageToUse = submissionRes.data?.language || languageToUse
                  } catch (e) {
                    console.warn('Could not fetch submission:', e)
                  }
                }
                
                if (!codeToUse) {
                  alert('Code not available. Please submit code again to generate a report.')
                  return
                }
                
                // Generate HTML report
                const response = await apiClient.post(
                  `/submissions/optimize/report?format=html`,
                  {
                    code: codeToUse,
                    language: languageToUse,
                    region: 'usa'
                  },
                  {
                    responseType: 'blob'
                  }
                )
                
                // Download the HTML
                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', `green-coding-report-${data.filename || 'code'}-${new Date().toISOString().split('T')[0]}.html`)
                document.body.appendChild(link)
                link.click()
                link.remove()
                window.URL.revokeObjectURL(url)
              } catch (error: any) {
                console.error('Error downloading report:', error)
                alert(error?.response?.data?.detail || error?.message || 'Failed to download report. Please try again.')
              }
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
          >
            Download HTML Report
          </button>
          {data.id && (
            <button
              onClick={async () => {
                try {
                  // Download report using submission ID (if available)
                  const response = await apiClient.get(
                    `/reports/submission/${data.id}/comprehensive?format=pdf`,
                    {
                      responseType: 'blob'
                    }
                  )
                  
                  // Download the PDF
                  const url = window.URL.createObjectURL(new Blob([response.data]))
                  const link = document.createElement('a')
                  link.href = url
                  link.setAttribute('download', `green-coding-report-${data.id}-${new Date().toISOString().split('T')[0]}.pdf`)
                  document.body.appendChild(link)
                  link.click()
                  link.remove()
                  window.URL.revokeObjectURL(url)
                } catch (error: any) {
                  console.error('Error downloading report:', error)
                  alert(error?.response?.data?.detail || error?.message || 'Failed to download report. Please try again.')
                }
              }}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 text-sm"
            >
              Download Saved Report
            </button>
          )}
        </div>
      </div>
    </Page>
  )
}

function NotFound() {
  return (
    <Page title="Not Found">
      <p>The page you're looking for doesn't exist.</p>
    </Page>
  )
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/services" element={<Services />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/submit" element={<CodeSubmission />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/badges" element={<Badges />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}
