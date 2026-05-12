import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import apiClient from '../api/client'
import {
  FadeInUp,
  StaggerContainer,
  StaggerItem,
} from './animations'

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

interface TeamMemberInfo {
  id: number
  username: string
  email: string
  role: string
  joined_at: string
}

interface Activity {
  id: number
  user_id: number
  username: string
  filename: string
  language: string
  green_score: number | null
  created_at: string
}

const Teams: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([])
  const [selectedTeam, setSelectedTeam] = useState<TeamDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newTeamName, setNewTeamName] = useState('')
  const [newTeamDescription, setNewTeamDescription] = useState('')
  const [showAddMemberModal, setShowAddMemberModal] = useState(false)
  const [newMemberEmail, setNewMemberEmail] = useState('')
  const [memberError, setMemberError] = useState<string | null>(null)
  const [memberSuccess, setMemberSuccess] = useState<string | null>(null)
  const [createError, setCreateError] = useState<string | null>(null)
  const [members, setMembers] = useState<TeamMemberInfo[]>([])
  const [activities, setActivities] = useState<Activity[]>([])
  const [showCreateProjectModal, setShowCreateProjectModal] = useState(false)
  const [newProjectName, setNewProjectName] = useState('')
  const [newProjectDesc, setNewProjectDesc] = useState('')
  const [showEditTeamModal, setShowEditTeamModal] = useState(false)
  const [editTeamName, setEditTeamName] = useState('')
  const [editTeamDesc, setEditTeamDesc] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchTeams()
  }, [])

  const fetchTeams = async () => {
    try {
      setLoading(true)
      const res = await apiClient.get('/teams')
      const teamsList = res.data || []
      setTeams(teamsList)
      if (teamsList.length > 0 && !selectedTeam) {
        fetchTeamDashboard(teamsList[0].id)
      }
    } catch (error) {
      console.error('Error fetching teams:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTeamDashboard = async (teamId: number) => {
    try {
      const [dashRes, membersRes, actRes] = await Promise.all([
        apiClient.get(`/teams/${teamId}/dashboard`),
        apiClient.get(`/teams/${teamId}/members`).catch(() => ({ data: [] })),
        apiClient.get(`/teams/${teamId}/activity`).catch(() => ({ data: { activities: [] } }))
      ])
      setSelectedTeam(dashRes.data)
      setMembers(membersRes.data || [])
      setActivities(actRes.data?.activities || [])
    } catch (error) {
      console.error('Error fetching team dashboard:', error)
    }
  }

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedTeam) return
    try {
      await apiClient.post('/projects', { name: newProjectName, description: newProjectDesc, team_id: selectedTeam.team.id })
      setNewProjectName(''); setNewProjectDesc(''); setShowCreateProjectModal(false)
      fetchTeamDashboard(selectedTeam.team.id)
    } catch (error: any) {
      alert(error?.response?.data?.detail || 'Failed to create project')
    }
  }

  const handleDeleteProject = async (projectId: number) => {
    if (!confirm('Delete this project?')) return
    try {
      await apiClient.delete(`/projects/${projectId}`)
      if (selectedTeam) fetchTeamDashboard(selectedTeam.team.id)
    } catch (error: any) {
      alert(error?.response?.data?.detail || 'Failed to delete project')
    }
  }

  const handleRemoveMember = async (userId: number, username: string) => {
    if (!selectedTeam || !confirm(`Remove ${username} from the team?`)) return
    try {
      await apiClient.delete(`/teams/${selectedTeam.team.id}/members/${userId}`)
      fetchTeamDashboard(selectedTeam.team.id)
    } catch (error: any) {
      alert(error?.response?.data?.detail || 'Failed to remove member')
    }
  }

  const handleEditTeam = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedTeam) return
    try {
      await apiClient.put(`/teams/${selectedTeam.team.id}`, { name: editTeamName, description: editTeamDesc })
      setShowEditTeamModal(false)
      fetchTeams()
      fetchTeamDashboard(selectedTeam.team.id)
    } catch (error: any) {
      alert(error?.response?.data?.detail || 'Failed to update team')
    }
  }

  const handleCreateTeam = async (e: React.FormEvent) => {
    e.preventDefault()
    setCreateError(null)
    try {
      const res = await apiClient.post('/teams', {
        name: newTeamName,
        description: newTeamDescription
      })
      const newTeam = res.data
      setTeams(prev => [...prev, newTeam])
      setNewTeamName('')
      setNewTeamDescription('')
      setShowCreateModal(false)
      // Immediately load the new team's dashboard
      fetchTeamDashboard(newTeam.id)
    } catch (error: any) {
      console.error('Error creating team:', error)
      setCreateError(error?.response?.data?.detail || 'Failed to create team. Please try again.')
    }
  }

  const handleAddMember = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedTeam) return

    setMemberError(null)
    setMemberSuccess(null)

    try {
      await apiClient.post(`/teams/${selectedTeam.team.id}/members`, {
        email: newMemberEmail,
        role: 'member'
      })
      setMemberSuccess(`Member "${newMemberEmail}" added successfully!`)
      setNewMemberEmail('')
      // Refresh dashboard to show new member
      fetchTeamDashboard(selectedTeam.team.id)
      // Auto-close after 2 seconds
      setTimeout(() => {
        setShowAddMemberModal(false)
        setMemberSuccess(null)
      }, 2000)
    } catch (error: any) {
      console.error('Error adding member:', error)
      const detail = error?.response?.data?.detail
      if (detail) {
        setMemberError(detail)
      } else if (error?.response?.status === 404) {
        setMemberError('User with this email not found. Please make sure the user has registered an account first.')
      } else if (error?.response?.status === 400) {
        setMemberError('This user is already a member of this team.')
      } else if (error?.response?.status === 403) {
        setMemberError('You do not have permission to add members to this team.')
      } else {
        setMemberError('Failed to add member. Please check the email and try again.')
      }
    }
  }

  const handleDeleteTeam = async (teamId: number, teamName: string) => {
    if (!confirm(`Delete team "${teamName}"? This action cannot be undone.`)) return
    try {
      await apiClient.delete(`/teams/${teamId}`)
      // Remove from local state
      setTeams(prev => prev.filter(t => t.id !== teamId))
      // Clear selected if it was the deleted team
      if (selectedTeam?.team.id === teamId) {
        setSelectedTeam(null)
      }
      // Re-fetch teams to update sidebar
      fetchTeams()
    } catch (error: any) {
      console.error('Error deleting team:', error)
      alert(error?.response?.data?.detail || 'Failed to delete team')
    }
  }

  return (
    <div className="space-y-6 bg-slate-50 dark:bg-slate-900 min-h-screen p-4 sm:p-6">
      <FadeInUp>
        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-lg p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Team Dashboard</h1>
              <p className="text-green-100">
                Collaborate with your team to create sustainable code
              </p>
            </div>
            <motion.button
              onClick={() => { setShowCreateModal(true); setCreateError(null); }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              className="px-4 py-2 bg-white dark:bg-slate-800 text-emerald-600 dark:text-emerald-400 rounded-md font-medium hover:bg-emerald-50 dark:hover:bg-slate-700"
            >
              + Create Team
            </motion.button>
          </div>
        </div>
      </FadeInUp>

      {/* Create Team Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Create New Team</h2>
            
            {createError && (
              <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
                <p className="text-sm text-red-700 dark:text-red-300">{createError}</p>
              </div>
            )}

            <form onSubmit={handleCreateTeam} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Team Name
                </label>
                <input
                  type="text"
                  value={newTeamName}
                  onChange={(e) => setNewTeamName(e.target.value)}
                  className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Description
                </label>
                <textarea
                  value={newTeamDescription}
                  onChange={(e) => setNewTeamDescription(e.target.value)}
                  className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white"
                  rows={3}
                />
              </div>
              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="flex-1 bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700"
                >
                  Create Team
                </button>
                <button
                  type="button"
                  onClick={() => { setShowCreateModal(false); setCreateError(null); }}
                  className="flex-1 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md hover:bg-gray-300 dark:hover:bg-slate-600"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Member Modal */}
      {showAddMemberModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Add Team Member</h2>
            
            {memberError && (
              <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md flex items-start gap-2">
                <svg className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-sm text-red-700 dark:text-red-300">{memberError}</p>
              </div>
            )}

            {memberSuccess && (
              <div className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-md flex items-start gap-2">
                <svg className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <p className="text-sm text-green-700 dark:text-green-300">{memberSuccess}</p>
              </div>
            )}

            <form onSubmit={handleAddMember} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Member Email
                </label>
                <input
                  type="email"
                  value={newMemberEmail}
                  onChange={(e) => { setNewMemberEmail(e.target.value); setMemberError(null); }}
                  className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white"
                  placeholder="user@example.com"
                  required
                />
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">The user must have a registered account to be added.</p>
              </div>
              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="flex-1 bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700"
                >
                  Add Member
                </button>
                <button
                  type="button"
                  onClick={() => { setShowAddMemberModal(false); setMemberError(null); setMemberSuccess(null); }}
                  className="flex-1 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md hover:bg-gray-300 dark:hover:bg-slate-600"
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
          <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">My Teams</h2>
            <div className="space-y-2">
              {teams.map((team) => (
                <div
                  key={team.id}
                  className={`flex items-center justify-between px-4 py-2 rounded-md group ${selectedTeam?.team.id === team.id
                    ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
                    : 'hover:bg-gray-100 dark:hover:bg-slate-700'
                    }`}
                >
                  <button
                    onClick={() => fetchTeamDashboard(team.id)}
                    className="flex-1 text-left"
                  >
                    <div className="font-medium text-gray-900 dark:text-white">{team.name}</div>
                    {team.description && (
                      <div className="text-sm text-gray-500 dark:text-gray-400 truncate">{team.description}</div>
                    )}
                  </button>
                  <button
                    onClick={(e) => { e.stopPropagation(); handleDeleteTeam(team.id, team.name); }}
                    className="ml-2 p-1.5 rounded-md text-red-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Delete team"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              ))}
              {teams.length === 0 && (
                <p className="text-gray-500 dark:text-gray-400 text-sm">No teams yet. Create one to get started!</p>
              )}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          {selectedTeam ? (
            <div className="space-y-6">
              {/* Team Header with Edit */}
              <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{selectedTeam.team.name}</h2>
                  <button onClick={() => { setEditTeamName(selectedTeam.team.name); setEditTeamDesc(selectedTeam.team.description || ''); setShowEditTeamModal(true); }} className="p-2 text-gray-400 hover:text-emerald-600 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700" title="Edit Team">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                  </button>
                </div>
                {selectedTeam.team.description && <p className="text-gray-600 dark:text-gray-300 mb-4">{selectedTeam.team.description}</p>}

                {/* 5 Stat Cards */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4">
                  <div className="bg-indigo-50 dark:bg-indigo-900/30 rounded-lg p-3 border border-indigo-200 dark:border-indigo-800 text-center">
                    <p className="text-xs text-indigo-600 dark:text-indigo-400">Members</p>
                    <p className="text-xl font-bold text-indigo-900 dark:text-indigo-200">{selectedTeam.metrics.total_members}</p>
                  </div>
                  <div className="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 border border-blue-200 dark:border-blue-800 text-center">
                    <p className="text-xs text-blue-600 dark:text-blue-400">Avg Score</p>
                    <p className="text-xl font-bold text-blue-900 dark:text-blue-200">{selectedTeam.metrics.average_green_score.toFixed(1)}</p>
                  </div>
                  <div className="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 border border-green-200 dark:border-green-800 text-center">
                    <p className="text-xs text-green-600 dark:text-green-400">Submissions</p>
                    <p className="text-xl font-bold text-green-900 dark:text-green-200">{selectedTeam.metrics.total_submissions}</p>
                  </div>
                  <div className="bg-emerald-50 dark:bg-emerald-900/30 rounded-lg p-3 border border-emerald-200 dark:border-emerald-800 text-center">
                    <p className="text-xs text-emerald-600 dark:text-emerald-400">CO₂ Saved</p>
                    <p className="text-xl font-bold text-emerald-900 dark:text-emerald-200">{selectedTeam.metrics.total_co2_saved.toFixed(1)}g</p>
                  </div>
                  <div className="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3 border border-amber-200 dark:border-amber-800 text-center">
                    <p className="text-xs text-amber-600 dark:text-amber-400">Energy</p>
                    <p className="text-xl font-bold text-amber-900 dark:text-amber-200">{selectedTeam.metrics.total_energy_saved.toFixed(2)}Wh</p>
                  </div>
                </div>
              </div>

              {/* Team Members */}
              <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Team Members ({members.length})</h3>
                  <button onClick={() => { setShowAddMemberModal(true); setMemberError(null); setMemberSuccess(null); }} className="text-sm text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 font-medium">+ Add Member</button>
                </div>
                <div className="space-y-2">
                  {members.map((m) => (
                    <div key={m.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg group">
                      <div className="flex items-center space-x-3">
                        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white font-bold text-sm">
                          {m.username?.slice(0,2).toUpperCase() || '??'}
                        </div>
                        <div>
                          <div className="font-medium text-gray-900 dark:text-white text-sm">{m.username}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">{m.email}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${m.role === 'admin' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' : 'bg-gray-100 text-gray-600 dark:bg-gray-600 dark:text-gray-300'}`}>{m.role}</span>
                        {m.role !== 'admin' && (
                          <button onClick={() => handleRemoveMember(m.id, m.username)} className="p-1 text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity" title="Remove member">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                  {members.length === 0 && <p className="text-gray-500 text-sm text-center py-3">No members yet.</p>}
                </div>
              </div>

              {/* Leaderboard */}
              <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Team Leaderboard</h3>
                <div className="space-y-2">
                  {selectedTeam.leaderboard.map((member, index) => (
                    <div key={member.user_id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={`flex items-center justify-center w-7 h-7 rounded-full text-sm font-bold ${index === 0 ? 'bg-yellow-100 text-yellow-700' : index === 1 ? 'bg-gray-100 text-gray-600' : index === 2 ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'}`}>{index + 1}</div>
                        <div>
                          <div className="font-medium text-gray-900 dark:text-white text-sm">{member.username}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">{member.total_submissions} submissions · {member.total_co2_saved.toFixed(1)}g CO₂</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`font-bold text-sm ${member.average_green_score >= 70 ? 'text-green-600' : member.average_green_score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>{member.average_green_score.toFixed(1)}</div>
                        <div className="text-[10px] text-gray-400">Score</div>
                      </div>
                    </div>
                  ))}
                  {selectedTeam.leaderboard.length === 0 && <p className="text-gray-500 text-sm text-center py-3">No submissions yet.</p>}
                </div>
              </div>

              {/* Projects */}
              <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Team Projects ({selectedTeam.projects.length})</h3>
                  <button onClick={() => setShowCreateProjectModal(true)} className="text-sm text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 font-medium">+ New Project</button>
                </div>
                <div className="space-y-2">
                  {selectedTeam.projects.map((project) => (
                    <div key={project.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg group">
                      <div>
                        <div className="font-medium text-gray-900 dark:text-white text-sm">{project.name}</div>
                        {project.description && <div className="text-xs text-gray-500 dark:text-gray-400">{project.description}</div>}
                      </div>
                      <div className="flex items-center gap-2">
                        <button onClick={() => navigate(`/projects/${project.id}`)} className="px-3 py-1 bg-emerald-600 text-white rounded text-xs hover:bg-emerald-700">View</button>
                        <button onClick={() => handleDeleteProject(project.id)} className="p-1 text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity" title="Delete project">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                        </button>
                      </div>
                    </div>
                  ))}
                  {selectedTeam.projects.length === 0 && <p className="text-gray-500 text-sm text-center py-3">No projects yet. Create one to get started!</p>}
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Activity</h3>
                <div className="space-y-2">
                  {activities.map((a) => (
                    <div key={a.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                          <svg className="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>
                        </div>
                        <div>
                          <div className="text-sm text-gray-900 dark:text-white"><span className="font-medium">{a.username}</span> submitted <span className="font-mono text-xs bg-gray-200 dark:bg-slate-600 px-1 rounded">{a.filename}</span></div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">{a.language} · {a.created_at ? new Date(a.created_at).toLocaleDateString() : ''}</div>
                        </div>
                      </div>
                      {a.green_score != null && (
                        <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${a.green_score >= 70 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' : a.green_score >= 50 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'}`}>{a.green_score.toFixed(0)}</span>
                      )}
                    </div>
                  ))}
                  {activities.length === 0 && <p className="text-gray-500 text-sm text-center py-3">No recent activity.</p>}
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-12 text-center">
              <svg className="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              <p className="text-gray-500 dark:text-gray-400 text-lg">Select a team to view dashboard</p>
              <p className="text-gray-400 dark:text-gray-500 text-sm mt-1">Or create a new team to get started</p>
            </div>
          )}
        </div>
      </div>

      {/* Edit Team Modal */}
      {showEditTeamModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Edit Team</h2>
            <form onSubmit={handleEditTeam} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Team Name</label>
                <input type="text" value={editTeamName} onChange={(e) => setEditTeamName(e.target.value)} className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                <textarea value={editTeamDesc} onChange={(e) => setEditTeamDesc(e.target.value)} className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white" rows={3} />
              </div>
              <div className="flex space-x-4">
                <button type="submit" className="flex-1 bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700">Save</button>
                <button type="button" onClick={() => setShowEditTeamModal(false)} className="flex-1 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md hover:bg-gray-300 dark:hover:bg-slate-600">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Project Modal */}
      {showCreateProjectModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Create Project</h2>
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Project Name</label>
                <input type="text" value={newProjectName} onChange={(e) => setNewProjectName(e.target.value)} className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                <textarea value={newProjectDesc} onChange={(e) => setNewProjectDesc(e.target.value)} className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white" rows={3} />
              </div>
              <div className="flex space-x-4">
                <button type="submit" className="flex-1 bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700">Create</button>
                <button type="button" onClick={() => setShowCreateProjectModal(false)} className="flex-1 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md hover:bg-gray-300 dark:hover:bg-slate-600">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Teams
