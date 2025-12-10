import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement,
  Title, 
  Tooltip, 
  Legend,
  ArcElement
} from 'chart.js'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import apiClient from '../api/client'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

interface DashboardStats {
  totalSubmissions: number
  averageGreenScore: number
  carbonSaved: number
  energySaved: number
  badgesEarned: number
  currentStreak: number
  rank: number
}

interface GreenScoreHistory {
  date: string
  score: number
}

interface LanguageStats {
  language: string
  submissions: number
  averageScore: number
  carbonSaved: number
  totalEnergySaved: number
  averageCo2PerSubmission: number
}

interface RecentSubmission {
  id: string
  filename: string
  language: string
  greenScore: number
  carbonSaved: number
  timestamp: string
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate()
  const [userId, setUserId] = useState<number | null>(null)
  const [stats, setStats] = useState<DashboardStats>({
    totalSubmissions: 0,
    averageGreenScore: 0,
    carbonSaved: 0,
    energySaved: 0,
    badgesEarned: 0,
    currentStreak: 0,
    rank: 0
  })
  
  const [greenScoreHistory, setGreenScoreHistory] = useState<GreenScoreHistory[]>([])
  const [languageStats, setLanguageStats] = useState<LanguageStats[]>([])
  const [recentSubmissions, setRecentSubmissions] = useState<RecentSubmission[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        // Get user ID from token or API
        let uid: number | null = null
        try {
          const meRes = await apiClient.get('/auth/me')
          uid = meRes.data?.id
          setUserId(uid)
        } catch (e) {
          console.error('Failed to get user ID:', e)
        }

        // Summary
        const summaryUrl = uid ? `/metrics/summary?user_id=${uid}` : '/metrics/summary'
        const summaryRes = await apiClient.get(summaryUrl)
        const s = summaryRes.data || {}
        
        // Get streak info
        let streakInfo = { current_streak: 0, longest_streak: 0 }
        try {
          const streakRes = await apiClient.get('/streaks/me')
          streakInfo = streakRes.data || streakInfo
        } catch (e) {
          console.error('Failed to get streak info:', e)
        }
        
        setStats({
          totalSubmissions: s.total_submissions || 0,
          averageGreenScore: s.average_green_score || 0,
          carbonSaved: s.total_co2_saved || 0,
          energySaved: s.total_energy_saved || 0,
          badgesEarned: s.badges_earned || 0,
          currentStreak: streakInfo.current_streak || s.current_streak || 0,
          rank: 0,
        })

        // History
        const historyRes = await apiClient.get(uid ? `/metrics/history?user_id=${uid}` : '/metrics/history')
        const points: Array<{date: string; greenScore: number}> = (historyRes.data?.points || []).map((p: any) => ({
          date: p.date,
          score: p.greenScore,
        }))
        setGreenScoreHistory(points)

        // Language stats
        try {
          const langStatsRes = await apiClient.get(uid ? `/metrics/language-stats?user_id=${uid}` : '/metrics/language-stats')
          const langStats = (langStatsRes.data?.language_stats || []).map((stat: any) => ({
            language: stat.language,
            submissions: stat.submissions,
            averageScore: stat.average_green_score,
            carbonSaved: stat.total_co2_saved,
            totalEnergySaved: stat.total_energy_saved,
            averageCo2PerSubmission: stat.average_co2_per_submission
          }))
          setLanguageStats(langStats)
        } catch (e) {
          console.error('Failed to get language stats:', e)
        }

        // Carbon timeline
        try {
          const carbonRes = await apiClient.get(uid ? `/metrics/carbon-timeline?user_id=${uid}&days=30` : '/metrics/carbon-timeline?days=30')
          // Could use this for carbon timeline chart
        } catch (e) {
          console.error('Failed to get carbon timeline:', e)
        }

        // Recent submissions (persisted)
        if (uid) {
          try {
            const recentRes = await apiClient.get(`/submissions/user/${uid}/history`, { params: { limit: 5 } })
            const items = recentRes.data?.items || []
            const mapped: RecentSubmission[] = items.map((s: any) => ({
              id: String(s.id),
              filename: s.filename || 'snippet',
              language: s.language || 'unknown',
              greenScore: s.green_score || 0,
              carbonSaved: (s.co2_emissions_g || 0) / 1000, // show kg
              timestamp: s.created_at || new Date().toISOString(),
            }))
            setRecentSubmissions(mapped)
          } catch (e) {
            console.error('Failed to get recent submissions:', e)
          }
        } else {
          setRecentSubmissions([])
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchDashboardData()
  }, [])

  const greenScoreChartData = {
    labels: greenScoreHistory.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Green Score',
        data: greenScoreHistory.map(item => item.score),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  }

  const languageChartData = {
    labels: languageStats.map(item => item.language.toUpperCase()),
    datasets: [
      {
        label: 'Average Green Score',
        data: languageStats.map(item => item.averageScore),
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(168, 85, 247, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(236, 72, 153, 0.8)',
          'rgba(14, 165, 233, 0.8)'
        ],
        borderColor: [
          'rgb(34, 197, 94)',
          'rgb(59, 130, 246)',
          'rgb(168, 85, 247)',
          'rgb(245, 158, 11)',
          'rgb(239, 68, 68)',
          'rgb(236, 72, 153)',
          'rgb(14, 165, 233)'
        ],
        borderWidth: 2
      }
    ]
  }

