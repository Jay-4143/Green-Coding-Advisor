import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

interface Team {
  id: number
  name: string
  description: string
  created_by: number
  created_at: string
}

interface TeamMember {
  id: number
  username: string
  email: string
  role: string
  joined_at: string
}

interface TeamDashboard {
  team: Team
  metrics: {
    total_members: number
    total_projects: number
    total_submissions: number
    average_green_score: number
    total_co2_saved: number
    total_energy_saved: number
  }
  leaderboard: Array<{
    user_id: number
    username: string
    average_green_score: number
    total_submissions: number
    total_co2_saved: number
    role: string
  }>
  projects: Array<{
    id: number
    name: string
    description: string
    created_at: string
  }>
}

const Teams: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([])
  const [selectedTeam, setSelectedTeam] = useState<TeamDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newTeamName, setNewTeamName] = useState('')
  const [newTeamDescription, setNewTeamDescription] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchTeams()
  }, [])

  const fetchTeams = async () => {
    try {
      setLoading(true)
      const res = await apiClient.get('/teams')
      setTeams(res.data || [])
      if (res.data && res.data.length > 0 && !selectedTeam) {
        fetchTeamDashboard(res.data[0].id)
      }
    } catch (error) {
      console.error('Error fetching teams:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTeamDashboard = async (teamId: number) => {
    try {
      const res = await apiClient.get(`/teams/${teamId}/dashboard`)
      setSelectedTeam(res.data)
    } catch (error) {
      console.error('Error fetching team dashboard:', error)
    }
  }

  const handleCreateTeam = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await apiClient.post('/teams', {
        name: newTeamName,
        description: newTeamDescription
      })
      setTeams([...teams, res.data])
      setNewTeamName('')
      setNewTeamDescription('')
      setShowCreateModal(false)
      fetchTeamDashboard(res.data.id)
    } catch (error: any) {
      console.error('Error creating team:', error)
      alert(error?.response?.data?.detail || 'Failed to create team')
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
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Team Dashboard</h1>
            <p className="text-green-100">
              Collaborate with your team to create sustainable code
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-4 py-2 bg-white text-green-600 rounded-md font-medium hover:bg-green-50"
          >
            + Create Team
          </button>
        </div>
      </div>

      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Create New Team</h2>
            <form onSubmit={handleCreateTeam} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Team Name
                </label>
                <input
                  type="text"
                  value={newTeamName}
                  onChange={(e) => setNewTeamName(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={newTeamDescription}
                  onChange={(e) => setNewTeamDescription(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  rows={3}
                />
              </div>
              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
                >
                  Create Team
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">My Teams</h2>
            <div className="space-y-2">
              {teams.map((team) => (
                <button
                  key={team.id}
                  onClick={() => fetchTeamDashboard(team.id)}
                  className={`w-full text-left px-4 py-2 rounded-md ${
                    selectedTeam?.team.id === team.id
                      ? 'bg-green-100 text-green-700'
                      : 'hover:bg-gray-100'
                  }`}
                >
                  <div className="font-medium">{team.name}</div>
                  {team.description && (
                    <div className="text-sm text-gray-500 truncate">{team.description}</div>
                  )}
                </button>
              ))}
              {teams.length === 0 && (
                <p className="text-gray-500 text-sm">No teams yet. Create one to get started!</p>
              )}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          {selectedTeam ? (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-bold mb-2">{selectedTeam.team.name}</h2>
                {selectedTeam.team.description && (
                  <p className="text-gray-600 mb-4">{selectedTeam.team.description}</p>
                )}

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <p className="text-sm text-blue-600">Average Green Score</p>
                    <p className="text-2xl font-bold text-blue-900">
                      {selectedTeam.metrics.average_green_score.toFixed(1)}
                    </p>
                  </div>
                  <div className="bg-green-50 rounded-lg p-4">
                    <p className="text-sm text-green-600">Total Submissions</p>
                    <p className="text-2xl font-bold text-green-900">
                      {selectedTeam.metrics.total_submissions}
                    </p>
                  </div>
                  <div className="bg-emerald-50 rounded-lg p-4">
                    <p className="text-sm text-emerald-600">CO₂ Saved</p>
                    <p className="text-2xl font-bold text-emerald-900">
                      {selectedTeam.metrics.total_co2_saved.toFixed(2)} g
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4">Team Leaderboard</h3>
                <div className="space-y-2">
                  {selectedTeam.leaderboard.map((member, index) => (
                    <div
                      key={member.user_id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center justify-center w-8 h-8 bg-green-100 rounded-full">
                          <span className="text-sm font-medium text-green-700">
                            {index + 1}
                          </span>
                        </div>
                        <div>
                          <div className="font-medium">{member.username}</div>
                          <div className="text-sm text-gray-500">
                            {member.total_submissions} submissions
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold text-green-600">
                          {member.average_green_score.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-500">Green Score</div>
                      </div>
                    </div>
                  ))}
                  {selectedTeam.leaderboard.length === 0 && (
                    <p className="text-gray-500 text-sm text-center py-4">
                      No team members with submissions yet.
                    </p>
                  )}
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4">Team Projects</h3>
                <div className="space-y-2">
                  {selectedTeam.projects.map((project) => (
                    <div
                      key={project.id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <div className="font-medium">{project.name}</div>
                        {project.description && (
                          <div className="text-sm text-gray-500">{project.description}</div>
                        )}
                      </div>
                      <button
                        onClick={() => navigate(`/projects/${project.id}`)}
                        className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
                      >
                        View
                      </button>
                    </div>
                  ))}
                  {selectedTeam.projects.length === 0 && (
                    <p className="text-gray-500 text-sm text-center py-4">
                      No projects yet. Create one to get started!
                    </p>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <p className="text-gray-500">Select a team to view dashboard</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Teams

