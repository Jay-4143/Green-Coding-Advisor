import React from 'react'
import { Routes, Route, NavLink, useNavigate, Link } from 'react-router-dom'
import { api, setTokens, clearTokens } from './api/client'
import Dashboard from './components/Dashboard'
import CodeSubmission from './components/CodeSubmission'
import Leaderboard from './components/Leaderboard'

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-md text-sm font-medium ${isActive ? 'bg-emerald-100 text-emerald-700' : 'text-slate-700 hover:bg-slate-100'}`

function Layout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  const [authed, setAuthed] = React.useState<boolean>(Boolean(localStorage.getItem('access_token')))

  function onLogout() {
    clearTokens()
    setAuthed(false)
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="p-4 border-b bg-white">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">Green Coding Advisor</h1>
            <p className="text-sm text-slate-600">AI-enhanced web platform for sustainable coding</p>
          </div>
          <div className="flex items-center gap-2">
            <nav className="flex gap-2">
              <NavLink to="/dashboard" className={navLinkClass}>Dashboard</NavLink>
              <NavLink to="/submit" className={navLinkClass}>Submit</NavLink>
              <NavLink to="/analysis" className={navLinkClass}>Analysis</NavLink>
              <NavLink to="/leaderboard" className={navLinkClass}>Leaderboard</NavLink>
              <NavLink to="/teams" className={navLinkClass}>Teams</NavLink>
              <NavLink to="/chatbot" className={navLinkClass}>Chatbot</NavLink>
              <NavLink to="/settings" className={navLinkClass}>Settings</NavLink>
              {!authed && <NavLink to="/login" className={navLinkClass}>Login</NavLink>}
            </nav>
            {authed && (
              <button onClick={onLogout} className="px-3 py-2 rounded-md text-sm font-medium bg-red-100 text-red-700 hover:bg-red-200">
                Logout
              </button>
            )}
          </div>
        </div>
      </header>
      <main className="p-6">
        <div className="max-w-6xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  )
}

function Page({ title, children }: { title: string; children?: React.ReactNode }) {
  return (
    <div className="rounded-lg border bg-white p-4">
      <h2 className="text-lg font-medium mb-2">{title}</h2>
      {children}
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
      </div>
    </Page>
  )
}


function Teams() {
  return (
    <Page title="Teams">
      <p>Team dashboard and collaboration tools.</p>
    </Page>
  )
}

function Chatbot() {
  return (
    <Page title="AI Chatbot">
      <p>Ask questions about greener data structures and optimizations.</p>
    </Page>
  )
}

function Settings() {
  return (
    <Page title="Settings">
      <p>Manage your profile, preferences, and integrations.</p>
    </Page>
  )
}

function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = React.useState('jayvasani@gmail.com')
  const [password, setPassword] = React.useState('Jay@2543')
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = React.useState<{email?: string; password?: string}>({})

  function validate(): boolean {
    const errs: {email?: string; password?: string} = {}
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = 'Enter a valid email address'
    }
    const strongPass = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/
    if (!strongPass.test(password)) {
      errs.password = 'Min 8 chars, 1 uppercase, 1 number, 1 special'
    }
    setFieldErrors(errs)
    return Object.keys(errs).length === 0
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    if (!validate()) {
      setLoading(false)
      return
    }
    try {
      const res = await api.post('/auth/login', { email, password })
      setTokens(res.data.access_token, res.data.refresh_token)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Page title="Login">
      <form className="space-y-3" onSubmit={onSubmit} noValidate>
        <div>
          <label className="block text-sm mb-1">Email</label>
          <input
            className={`w-full border rounded px-3 py-2 ${fieldErrors.email ? 'border-red-500' : ''}`}
            type="email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
            required
          />
          {fieldErrors.email && <p className="text-xs text-red-600 mt-1">{fieldErrors.email}</p>}
        </div>
        <div>
          <label className="block text-sm mb-1">Password</label>
          <input
            className={`w-full border rounded px-3 py-2 ${fieldErrors.password ? 'border-red-500' : ''}`}
            type="password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            required
          />
          {fieldErrors.password && <p className="text-xs text-red-600 mt-1">{fieldErrors.password}</p>}
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button className="bg-emerald-600 text-white px-4 py-2 rounded disabled:opacity-50" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
        <p className="text-sm text-slate-600">
          Don’t have an account? <Link to="/signup" className="text-emerald-700 underline">Sign up</Link>
        </p>
      </form>
    </Page>
  )
}

function Signup() {
  const navigate = useNavigate()
  const [email, setEmail] = React.useState('jayvasani@gmail.com')
  const [username, setUsername] = React.useState('jayvasani')
  const [password, setPassword] = React.useState('Jay@2543')
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = React.useState<{email?: string; username?: string; password?: string}>({})

  function validate(): boolean {
    const errs: {email?: string; username?: string; password?: string} = {}
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = 'Enter a valid email address'
    }
    if (username.trim().length < 3) {
      errs.username = 'Username must be at least 3 characters'
    }
    const strongPass = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/
    if (!strongPass.test(password)) {
      errs.password = 'Min 8 chars, 1 uppercase, 1 number, 1 special'
    }
    setFieldErrors(errs)
    return Object.keys(errs).length === 0
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    if (!validate()) {
      setLoading(false)
      return
    }
    try {
      await api.post('/auth/signup', { email, username, password })
      // Auto-login
      const res = await api.post('/auth/login', { email, password })
      setTokens(res.data.access_token, res.data.refresh_token)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Page title="Sign up">
      <form className="space-y-3" onSubmit={onSubmit} noValidate>
        <div>
          <label className="block text-sm mb-1">Email</label>
          <input
            className={`w-full border rounded px-3 py-2 ${fieldErrors.email ? 'border-red-500' : ''}`}
            type="email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
            required
          />
          {fieldErrors.email && <p className="text-xs text-red-600 mt-1">{fieldErrors.email}</p>}
        </div>
        <div>
          <label className="block text-sm mb-1">Username</label>
          <input
            className={`w-full border rounded px-3 py-2 ${fieldErrors.username ? 'border-red-500' : ''}`}
            value={username}
            onChange={(e)=>setUsername(e.target.value)}
            required
          />
          {fieldErrors.username && <p className="text-xs text-red-600 mt-1">{fieldErrors.username}</p>}
        </div>
        <div>
          <label className="block text-sm mb-1">Password</label>
          <input
            className={`w-full border rounded px-3 py-2 ${fieldErrors.password ? 'border-red-500' : ''}`}
            type="password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            required
          />
          {fieldErrors.password && <p className="text-xs text-red-600 mt-1">{fieldErrors.password}</p>}
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button className="bg-emerald-600 text-white px-4 py-2 rounded disabled:opacity-50" disabled={loading}>
          {loading ? 'Creating account...' : 'Create account'}
        </button>
        <p className="text-sm text-slate-600">
          Already have an account? <Link to="/login" className="text-emerald-700 underline">Log in</Link>
        </p>
      </form>
    </Page>
  )
}

function NotFound() {
  return (
    <Page title="Not Found">
      <p>The page you’re looking for doesn’t exist.</p>
    </Page>
  )
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/submit" element={<CodeSubmission />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}