  const carbonChartData = {
    labels: languageStats.map(item => item.language.toUpperCase()),
    datasets: [
      {
        label: 'CO₂ Saved (g)',
        data: languageStats.map(item => item.carbonSaved),
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgb(34, 197, 94)',
        borderWidth: 2
      }
    ]
  }

  const energyChartData = {
    labels: languageStats.map(item => item.language.toUpperCase()),
    datasets: [
      {
        label: 'Energy Saved (Wh)',
        data: languageStats.map(item => item.totalEnergySaved),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 2
      }
    ]
  }

  const carbonSavedData = {
    labels: ['Carbon Saved (kg CO₂)', 'Remaining Impact'],
    datasets: [
      {
        data: [stats.carbonSaved, 10 - stats.carbonSaved],
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(156, 163, 175, 0.3)'
        ],
        borderColor: [
          'rgb(34, 197, 94)',
          'rgb(156, 163, 175)'
        ],
        borderWidth: 2
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Green Score Progress'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100
      }
    }
  }

  const barChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Performance by Language'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100
      }
    }
  }

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      title: {
        display: true,
        text: 'Carbon Impact Reduction'
      }
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
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome to Green Coding Advisor</h1>
        <p className="text-green-100">
          You've saved <span className="font-semibold">{stats.carbonSaved} kg CO₂</span> and 
          <span className="font-semibold"> {stats.energySaved} kWh</span> of energy this month!
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Submissions</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalSubmissions}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Green Score</p>
              <p className="text-2xl font-bold text-gray-900">{stats.averageGreenScore}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-emerald-500">
          <div className="flex items-center">
            <div className="p-2 bg-emerald-100 rounded-lg">
              <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Carbon Saved</p>
              <p className="text-2xl font-bold text-gray-900">{stats.carbonSaved} kg</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Badges Earned</p>
              <p className="text-2xl font-bold text-gray-900">{stats.badgesEarned}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Current Streak</p>
              <p className="text-2xl font-bold text-gray-900">{stats.currentStreak} days 🔥</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <Line data={greenScoreChartData} options={chartOptions} />
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <Bar data={languageChartData} options={barChartOptions} />
        </div>
      </div>

      {/* Language Efficiency Charts */}
      {languageStats.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Carbon Emissions by Language</h3>
            <Bar data={carbonChartData} options={{
              ...barChartOptions,
              plugins: {
                ...barChartOptions.plugins,
                title: {
                  display: false
                }
              }
            }} />
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Energy Consumption by Language</h3>
            <Bar data={energyChartData} options={{
              ...barChartOptions,
              plugins: {
                ...barChartOptions.plugins,
                title: {
                  display: false
                }
              }
            }} />
          </div>
        </div>
      )}

      {/* Language Stats Table */}
      {languageStats.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Language Performance Statistics</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Language</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submissions</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Green Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CO₂ Saved (g)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Energy Saved (Wh)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg CO₂/Submission</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {languageStats.map((stat, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                        {stat.language.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{stat.submissions}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        stat.averageScore >= 80 ? 'bg-green-100 text-green-800' :
                        stat.averageScore >= 60 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {stat.averageScore.toFixed(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{stat.carbonSaved.toFixed(3)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{stat.totalEnergySaved.toFixed(4)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{stat.averageCo2PerSubmission.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Carbon Impact and Recent Submissions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <Doughnut data={carbonSavedData} options={doughnutOptions} />
        </div>
        
        <div className="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Submissions</h3>
          <div className="space-y-4">
            {recentSubmissions.map((submission) => (
              <div key={submission.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{submission.filename}</p>
                    <p className="text-sm text-gray-500">{submission.language}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      submission.greenScore >= 80 ? 'bg-green-100 text-green-800' :
                      submission.greenScore >= 60 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {submission.greenScore}
                    </span>
                    <span className="text-sm text-gray-500">
                      {submission.carbonSaved} kg CO₂
                    </span>
                  </div>
                  <p className="text-xs text-gray-400">
                    {new Date(submission.timestamp).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => navigate('/submit')}
            className="flex items-center justify-center p-4 bg-green-50 hover:bg-green-100 rounded-lg border-2 border-dashed border-green-300 transition-colors"
          >
            <div className="text-center">
              <svg className="w-8 h-8 text-green-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <p className="font-medium text-green-800">Submit Code</p>
              <p className="text-sm text-green-600">Analyze new code</p>
            </div>
          </button>
          
          <button
            onClick={async () => {
              try {
                const response = await apiClient.get('/reports/metrics/csv', {
                  responseType: 'blob'
                })
                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', `green-coding-metrics-${new Date().toISOString().split('T')[0]}.csv`)
                document.body.appendChild(link)
                link.click()
                link.remove()
              } catch (error) {
                console.error('Error downloading report:', error)
                alert('Failed to download report')
              }
            }}
            className="flex items-center justify-center p-4 bg-blue-50 hover:bg-blue-100 rounded-lg border-2 border-dashed border-blue-300 transition-colors cursor-pointer"
          >
            <div className="text-center">
              <svg className="w-8 h-8 text-blue-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <p className="font-medium text-blue-800">Download Reports</p>
              <p className="text-sm text-blue-600">CSV & PDF</p>
            </div>
          </button>
          
          <button
            onClick={() => navigate('/chatbot')}
            className="flex items-center justify-center p-4 bg-purple-50 hover:bg-purple-100 rounded-lg border-2 border-dashed border-purple-300 transition-colors"
          >
            <div className="text-center">
              <svg className="w-8 h-8 text-purple-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p className="font-medium text-purple-800">AI Advisor</p>
              <p className="text-sm text-purple-600">Get optimization tips</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
