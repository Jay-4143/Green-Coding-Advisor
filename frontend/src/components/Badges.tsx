import React, { useState, useEffect } from 'react'
import apiClient from '../api/client'

interface Badge {
  id: number
  name: string
  description: string
  icon: string
  points: number
  earned_at?: string
}

const Badges: React.FC = () => {
  const [myBadges, setMyBadges] = useState<Badge[]>([])
  const [allBadges, setAllBadges] = useState<Badge[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'earned' | 'all'>('earned')

  useEffect(() => {
    const fetchBadges = async () => {
      try {
        setLoading(true)
        const [myBadgesRes, allBadgesRes] = await Promise.all([
          apiClient.get('/badges/me'),
          apiClient.get('/badges/all')
        ])
        setMyBadges(myBadgesRes.data?.badges || [])
        setAllBadges(allBadgesRes.data?.badges || [])
      } catch (error) {
        console.error('Error fetching badges:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchBadges()
  }, [])

  const earnedBadgeIds = new Set(myBadges.map(b => b.id))
  const unearnedBadges = allBadges.filter(b => !earnedBadgeIds.has(b.id))

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Badges & Achievements</h1>
        <p className="text-green-100">
          You've earned <span className="font-semibold">{myBadges.length}</span> badges out of{' '}
          <span className="font-semibold">{allBadges.length}</span> available
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex space-x-4 border-b">
          <button
            onClick={() => setActiveTab('earned')}
            className={`px-4 py-2 rounded-t-md font-medium ${
              activeTab === 'earned'
                ? 'bg-green-100 text-green-700 border-b-2 border-green-500'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Earned ({myBadges.length})
          </button>
          <button
            onClick={() => setActiveTab('all')}
            className={`px-4 py-2 rounded-t-md font-medium ${
              activeTab === 'all'
                ? 'bg-green-100 text-green-700 border-b-2 border-green-500'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            All Badges ({allBadges.length})
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {(activeTab === 'earned' ? myBadges : allBadges).map((badge) => {
          const isEarned = earnedBadgeIds.has(badge.id)
          return (
            <div
              key={badge.id}
              className={`bg-white rounded-lg shadow-md p-6 border-2 ${
                isEarned ? 'border-green-500' : 'border-gray-200 opacity-60'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-4xl">{badge.icon}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{badge.name}</h3>
                      <p className="text-sm text-gray-500">{badge.points} points</p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{badge.description}</p>
                  {isEarned && badge.earned_at && (
                    <p className="text-xs text-green-600">
                      Earned on {new Date(badge.earned_at).toLocaleDateString()}
                    </p>
                  )}
                  {!isEarned && (
                    <p className="text-xs text-gray-400">Not yet earned</p>
                  )}
                </div>
                {isEarned && (
                  <div className="ml-4">
                    <svg
                      className="w-6 h-6 text-green-500"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {activeTab === 'all' && unearnedBadges.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            💡 Keep coding green to earn {unearnedBadges.length} more badges!
          </p>
        </div>
      )}
    </div>
  )
}

export default Badges

