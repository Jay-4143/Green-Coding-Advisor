import React, { useState, useEffect } from 'react'
import apiClient from '../api/client'

interface LeaderboardEntry {
  rank: number
  username: string
  greenScore: number
  carbonSaved: number
  submissions: number
  badges: string[]
  avatar?: string
}

interface MyPerformance {
  rank: number | null
  greenScore: number
  carbonSaved: number
}

const Leaderboard: React.FC = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [timeframe, setTimeframe] = useState<'week' | 'month' | 'all'>('month')
  const [me, setMe] = useState<{ id: number | null; username: string | null }>({ id: null, username: null })
  const [myPerf, setMyPerf] = useState<MyPerformance>({ rank: null, greenScore: 0, carbonSaved: 0 })

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true)
        const [meRes, lbRes] = await Promise.all([
          apiClient.get('/auth/me').catch(() => ({ data: {} })),
          apiClient.get('/metrics/leaderboard', { params: { timeframe } }),
        ])
        const entries: LeaderboardEntry[] = lbRes.data?.entries || []
        setLeaderboard(entries)

        const uid = meRes.data?.id || null
        const username = meRes.data?.username || null
        setMe({ id: uid, username })

        if (uid) {
          try {
            const summaryRes = await apiClient.get(`/metrics/summary?user_id=${uid}`)
            const summary = summaryRes.data || {}
            const myEntry = entries.find((e) => e.username === username || e.rank === 1 && uid === uid) // best-effort match by username
            setMyPerf({
              rank: myEntry?.rank ?? null,
              greenScore: summary.average_green_score || 0,
              carbonSaved: summary.total_co2_saved || 0,
            })
          } catch (e) {
            setMyPerf((prev) => ({ ...prev, rank: null }))
          }
        } else {
          setMyPerf({ rank: null, greenScore: 0, carbonSaved: 0 })
        }
      } catch (error) {
        console.error('Error fetching leaderboard:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchLeaderboard()
  }, [timeframe])

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return (
          <div className="flex items-center justify-center w-8 h-8 bg-yellow-100 rounded-full">
            <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
        )
      case 2:
        return (
          <div className="flex items-center justify-center w-8 h-8 bg-gray-100 rounded-full">
            <svg className="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
        )
      case 3:
        return (
          <div className="flex items-center justify-center w-8 h-8 bg-orange-100 rounded-full">
            <svg className="w-5 h-5 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
        )
      default:
        return (
          <div className="flex items-center justify-center w-8 h-8 bg-gray-100 rounded-full">
            <span className="text-sm font-medium text-gray-600">{rank}</span>
          </div>
        )
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100'
    if (score >= 80) return 'text-blue-600 bg-blue-100'
    if (score >= 70) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Green Coding Leaderboard</h1>
        <p className="text-green-100">
          Compete with developers worldwide to create the most sustainable code
        </p>
      </div>

      {/* Timeframe Selector */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex space-x-4">
          <button
            onClick={() => setTimeframe('week')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              timeframe === 'week'
                ? 'bg-green-100 text-green-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            This Week
          </button>
          <button
            onClick={() => setTimeframe('month')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              timeframe === 'month'
                ? 'bg-green-100 text-green-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            This Month
          </button>
          <button
            onClick={() => setTimeframe('all')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              timeframe === 'all'
                ? 'bg-green-100 text-green-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            All Time
          </button>
        </div>
      </div>

      {/* Leaderboard */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Top Performers</h2>
        </div>
        
        <div className="divide-y divide-gray-200">
          {leaderboard.map((entry) => (
            <div key={entry.rank} className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  {getRankIcon(entry.rank)}
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <h3 className="text-lg font-medium text-gray-900">{entry.username}</h3>
                      {entry.badges.length > 0 && (
                        <div className="flex space-x-1">
                          {entry.badges.map((badge, index) => (
                            <span
                              key={index}
                              className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
                            >
                              {badge}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-4 mt-1">
                      <span className="text-sm text-gray-500">
                        {entry.submissions} submissions
                      </span>
                      <span className="text-sm text-gray-500">
                        {entry.carbonSaved} kg CO₂ saved
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(entry.greenScore)}`}>
                    {entry.greenScore}/100
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Green Score</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Your Position */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Performance</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <p className="text-2xl font-bold text-green-600">{myPerf.rank ? `#${myPerf.rank}` : '—'}</p>
            <p className="text-sm text-green-600">Current Rank</p>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <p className="text-2xl font-bold text-blue-600">{myPerf.greenScore.toFixed(1)}</p>
            <p className="text-sm text-blue-600">Avg Green Score</p>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <p className="text-2xl font-bold text-purple-600">{(myPerf.carbonSaved / 1000).toFixed(2)}</p>
            <p className="text-sm text-purple-600">kg CO₂ Saved</p>
          </div>
        </div>
      </div>

      {/* Achievement Progress */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Achievement Progress</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Carbon Saver</span>
              <span className="text-sm text-gray-500">2.4/5.0 kg CO₂</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-green-500 h-2 rounded-full" style={{ width: '48%' }}></div>
            </div>
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Eco-Friendly Champion</span>
              <span className="text-sm text-gray-500">24/50 submissions</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-500 h-2 rounded-full" style={{ width: '48%' }}></div>
            </div>
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Efficient Coder</span>
              <span className="text-sm text-gray-500">Achieved!</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Leaderboard
