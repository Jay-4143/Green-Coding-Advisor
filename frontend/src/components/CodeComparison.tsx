import React, { useState } from 'react'

interface CodeSuggestion {
  finding: string
  before_code: string
  after_code: string
  explanation: string
  predicted_improvement: {
    green_score?: number
    energy_wh?: number
  }
  severity: 'low' | 'medium' | 'high'
}

interface CodeComparisonProps {
  suggestions: CodeSuggestion[]
}

const CodeComparison: React.FC<CodeComparisonProps> = ({ suggestions }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(0)

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-300 dark:border-red-800'
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-300 dark:border-yellow-800'
      case 'low':
        return 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 border-blue-300 dark:border-blue-800'
      default:
        return 'bg-gray-100 dark:bg-slate-700 text-gray-800 dark:text-gray-200 border-gray-300 dark:border-slate-600'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return '🔴'
      case 'medium':
        return '🟡'
      case 'low':
        return '🔵'
      default:
        return '⚪'
    }
  }

  if (!suggestions || suggestions.length === 0) {
    return null
  }

  return (
    <div className="space-y-4">
      <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Code Optimization Suggestions</h4>
      {suggestions.map((suggestion, index) => (
        <div
          key={index}
          className={`border-2 rounded-lg overflow-hidden ${getSeverityColor(suggestion.severity)}`}
        >
          <button
            onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-opacity-80 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <span className="text-xl">{getSeverityIcon(suggestion.severity)}</span>
              <div className="text-left">
                <h5 className="font-semibold">{suggestion.finding}</h5>
                <p className="text-sm opacity-75 mt-1">{suggestion.explanation}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {suggestion.predicted_improvement.green_score && (
                <div className="text-right">
                  <div className="text-xs opacity-75">Predicted Improvement</div>
                  <div className="font-bold">+{suggestion.predicted_improvement.green_score} Green Score</div>
                </div>
              )}
              <svg
                className={`w-5 h-5 transform transition-transform ${
                  expandedIndex === index ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </button>

          {expandedIndex === index && (
            <div className="bg-white dark:bg-slate-800 border-t-2 border-gray-200 dark:border-slate-700 p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h6 className="font-semibold text-red-700 dark:text-red-300 flex items-center space-x-2">
                      <span>Before</span>
                      <span className="text-xs bg-red-100 dark:bg-red-900/30 px-2 py-1 rounded">Inefficient</span>
                    </h6>
                  </div>
                  <pre className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded p-3 text-sm overflow-x-auto">
                    <code className="text-red-900 dark:text-red-200">{suggestion.before_code}</code>
                  </pre>
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h6 className="font-semibold text-green-700 dark:text-green-300 flex items-center space-x-2">
                      <span>After</span>
                      <span className="text-xs bg-green-100 dark:bg-green-900/30 px-2 py-1 rounded">Optimized</span>
                    </h6>
                  </div>
                  <pre className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded p-3 text-sm overflow-x-auto">
                    <code className="text-green-900 dark:text-green-200">{suggestion.after_code}</code>
                  </pre>
                </div>
              </div>
              <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded">
                <p className="text-sm text-blue-900 dark:text-blue-200">
                  <strong>Explanation:</strong> {suggestion.explanation}
                </p>
                {suggestion.predicted_improvement.energy_wh && (
                  <p className="text-xs text-blue-700 dark:text-blue-300 mt-2">
                    Estimated energy savings: {Math.abs(suggestion.predicted_improvement.energy_wh * 1000).toFixed(2)} mWh per execution
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default CodeComparison

