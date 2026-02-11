import React, { useState } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import apiClient from '../api/client'

const Settings: React.FC = () => {
  const { theme, toggleTheme } = useTheme()
  const [activeTab, setActiveTab] = useState<'preferences' | 'integrations'>('preferences')
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)
  const [apiKey, setApiKey] = useState<string | null>(null)


  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 bg-slate-50 dark:bg-slate-900 min-h-screen">
      <div className="space-y-6">
        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-lg p-6 text-white shadow-lg">
          <h1 className="text-3xl font-bold mb-2">Settings</h1>
          <p className="text-emerald-100">
            Manage your preferences and account settings
          </p>
        </div>

        {message && (
          <div
            className={`p-4 rounded-lg ${message.type === 'success'
              ? 'bg-green-50 border border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-300'
              : 'bg-red-50 border border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-800 dark:text-red-300'
              }`}
          >
            {message.text}
          </div>
        )}

        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md">
          <div className="border-b border-gray-200 dark:border-slate-700">
            <nav className="flex space-x-4 px-6">
              <button
                onClick={() => setActiveTab('preferences')}
                className={`py-4 px-2 border-b-2 font-medium text-sm ${activeTab === 'preferences'
                  ? 'border-green-500 dark:border-green-400 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
              >
                Preferences
              </button>
              <button
                onClick={() => setActiveTab('integrations')}
                className={`py-4 px-2 border-b-2 font-medium text-sm ${activeTab === 'integrations'
                  ? 'border-green-500 dark:border-green-400 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
              >
                Integrations
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Preferences</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 dark:text-white">Dark Mode</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">Switch between light and dark theme</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        className="sr-only peer"
                        checked={theme === 'dark'}
                        onChange={toggleTheme}
                      />
                      <div className="w-11 h-6 bg-gray-200 dark:bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600 dark:peer-checked:bg-green-500"></div>
                    </label>
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">Email Notifications</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">Receive email notifications for analysis results</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked />
                      <div className="w-11 h-6 bg-gray-200 dark:bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600 dark:peer-checked:bg-green-500"></div>
                    </label>
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">Weekly Reports</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">Receive weekly summary reports via email</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" />
                      <div className="w-11 h-6 bg-gray-200 dark:bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600 dark:peer-checked:bg-green-500"></div>
                    </label>
                  </div>
                </div>
                <div className="flex justify-end space-x-4">
                  <button
                    onClick={async () => {
                      try {
                        await apiClient.post('/reports/weekly-email')
                        setMessage({ type: 'success', text: 'Weekly report sent successfully' })
                        setTimeout(() => setMessage(null), 3000)
                      } catch (error) {
                        console.error('Failed to send weekly report:', error)
                        setMessage({ type: 'error', text: 'Failed to send weekly report' })
                        setTimeout(() => setMessage(null), 3000)
                      }
                    }}
                    className="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium underline"
                  >
                    Send Weekly Report
                  </button>
                  <button
                    onClick={async () => {
                      try {
                        await apiClient.post('/reports/test-email')
                        setMessage({ type: 'success', text: 'Test email sent successfully' })
                        setTimeout(() => setMessage(null), 3000)
                      } catch (error) {
                        console.error('Failed to send test email:', error)
                        setMessage({ type: 'error', text: 'Failed to send test email' })
                        setTimeout(() => setMessage(null), 3000)
                      }
                    }}
                    className="text-sm text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300 font-medium underline"
                  >
                    Send Test Email
                  </button>
                </div>
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-white">Badge Notifications</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Get notified when you earn new badges</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 dark:bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600 dark:peer-checked:bg-green-500"></div>
                  </label>
                </div>
              </div>
            )}

            {activeTab === 'integrations' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Integrations</h2>
                <div className="space-y-4">
                  <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-gray-50 dark:bg-gray-900/50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900 dark:text-white">GitHub Integration</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">Connect your GitHub account to analyze repositories</p>
                      </div>
                      <button
                        onClick={() => {
                          alert("GitHub integration coming soon! This will allow you to sync repositories.")
                        }}
                        className="px-4 py-2 bg-gray-600 dark:bg-gray-700 text-white rounded-md hover:bg-gray-700 dark:hover:bg-gray-600 text-sm transition-colors"
                      >
                        Connect
                      </button>
                    </div>
                  </div>
                  <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-gray-50 dark:bg-gray-900/50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900 dark:text-white">VS Code Extension</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">Install our VS Code extension for real-time suggestions</p>
                      </div>
                      <button
                        onClick={() => {
                          window.open('https://marketplace.visualstudio.com/search?term=green+coding', '_blank')
                        }}
                        className="px-4 py-2 bg-blue-600 dark:bg-blue-700 text-white rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 text-sm transition-colors"
                      >
                        Install
                      </button>
                    </div>
                  </div>
                  <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-gray-50 dark:bg-gray-900/50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900 dark:text-white">API Key</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">Generate API key for programmatic access</p>
                        {apiKey && (
                          <div className="mt-2 p-2 bg-slate-100 dark:bg-slate-800 rounded border border-slate-300 dark:border-slate-600 font-mono text-xs break-all">
                            {apiKey}
                          </div>
                        )}
                      </div>
                      <button
                        onClick={async () => {
                          try {
                            const res = await apiClient.post('/auth/api-key')
                            setApiKey(res.data.api_key)
                            setMessage({ type: 'success', text: 'API Key generated successfully' })
                            setTimeout(() => setMessage(null), 3000)
                          } catch (error) {
                            console.error('Failed to generate API key:', error)
                            setMessage({ type: 'error', text: 'Failed to generate API Key' })
                            setTimeout(() => setMessage(null), 3000)
                          }
                        }}
                        className="px-4 py-2 bg-green-600 dark:bg-green-700 text-white rounded-md hover:bg-green-700 dark:hover:bg-green-600 text-sm transition-colors"
                      >
                        {apiKey ? 'Regenerate' : 'Generate'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings

