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
  submissions: number
}

const Leaderboard: React.FC = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [timeframe, setTimeframe] = useState<'week' | 'month' | 'all'>('all')
  const [me, setMe] = useState<{ id: number | null; username: string | null }>({ id: null, username: null })
  const [myPerf, setMyPerf] = useState<MyPerformance>({ rank: null, greenScore: 0, carbonSaved: 0, submissions: 0 })

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true)
        const [meRes, lbRes] = await Promise.all([
          apiClient.get('/auth/me').catch(() => ({ data: {} })),
          apiClient.get('/metrics/leaderboard', { params: { timeframe, limit: 50 } }),
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
            const myEntry = entries.find((e) => e.username === username)
            setMyPerf({
              rank: myEntry?.rank ?? null,
              greenScore: summary.average_green_score || 0,
              carbonSaved: summary.total_co2_saved || 0,
              submissions: summary.total_submissions || 0
            })
          } catch (e) {
            setMyPerf((prev) => ({ ...prev, rank: null }))
          }
        } else {
          setMyPerf({ rank: null, greenScore: 0, carbonSaved: 0, submissions: 0 })
        }
      } catch (error) {
        console.error('Error fetching leaderboard:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchLeaderboard()
  }, [timeframe])

  // Get initials for avatar
  const getInitials = (name: string) => {
    const parts = name.trim().split(' ')
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
    return name.slice(0, 2).toUpperCase()
  }

  const top3 = leaderboard.slice(0, 3)
  const rest = leaderboard.slice(3)
  // Podium order: 2nd, 1st, 3rd
  const podiumOrder = top3.length >= 3 ? [
    { ...top3[1], podiumRank: 2 },
    { ...top3[0], podiumRank: 1 },
    { ...top3[2], podiumRank: 3 },
  ] : top3.map(e => ({ ...e, podiumRank: e.rank }))

  // Medal config
  const getMedalInfo = (rank: number) => {
    switch(rank) {
      case 1: return { medal: '🥇', bg: 'from-yellow-100 to-amber-100 dark:from-yellow-900/30 dark:to-amber-900/30', border: 'border-yellow-400', avatarRing: 'ring-yellow-400', height: 'min-h-[260px]' }
      case 2: return { medal: '🥈', bg: 'from-gray-100 to-slate-100 dark:from-gray-800/50 dark:to-slate-800/50', border: 'border-slate-400', avatarRing: 'ring-slate-400', height: 'min-h-[220px]' }
      case 3: return { medal: '🥉', bg: 'from-orange-100 to-amber-100 dark:from-orange-900/20 dark:to-amber-900/20', border: 'border-orange-400', avatarRing: 'ring-orange-400', height: 'min-h-[200px]' }
      default: return { medal: '', bg: 'from-gray-100 to-gray-100 dark:from-gray-800 dark:to-gray-800', border: 'border-gray-300', avatarRing: 'ring-gray-400', height: 'min-h-[200px]' }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6 bg-slate-50 dark:bg-slate-900 min-h-screen p-4 sm:p-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Green Coding Leaderboard</h1>
        <p className="text-green-100">
          Compete with developers worldwide to create the most sustainable code
        </p>
      </div>

      {/* Timeframe Selector */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-4">
        <div className="flex space-x-4">
          <button
            onClick={() => setTimeframe('week')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${timeframe === 'week'
              ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
          >
            This Week
          </button>
          <button
            onClick={() => setTimeframe('month')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${timeframe === 'month'
              ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
          >
            This Month
          </button>
          <button
            onClick={() => setTimeframe('all')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${timeframe === 'all'
              ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
          >
            All Time
          </button>
        </div>
      </div>

      {/* Podium — Top 3 */}
      {top3.length >= 3 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6 text-center">🏆 Top Performers</h2>
          <div className="flex items-end justify-center gap-3 sm:gap-5 max-w-3xl mx-auto pb-2">
            {podiumOrder.map((entry) => {
              const info = getMedalInfo(entry.podiumRank)
              return (
                <div
                  key={entry.podiumRank}
                  className={`flex-1 max-w-[200px] ${info.height} bg-gradient-to-b ${info.bg} border ${info.border} rounded-xl flex flex-col items-center justify-start pt-8 pb-4 px-3 relative transition-transform hover:scale-[1.02]`}
                >
                  {/* Medal badge */}
                  <div className="absolute -top-5 left-1/2 -translate-x-1/2 w-10 h-10 rounded-full bg-white dark:bg-slate-700 flex items-center justify-center text-xl shadow-lg border-2 border-white dark:border-slate-600">
                    {info.medal}
                  </div>

                  {/* Avatar */}
                  <div className={`w-14 h-14 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white font-bold text-lg ring-3 ${info.avatarRing} shrink-0`}>
                    {getInitials(entry.username)}
                  </div>

                  {/* Username - clearly visible */}
                  <p className="text-sm font-semibold text-gray-900 dark:text-white mt-3 text-center leading-snug w-full" title={entry.username}>
                    {entry.username}
                  </p>

                  {/* Score */}
                  <div className={`mt-2 px-3 py-1 rounded-full text-xs font-bold ${
                    entry.greenScore >= 80 ? 'text-green-700 dark:text-green-300 bg-green-100 dark:bg-green-900/40' :
                    entry.greenScore >= 70 ? 'text-blue-700 dark:text-blue-300 bg-blue-100 dark:bg-blue-900/40' :
                    'text-yellow-700 dark:text-yellow-300 bg-yellow-100 dark:bg-yellow-900/40'
                  }`}>
                    {entry.greenScore}/100
                  </div>

                  {/* Badges count */}
                  {entry.badges.length > 0 && (
                    <div className="mt-1.5 text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                      <span>🏅</span>
                      <span>{entry.badges.length} badge{entry.badges.length > 1 ? 's' : ''}</span>
                    </div>
                  )}

                  {/* Stats */}
                  <div className="mt-1 text-[11px] text-gray-500 dark:text-gray-400 text-center">
                    {entry.submissions} submissions
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Remaining Rankings (4+) */}
      {rest.length > 0 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-slate-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Rankings</h2>
          </div>

          <div className="divide-y divide-gray-200 dark:divide-slate-700">
            {rest.map((entry) => (
              <div
                key={entry.rank}
                className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    {/* Rank number */}
                    <div className="flex items-center justify-center w-8 h-8 bg-gray-100 dark:bg-slate-700 rounded-full">
                      <span className="text-sm font-medium text-gray-600 dark:text-gray-300">{entry.rank}</span>
                    </div>

                    {/* Avatar */}
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white font-bold text-sm">
                      {getInitials(entry.username)}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <h3 className="text-base font-medium text-gray-900 dark:text-white">{entry.username}</h3>
                        {entry.badges.length > 0 && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300" title={entry.badges.join(', ')}>
                            🏅 {entry.badges.length}
                          </span>
                        )}
                      </div>
                      <div className="flex items-center space-x-4 mt-1">
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          {entry.submissions} submissions
                        </span>
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          {entry.carbonSaved.toFixed(3)} g CO₂ saved
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${entry.greenScore >= 80 ? 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30' :
                      entry.greenScore >= 70 ? 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30' :
                        entry.greenScore >= 60 ? 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30' :
                          'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30'
                      }`}>
                      {entry.greenScore}/100
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Green Score</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Show all entries in table if less than 3 total */}
      {top3.length < 3 && leaderboard.length > 0 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-slate-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Rankings</h2>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-slate-700">
            {leaderboard.map((entry) => (
              <div
                key={entry.rank}
                className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center justify-center w-8 h-8 bg-gray-100 dark:bg-slate-700 rounded-full">
                      <span className="text-sm font-medium text-gray-600 dark:text-gray-300">{entry.rank}</span>
                    </div>
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white font-bold text-sm">
                      {getInitials(entry.username)}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-base font-medium text-gray-900 dark:text-white">{entry.username}</h3>
                      <span className="text-sm text-gray-500 dark:text-gray-400">{entry.submissions} submissions</span>
                    </div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${entry.greenScore >= 80 ? 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/30' : 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30'}`}>
                    {entry.greenScore}/100
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {leaderboard.length === 0 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-12 text-center">
          <p className="text-gray-500 dark:text-gray-400 text-lg">No leaderboard data available for this timeframe.</p>
          <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">Submit code for analysis to appear on the leaderboard!</p>
        </div>
      )}

      {/* Your Position */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Your Performance</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 dark:bg-green-900/30 rounded-lg border border-green-200 dark:border-green-800">
            <p className="text-2xl font-bold text-green-600 dark:text-green-400">{myPerf.rank ? `#${myPerf.rank}` : '—'}</p>
            <p className="text-sm text-green-600 dark:text-green-400">Current Rank</p>
          </div>
          <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg border border-blue-200 dark:border-blue-800">
            <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{myPerf.greenScore.toFixed(1)}</p>
            <p className="text-sm text-blue-600 dark:text-blue-400">Avg Green Score</p>
          </div>
          <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/30 rounded-lg border border-purple-200 dark:border-purple-800">
            <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">{(myPerf.carbonSaved / 1000).toFixed(2)}</p>
            <p className="text-sm text-purple-600 dark:text-purple-400">kg CO₂ Saved</p>
          </div>
        </div>
      </div>

      {/* Achievement Progress */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Achievement Progress</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Carbon Saver</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {(myPerf.carbonSaved / 1000).toFixed(1)} / 5.0 kg CO₂
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                className="bg-green-500 h-2 rounded-full"
                style={{ width: `${Math.min((myPerf.carbonSaved / 5000) * 100, 100)}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Eco-Friendly Champion</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {myPerf.submissions} / 50 submissions
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full"
                style={{ width: `${Math.min((myPerf.submissions / 50) * 100, 100)}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Efficient Coder</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {myPerf.greenScore >= 90 ? 'Achieved!' : `${myPerf.greenScore.toFixed(0)}/90 Score`}
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                className="bg-purple-500 h-2 rounded-full"
                style={{ width: `${Math.min((myPerf.greenScore / 90) * 100, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Leaderboard
