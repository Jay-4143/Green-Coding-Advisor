import React from 'react'
import { Routes, Route, NavLink, useNavigate, Link, useLocation } from 'react-router-dom'
import { api, setTokens, clearTokens } from './api/client'
import Dashboard from './components/Dashboard'
import CodeSubmission from './components/CodeSubmission'
import Leaderboard from './components/Leaderboard'
import Badges from './components/Badges'
import Teams from './components/Teams'
import Chatbot from './components/Chatbot'
import Settings from './components/Settings'
import Profile from './components/Profile'
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
  const [showLoginModal, setShowLoginModal] = React.useState(false)
  const [showMobileMenu, setShowMobileMenu] = React.useState(false)
  const [showUserMenu, setShowUserMenu] = React.useState(false)

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
        await api.get('/auth/me')
      } catch {
        clearTokens()
        if (!cancelled) {
          setAuthed(false)
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

  function handleLoginSuccess() {
    setAuthed(true)
    setShowLoginModal(false)
    if (location.pathname === '/' || location.pathname === '/login' || location.pathname === '/signup') {
      navigate('/dashboard')
    }
  }

  // Don't show navbar on login/signup pages (they use modal now)
  const showNavbar = !['/login', '/signup'].includes(location.pathname)

  if (!showNavbar) {
    return <>{children}</>
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-gray-900 text-slate-900 dark:text-gray-100">
      {/* Modern Navbar */}
      <header className="sticky top-0 z-40 bg-white dark:bg-gray-800 shadow-md border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">G</span>
              </div>
          <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">Green Coding Advisor</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400 hidden sm:block">Sustainable Coding Platform</p>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-1">
              <NavLink to="/" className={navLinkClass}>Home</NavLink>
              <NavLink to="/about" className={navLinkClass}>About</NavLink>
              <NavLink to="/services" className={navLinkClass}>Services</NavLink>
              <NavLink to="/contact" className={navLinkClass}>Contact</NavLink>
              
              {/* Profile + Menu (Desktop) */}
              {authed ? (
                <div className="flex items-center space-x-2 ml-4 relative">
                  <Link
                    to="/profile"
                    className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Profile"
                  >
                    <svg className="w-6 h-6 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </Link>
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Menu"
                  >
                    <svg className="w-6 h-6 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
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
                      <hr className="my-1 border-gray-200 dark:border-gray-700" />
                      <button
                        onClick={onLogout}
                        className="block w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
                      >
                        Logout
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className="ml-4 px-6 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg font-semibold hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl"
                >
                  Login
                </button>
              )}
            </nav>

            {/* Mobile Menu Button */}
            <div className="md:hidden flex items-center space-x-2">
              {authed ? (
                <>
                  <Link
                    to="/profile"
                    className="p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    title="Profile"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </Link>
                  <button
                    onClick={() => setShowMobileMenu(!showMobileMenu)}
                    className="p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg font-semibold text-sm"
                >
                  Login
              </button>
            )}
            </div>
          </div>

          {/* Mobile Menu */}
          {showMobileMenu && authed && (
            <div className="md:hidden py-4 border-t border-gray-200 dark:border-gray-700">
              <nav className="flex flex-col space-y-1">
                <Link to="/dashboard" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Dashboard</Link>
                <Link to="/submit" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Submit Code</Link>
                <Link to="/analysis" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Analysis</Link>
                <Link to="/leaderboard" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Leaderboard</Link>
                <Link to="/badges" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Badges</Link>
                <Link to="/teams" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Teams</Link>
                <Link to="/chatbot" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Chatbot</Link>
                <Link to="/settings" className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Settings</Link>
                <button
                  onClick={onLogout}
                  className="px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md text-left"
                >
                  Logout
                </button>
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

        {Array.isArray(data.suggestions) && data.suggestions.length > 0 && (
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
                alert('PDF report download requires a saved submission. Use the submissions page to download reports.')
              } catch (error) {
                console.error('Error:', error)
              }
            }}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
          >
            Download PDF Report
          </button>
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
        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}
