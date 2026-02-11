import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import apiClient from '../api/client'
import {
    FadeInUp,
    StaggerContainer,
    StaggerItem,
} from './animations'

interface ProjectDetails {
    project: {
        id: number
        name: string
        description: string
        created_at: string
    }
    metrics: {
        total_submissions: number
        average_green_score: number
        total_co2_saved: number
    }
    recent_submissions: Array<{
        id: number
        filename: string
        green_score: number
        co2_emissions_g: number
        created_at: string
    }>
}

const ProjectDetails: React.FC = () => {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const [projectData, setProjectData] = useState<ProjectDetails | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchProjectDetails = async () => {
            try {
                setLoading(true)
                const res = await apiClient.get(`/projects/${id}/summary`)
                setProjectData(res.data)
            } catch (err) {
                console.error('Error fetching project details:', err)
                setError('Failed to load project details')
            } finally {
                setLoading(false)
            }
        }

        if (id) {
            fetchProjectDetails()
        }
    }, [id])

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-slate-50 dark:bg-slate-900">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
            </div>
        )
    }

    if (error || !projectData) {
        return (
            <div className="flex flex-col items-center justify-center h-screen bg-slate-50 dark:bg-slate-900">
                <div className="text-red-500 text-xl font-semibold mb-4">{error || 'Project not found'}</div>
                <button
                    onClick={() => navigate('/teams')}
                    className="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700"
                >
                    Back to Teams
                </button>
            </div>
        )
    }

    return (
        <div className="space-y-6 bg-slate-50 dark:bg-slate-900 min-h-screen p-4 sm:p-6 pt-20">
            <FadeInUp>
                <div className="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-lg p-6 text-white shadow-lg mb-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold mb-2">{projectData.project.name}</h1>
                            <p className="text-emerald-100">{projectData.project.description}</p>
                        </div>
                        <button
                            onClick={() => navigate('/teams')}
                            className="px-4 py-2 bg-white/20 text-white rounded-md hover:bg-white/30 text-sm backdrop-blur-sm"
                        >
                            Back to Teams
                        </button>
                    </div>
                </div>
            </FadeInUp>

            <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 gap-6" staggerDelay={0.1}>
                <StaggerItem>
                    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                        <div className="flex items-center">
                            <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Avg Green Score</p>
                                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                    {projectData.metrics.average_green_score.toFixed(1)}
                                </p>
                            </div>
                        </div>
                    </div>
                </StaggerItem>
                <StaggerItem>
                    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                        <div className="flex items-center">
                            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Total Submissions</p>
                                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                    {projectData.metrics.total_submissions}
                                </p>
                            </div>
                        </div>
                    </div>
                </StaggerItem>
                <StaggerItem>
                    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
                        <div className="flex items-center">
                            <div className="p-3 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">CO₂ Saved</p>
                                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                    {(projectData.metrics.total_co2_saved / 1000).toFixed(3)} kg
                                </p>
                            </div>
                        </div>
                    </div>
                </StaggerItem>
            </StaggerContainer>

            <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6 mt-6">
                <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Recent Activity</h2>
                <div className="overflow-hidden">
                    {projectData.recent_submissions.length > 0 ? (
                        <table className="min-w-full divide-y divide-gray-200 dark:divide-slate-700">
                            <thead className="bg-gray-50 dark:bg-slate-700">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">File</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Score</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">CO₂ Emissions (g)</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Date</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white dark:bg-slate-800 divide-y divide-gray-200 dark:divide-slate-700">
                                {projectData.recent_submissions.map((sub) => (
                                    <tr key={sub.id} className="hover:bg-gray-50 dark:hover:bg-slate-700">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                            {sub.filename}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`px-2 py-1 rounded-full text-xs font-semibold ${sub.green_score >= 80 ? 'bg-green-100 text-green-800' :
                                                    sub.green_score >= 60 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
                                                }`}>
                                                {sub.green_score}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                            {sub.co2_emissions_g.toFixed(4)}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {new Date(sub.created_at).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <p className="text-center text-gray-500 dark:text-gray-400 py-4">No submissions yet.</p>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ProjectDetails
