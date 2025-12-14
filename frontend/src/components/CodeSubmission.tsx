import React, { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'
import CodeComparison from './CodeComparison'

interface SubmissionResult {
  id: string
  greenScore: number
  energyConsumption: number
  co2Emissions: number
  memoryUsage: number
  cpuTime: number
  suggestions: string[]
  language: string
  filename: string
  realWorldImpact?: {
    light_bulb_hours?: number
    tree_planting_days?: number
    car_miles?: number
    description?: string
  }
  codeSuggestions?: Array<{
    finding: string
    before_code: string
    after_code: string
    explanation: string
    predicted_improvement: {
      green_score?: number
      energy_wh?: number
    }
    severity: 'low' | 'medium' | 'high'
  }>
  // New fields for full optimization
  optimizedCode?: string
  originalCode?: string
  comparisonTable?: any
  improvementsExplanation?: string
  expectedGreenScoreImprovement?: string
  detectedLanguage?: string
  analysisSummary?: string
}

function looksLikeLanguage(code: string, language: string): boolean {
  const lang = language.toLowerCase()
  const trimmedCode = code.trim()
  
  // Check if input looks like actual code (not random gibberish)
  function looksLikeCode(text: string): boolean {
    // Must have at least some code structure
    const hasStructure = /[(){}[\];,=+\-*/<>!&|%]/.test(text) ||  // operators/symbols
                         /\b\w+\s*\(/.test(text) ||                 // function calls
                         /\b\w+\s*=/.test(text) ||                  // assignments
                         /['"]/.test(text) ||                       // strings
                         /\/\/|\/\*|#/.test(text)                   // comments
    
    if (!hasStructure) {
      return false  // No code structure at all
    }
    
    // Check for common code patterns (must have at least one)
    const hasCodePatterns = /\b\w+\s*\(/.test(text) ||           // function calls
                             /\b\w+\s*=\s*/.test(text) ||         // assignments
                             /['"].*['"]/.test(text) ||            // strings
                             /\b\w+\s*[+\-*/=<>!]/.test(text) ||  // operators
                             /:\s*$/.test(text) ||                 // colons (if/for/def)
                             /#include|import|from/.test(text) ||  // imports/includes
                             /\/\/|\/\*|#/.test(text)              // comments
    
    if (!hasCodePatterns) {
      return false  // No recognizable code patterns
    }
    
    // Check for random text patterns (reject if looks like gibberish)
    const words = text.match(/\b\w+\b/g) || []
    
    // Check if input is just a long string of random letters (no spaces, no structure)
    if (text.length > 15 && !/\s/.test(text) && !/[(){}[\];,=+\-*/<>!&|%'"]/.test(text)) {
      return false  // Random letter sequence without code structure
    }
    
    // Check for random words (long words that aren't keywords or common code terms)
    const hasOnlyRandomWords = words.length > 0 && 
                               words.every(word => 
                                 word.length > 8 &&  // Long words
                                 !/[(){}[\];,=+\-*/]/.test(word) &&  // No symbols
                                 !/^(def|import|print|function|const|let|var|class|public|private|static|void|int|return|if|for|while|console|System|include|True|False|None|null|undefined)$/i.test(word)  // Not keywords
                               )
    
    if (hasOnlyRandomWords && words.length > 2) {
      return false  // Looks like random text
    }
    
    // Must have at least one recognizable code element
    const hasRecognizableCode = /[(){}[\];,=+\-*/<>!&|%]/.test(text) ||  // Operators
                                 /\b\w+\s*\(/.test(text) ||              // Function calls
                                 /\b\w+\s*=/.test(text) ||               // Assignments
                                 /['"]/.test(text) ||                    // Strings
                                 /:\s*$/.test(text) ||                   // Colons
                                 /#include|import|from|def|function|class|public|private|static|const|let|var/.test(text)  // Keywords
    
    return hasRecognizableCode
  }
  
  // Very short code (less than 10 chars) - check if it looks like code
  if (trimmedCode.length < 10) {
    return looksLikeCode(trimmedCode)
  }
  
  // For longer code, must look like actual code
  if (!looksLikeCode(trimmedCode)) {
    return false
  }
  
  const patterns: Record<string, RegExp[]> = {
    python: [
      /\bdef\s+\w+\s*\(/,           // function definition with name
      /\bimport\s+\w+/,             // import statement
      /\bfrom\s+\w+\s+import/,      // from import
      /\bprint\s*\(/,                // print() function
      /\bself\b/,                   // self parameter
      /:\s*$/,                       // colon at end of line (if/for/while/def)
      /\bif\s+/,                     // if statement
      /\bfor\s+\w+\s+in/,           // for loop with in
      /\bwhile\s+/,                  // while loop
      /\bclass\s+\w+/,              // class definition with name
      /\breturn\b/,                  // return statement
      /\bTrue\b|\bFalse\b/,         // boolean literals
      /\bNone\b/,                    // None literal
      /\[.*\]/,                      // list literal
      /\{.*\}/,                      // dict literal
      /#.*/,                         // comment
      /\belif\b/,                    // elif keyword
      /\bpass\b/,                    // pass keyword
      /\bwith\s+/,                   // with statement
    ],
    javascript: [
      /\bfunction\b/,               // function keyword
      /\bconst\b/,                  // const keyword
      /\blet\b/,                    // let keyword
      /\bvar\b/,                    // var keyword
      /=>/,                          // arrow function
      /\bconsole\./,                 // console methods
      /\bdocument\./,                // DOM access
      /\brequire\s*\(/,              // require()
      /\bimport\s+/,                 // ES6 import
      /\/\/.*|\/\*.*\*\//,          // comments
      /\$\{.*\}/,                    // template literals
      /\bexport\b/,                  // export keyword
      /\.then\(/,                    // Promise.then
      /\.catch\(/,                   // Promise.catch
      /async\s+function/,            // async function
      /await\s+/,                    // await keyword
      /\.map\(/,                     // array.map
      /\.filter\(/,                  // array.filter
      /\.reduce\(/,                  // array.reduce
      /\.forEach\(/,                 // array.forEach
    ],
    java: [
      /\bpublic\b/,                 // public keyword
      /\bprivate\b/,                 // private keyword
      /\bstatic\b/,                 // static keyword
      /\bclass\b/,                   // class keyword
      /\bvoid\b/,                    // void return type
      /\bint\b/,                     // int type
      /\bString\b/,                  // String type
      /\bSystem\.out\./,             // System.out.println
      /\bimport\s+java/,            // Java imports
      /@Override/,                   // annotations
      /\bnew\s+\w+\(/,               // new keyword
    ],
    cpp: [
      /#include/,                    // include directive
      /\bstd::/,                     // std namespace
      /\bint\s+main\s*\(/,           // main function
      /\busing\s+namespace/,         // using namespace
      /\bcout\s*<</,                 // cout output
      /\bcin\s*>>/,                  // cin input
      /\bnew\s+/,                    // new keyword
      /\bdelete\s+/,                 // delete keyword
      /\/\/.*|\/\*.*\*\//,          // comments
    ],
    c: [
      /#include/,                    // include directive
      /\bint\s+main\s*\(/,           // main function
      /\bprintf\s*\(/,                // printf function
      /\bscanf\s*\(/,                 // scanf function
      /\breturn\s+/,                  // return statement
      /\/\/.*|\/\*.*\*\//,          // comments
    ],
  }
  
  // Get patterns for the selected language
  const checks = patterns[lang] || []
  if (!checks.length) return true  // Unknown language - allow it
  
  // Check if code matches any pattern for the selected language
  const matchesLanguage = checks.some((re) => re.test(code))
  
  // Check for strong anti-patterns from other languages (reject if found)
  const antiPatterns: Record<string, RegExp[]> = {
    python: [
      /\bpublic\s+static\s+void\s+main/,  // Java main
      /\bpublic\s+class/,                  // Java class
      /\bprivate\s+/,                      // Java private
      /\bstatic\s+/,                       // Java static
      /#include/,                          // C/C++ include
      /\bfunction\s+\w+\s*\(/,            // JavaScript function declaration
      /\bconsole\./,                       // JavaScript console (any method)
      /\bconst\s+\w+\s*=/,                 // JavaScript const
      /\blet\s+\w+\s*=/,                   // JavaScript let
      /\bvar\s+\w+\s*=/,                   // JavaScript var
      /=>/,                                // JavaScript arrow function
      /\bexport\s+/,                       // JavaScript export
      /\brequire\s*\(/,                    // JavaScript require
      /\.then\(|\.catch\(/,                // JavaScript Promises
      /\basync\s+/,                        // JavaScript async
      /\bawait\s+/,                        // JavaScript await
      /\bstd::/,                           // C++ namespace
      /\bint\s+main\s*\(/,                 // C/C++ main
      /\bvoid\s+/,                         // Java/C void
    ],
    javascript: [
      /\bdef\s+\w+\s*\(/,                 // Python def
      /\bimport\s+\w+\s*$/,               // Python import (without from)
      /\bfrom\s+\w+\s+import/,            // Python from import
      /\bprint\s*\(/,                      // Python print
      /\bself\b/,                          // Python self
      /\bTrue\b|\bFalse\b/,                // Python booleans (capitalized)
      /\bNone\b/,                          // Python None
      /:\s*$/,                             // Python colon at end of line
      /\belif\b/,                          // Python elif
      /\bpass\b/,                          // Python pass
      /\bpublic\s+static/,                 // Java
      /\bpublic\s+class/,                  // Java class
      /\bprivate\s+/,                      // Java private
      /\bvoid\s+/,                         // Java void
      /#include/,                          // C/C++
      /\bstd::/,                           // C++ namespace
      /\bint\s+main\s*\(/,                 // C/C++ main
    ],
    java: [
      /\bdef\s+\w+\s*\(/,                 // Python def
      /\bprint\s*\(/,                      // Python print
      /\bimport\s+\w+\s*$/,               // Python import
      /\bself\b/,                          // Python self
      /\bTrue\b|\bFalse\b/,                // Python booleans
      /\bNone\b/,                          // Python None
      /#include/,                          // C/C++ include
      /=>/,                                // JavaScript arrow
      /\bconsole\.log/,                    // JavaScript console
      /\bconst\s+\w+\s*=/,                 // JavaScript const
      /\blet\s+\w+\s*=/,                   // JavaScript let
      /\bstd::/,                           // C++ namespace
    ],
    cpp: [
      /\bdef\s+\w+\s*\(/,                 // Python def
      /\bprint\s*\(/,                      // Python print
      /\bimport\s+\w+\s*$/,               // Python import
      /\bself\b/,                          // Python self
      /\bpublic\s+static\s+void\s+main/,  // Java main
      /\bpublic\s+class/,                  // Java class
      /=>/,                                // JavaScript arrow
      /\bconsole\.log/,                    // JavaScript console
      /\bconst\s+\w+\s*=/,                 // JavaScript const
      /\blet\s+\w+\s*=/,                   // JavaScript let
    ],
    c: [
      /\bdef\s+\w+\s*\(/,                 // Python def
      /\bprint\s*\(/,                      // Python print
      /\bimport\s+\w+\s*$/,               // Python import
      /\bself\b/,                          // Python self
      /\bpublic\s+static\s+void\s+main/,  // Java main
      /\bpublic\s+class/,                  // Java class
      /=>/,                                // JavaScript arrow
      /\bconsole\.log/,                    // JavaScript console
      /\bconst\s+\w+\s*=/,                 // JavaScript const
      /\blet\s+\w+\s*=/,                   // JavaScript let
      /\bstd::/,                           // C++ namespace
    ],
  }
  
  const antiChecks = antiPatterns[lang] || []
  const hasAntiPattern = antiChecks.some((re) => re.test(code))
  
  // If strong anti-patterns are found, reject it
  if (hasAntiPattern) {
    return false
  }
  
  // For code longer than 20 characters, require at least one match with selected language
  // This ensures uploaded files match the selected language
  if (trimmedCode.length > 20) {
    return matchesLanguage
  }
  
  // For shorter code, be more lenient but still prefer language match
  return matchesLanguage || !hasAntiPattern
}

const CodeSubmission: React.FC = () => {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [filename, setFilename] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SubmissionResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const languages = [
    { value: 'python', label: 'Python' },
    { value: 'javascript', label: 'JavaScript' },
    { value: 'java', label: 'Java' },
    { value: 'cpp', label: 'C++' },
    { value: 'c', label: 'C' }
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!code.trim()) {
      setError('Please enter some code to analyze')
      return
    }

    const token = localStorage.getItem('access_token')
    if (!token) {
      setError('Please log in first to submit and track analyses.')
      return
    }

    if (!looksLikeLanguage(code, language)) {
      setError('The code does not look like the selected language. Please select the correct language.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // First, try to get fully optimized code
      let optimizeData: any = null
      try {
        const optimizeResponse = await apiClient.post('/submissions/optimize', {
          code: code.trim(),
          language: language || undefined,
          region: 'usa'
        })
        optimizeData = optimizeResponse.data
      } catch (optimizeError) {
        // If optimization fails, we'll fall back to regular analysis
        console.warn('Optimization endpoint failed, falling back to analysis:', optimizeError)
      }

      // Create submission so it is persisted for dashboard/metrics
      const createRes = await apiClient.post('/submissions', {
        code_content: code.trim(),
        language: optimizeData.detected_language || language,
        filename: filename || `code.${(optimizeData.detected_language || language) === 'javascript' ? 'js' : (optimizeData.detected_language || language)}`,
      })
      const submissionId = createRes.data?.id
      if (!submissionId) {
        throw new Error('Submission failed')
      }

      // Analyze and persist metrics (for dashboard tracking)
      const analyzeResponse = await apiClient.post(`/submissions/${submissionId}/analyze`)
      const analyzeData = analyzeResponse.data

      // Use optimized code metrics if available, otherwise fall back to analysis
      const metrics = optimizeData?.comparison_table ? {
        green_score: optimizeData.comparison_table.green_score?.optimized || analyzeData.green_score,
        energy_consumption_wh: parseFloat(optimizeData.comparison_table.energy_usage?.optimized?.replace(' Wh', '') || String(analyzeData.energy_consumption_wh)),
        co2_emissions_g: parseFloat(optimizeData.comparison_table.co2_emissions?.optimized?.replace(' g', '') || String(analyzeData.co2_emissions_g)),
        cpu_time_ms: parseFloat(optimizeData.comparison_table.cpu_time?.optimized?.replace(' ms', '') || String(analyzeData.cpu_time_ms)),
        memory_usage_mb: parseFloat(optimizeData.comparison_table.memory_usage?.optimized?.replace(' MB', '') || String(analyzeData.memory_usage_mb)),
      } : analyzeData

      const normalized: SubmissionResult = {
        id: String(submissionId),
        greenScore: metrics.green_score,
        energyConsumption: metrics.energy_consumption_wh,
        co2Emissions: metrics.co2_emissions_g,
        memoryUsage: metrics.memory_usage_mb,
        cpuTime: metrics.cpu_time_ms,
        suggestions: optimizeData?.improvements_explanation 
          ? optimizeData.improvements_explanation.split('\n').filter((s: string) => s.trim())
          : Array.isArray(analyzeData.suggestions)
            ? analyzeData.suggestions.map((s: any) => (typeof s === 'string' ? s : s.explanation || s.finding || ''))
            : [],
        language: optimizeData?.detected_language || language,
        filename: filename || `code.${(optimizeData?.detected_language || language) === 'javascript' ? 'js' : (optimizeData?.detected_language || language)}`,
        realWorldImpact: analyzeData.real_world_impact || analyzeData.analysis_details?.real_world_impact || undefined,
        codeSuggestions: Array.isArray(analyzeData.suggestions)
          ? analyzeData.suggestions
              .filter((s: any) => typeof s === 'object' && s.before_code && s.after_code)
              .map((s: any) => ({
                ...s,
                severity: ['low', 'medium', 'high'].includes(String(s.severity).toLowerCase())
                  ? (String(s.severity).toLowerCase() as 'low' | 'medium' | 'high')
                  : 'medium',
              }))
          : [],
        // Full optimization data (only if optimization was successful)
        optimizedCode: optimizeData?.optimized_code,
        originalCode: optimizeData?.original_code,
        comparisonTable: optimizeData?.comparison_table,
        improvementsExplanation: optimizeData?.improvements_explanation,
        expectedGreenScoreImprovement: optimizeData?.expected_green_score_improvement,
        detectedLanguage: optimizeData?.detected_language,
        analysisSummary: optimizeData?.analysis_summary
      }

      setResult(normalized)
      try {
        localStorage.setItem('last_analysis', JSON.stringify(normalized))
      } catch {}
      // Navigate to analysis page to view results
      navigate('/analysis')
    } catch (err: any) {
      if (err?.response?.status === 401) {
        setError('Please log in to submit and analyze code.')
      } else {
        setError(err?.response?.data?.detail || err?.message || 'Analysis failed')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFilename(file.name)
      const reader = new FileReader()
      reader.onload = (event) => {
        setCode(event.target?.result as string)
      }
      reader.readAsText(file)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    if (score >= 40) return 'Fair'
    return 'Poor'
  }

  const optimizationSummary = useMemo(() => {
    if (!result?.codeSuggestions || result.codeSuggestions.length === 0) return null

    const withScore = result.codeSuggestions.filter(
      (s) => typeof s.predicted_improvement?.green_score === 'number'
    )
    const best = withScore.length
      ? withScore.reduce((acc, curr) => {
          const currGain = curr.predicted_improvement?.green_score || 0
          const accGain = acc.predicted_improvement?.green_score || 0
          return currGain > accGain ? curr : acc
        })
      : null

    const totalEnergySavedWh = result.codeSuggestions.reduce((sum, s) => {
      const val = typeof s.predicted_improvement?.energy_wh === 'number'
        ? s.predicted_improvement.energy_wh
        : 0
      return sum + val
    }, 0)

    return {
      best,
      totalEnergySavedWh,
    }
  }, [result])

  return (
    <div className="space-y-6 bg-slate-50 dark:bg-slate-900 min-h-screen p-4 sm:p-6">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Submit Code for Analysis</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Programming Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                {languages.map((lang) => (
                  <option key={lang.value} value={lang.value}>
                    {lang.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Filename (optional)
              </label>
              <input
                type="text"
                value={filename}
                onChange={(e) => setFilename(e.target.value)}
                placeholder="e.g., algorithm.py"
                className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Code
            </label>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your code here..."
              rows={15}
              className="w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 font-mono text-sm"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <input
                type="file"
                onChange={handleFileUpload}
                accept=".py,.js,.java,.cpp,.c,.ts,.jsx,.tsx"
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-slate-800 hover:bg-gray-50 dark:hover:bg-slate-700 cursor-pointer"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Upload File
              </label>
            </div>

            <button
              type="submit"
              disabled={loading || !code.trim()}
              className="inline-flex items-center px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  Analyze Code
                </>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
            <div className="flex">
              <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="ml-3">
                <p className="text-sm text-red-800 dark:text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {result && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Analysis Results</h3>
          
          {/* Green Score */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white">Green Score</h4>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                result.greenScore >= 80 ? 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30' :
                result.greenScore >= 60 ? 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30' :
                'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30'
              }`}>
                {result.greenScore}/100 - {getScoreLabel(result.greenScore)}
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div
                className={`h-3 rounded-full ${
                  result.greenScore >= 80 ? 'bg-green-500' :
                  result.greenScore >= 60 ? 'bg-yellow-500' :
                  'bg-red-500'
                }`}
                style={{ width: `${result.greenScore}%` }}
              ></div>
            </div>
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
              <div className="flex items-center">
                <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <div className="ml-3">
                  <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Energy</p>
                  <p className="text-lg font-bold text-blue-900 dark:text-blue-200">{result.energyConsumption.toFixed(2)} Wh</p>
                </div>
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 border border-green-200 dark:border-green-800">
              <div className="flex items-center">
                <svg className="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="ml-3">
                  <p className="text-sm font-medium text-green-600 dark:text-green-400">CO₂</p>
                  <p className="text-lg font-bold text-green-900 dark:text-green-200">{result.co2Emissions.toFixed(3)} g</p>
                </div>
              </div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4 border border-purple-200 dark:border-purple-800">
              <div className="flex items-center">
                <svg className="w-8 h-8 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
                <div className="ml-3">
                  <p className="text-sm font-medium text-purple-600 dark:text-purple-400">Memory</p>
                  <p className="text-lg font-bold text-purple-900 dark:text-purple-200">{result.memoryUsage.toFixed(1)} MB</p>
                </div>
              </div>
            </div>

            <div className="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-4 border border-orange-200 dark:border-orange-800">
              <div className="flex items-center">
                <svg className="w-8 h-8 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="ml-3">
                  <p className="text-sm font-medium text-orange-600 dark:text-orange-400">CPU Time</p>
                  <p className="text-lg font-bold text-orange-900 dark:text-orange-200">{result.cpuTime.toFixed(1)} ms</p>
                </div>
              </div>
            </div>
          </div>

          {/* Real-World Impact */}
          {result.realWorldImpact && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Real-World Impact</h4>
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 rounded-lg p-4 border border-green-200 dark:border-green-800">
                <p className="text-sm text-gray-700 dark:text-gray-200 mb-3 font-medium">
                  {result.realWorldImpact.description || 
                   `Running this code 1M times would:`}
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {result.realWorldImpact.light_bulb_hours && (
                    <div className="bg-white dark:bg-slate-800 rounded-lg p-3 border border-green-200 dark:border-green-800">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">💡</span>
                        <div>
                          <p className="text-xs text-gray-500 dark:text-gray-400">Light Bulb Hours</p>
                          <p className="text-lg font-bold text-green-700 dark:text-green-400">
                            {result.realWorldImpact.light_bulb_hours.toFixed(1)} hrs
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                  {result.realWorldImpact.tree_planting_days && (
                    <div className="bg-white dark:bg-slate-800 rounded-lg p-3 border border-green-200 dark:border-green-800">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🌳</span>
                        <div>
                          <p className="text-xs text-gray-500 dark:text-gray-400">Tree Planting Days</p>
                          <p className="text-lg font-bold text-green-700 dark:text-green-400">
                            {result.realWorldImpact.tree_planting_days.toFixed(1)} days
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                  {result.realWorldImpact.car_miles && (
                    <div className="bg-white dark:bg-slate-800 rounded-lg p-3 border border-green-200 dark:border-green-800">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🚗</span>
                        <div>
                          <p className="text-xs text-gray-500 dark:text-gray-400">Car Miles</p>
                          <p className="text-lg font-bold text-green-700 dark:text-green-400">
                            {result.realWorldImpact.car_miles.toFixed(4)} miles
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

      {/* Optimization Summary */}
      {optimizationSummary && optimizationSummary.best && (
        <div className="mb-6 bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800 rounded-lg p-4 flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm text-emerald-700 dark:text-emerald-300 font-semibold">Top Optimization</p>
            <p className="text-lg font-bold text-emerald-900 dark:text-emerald-200">{optimizationSummary.best.finding}</p>
            <p className="text-sm text-emerald-800 dark:text-emerald-300 mt-1">
              {optimizationSummary.best.explanation}
            </p>
          </div>
          <div className="mt-3 md:mt-0 flex items-center space-x-4">
            {typeof optimizationSummary.best.predicted_improvement?.green_score === 'number' && (
              <div className="px-3 py-2 rounded-md bg-white dark:bg-slate-800 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-sm font-semibold">
                +{optimizationSummary.best.predicted_improvement.green_score} Green Score
              </div>
            )}
            {Math.abs(optimizationSummary.totalEnergySavedWh) > 0 && (
              <div className="px-3 py-2 rounded-md bg-white dark:bg-slate-800 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-sm font-semibold">
                ~{Math.abs(optimizationSummary.totalEnergySavedWh * 1000).toFixed(1)} mWh saved/run
              </div>
            )}
          </div>
        </div>
      )}

      {/* Full Optimized Code Section */}
      {result.optimizedCode && result.originalCode ? (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Full Code Optimization</h4>
          
          {/* Analysis Summary */}
          {result.analysisSummary && (
            <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg">
              <p className="text-sm text-blue-900 dark:text-blue-200">{result.analysisSummary}</p>
            </div>
          )}

          {/* Comparison Table */}
          {result.comparisonTable && (
            <div className="mb-6 overflow-x-auto">
              <h5 className="text-md font-semibold text-gray-900 dark:text-white mb-3">Performance Comparison</h5>
              <table className="min-w-full bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 rounded-lg">
                <thead>
                  <tr className="bg-gray-50 dark:bg-slate-700">
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">Metric</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-red-700 dark:text-red-300 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">Original</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-green-700 dark:text-green-300 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">Optimized</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 dark:text-blue-300 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">Improvement</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {result.comparisonTable.green_score && (
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">Green Score</td>
                      <td className="px-4 py-3 text-sm text-red-600 dark:text-red-400">{result.comparisonTable.green_score.original}</td>
                      <td className="px-4 py-3 text-sm text-green-600 dark:text-green-400 font-semibold">{result.comparisonTable.green_score.optimized}</td>
                      <td className="px-4 py-3 text-sm text-blue-600 dark:text-blue-400 font-semibold">+{result.comparisonTable.green_score.improvement}</td>
                    </tr>
                  )}
                  {result.comparisonTable.energy_usage && (
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">Energy Usage</td>
                      <td className="px-4 py-3 text-sm text-red-600 dark:text-red-400">{result.comparisonTable.energy_usage.original}</td>
                      <td className="px-4 py-3 text-sm text-green-600 dark:text-green-400 font-semibold">{result.comparisonTable.energy_usage.optimized}</td>
                      <td className="px-4 py-3 text-sm text-blue-600 dark:text-blue-400">{result.comparisonTable.energy_usage.improvement}</td>
                    </tr>
                  )}
                  {result.comparisonTable.co2_emissions && (
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">CO₂ Emissions</td>
                      <td className="px-4 py-3 text-sm text-red-600 dark:text-red-400">{result.comparisonTable.co2_emissions.original}</td>
                      <td className="px-4 py-3 text-sm text-green-600 dark:text-green-400 font-semibold">{result.comparisonTable.co2_emissions.optimized}</td>
                      <td className="px-4 py-3 text-sm text-blue-600 dark:text-blue-400">{result.comparisonTable.co2_emissions.improvement}</td>
                    </tr>
                  )}
                  {result.comparisonTable.cpu_time && (
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">CPU Time</td>
                      <td className="px-4 py-3 text-sm text-red-600 dark:text-red-400">{result.comparisonTable.cpu_time.original}</td>
                      <td className="px-4 py-3 text-sm text-green-600 dark:text-green-400 font-semibold">{result.comparisonTable.cpu_time.optimized}</td>
                      <td className="px-4 py-3 text-sm text-blue-600 dark:text-blue-400">{result.comparisonTable.cpu_time.improvement}</td>
                    </tr>
                  )}
                  {result.comparisonTable.memory_usage && (
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">Memory Usage</td>
                      <td className="px-4 py-3 text-sm text-red-600 dark:text-red-400">{result.comparisonTable.memory_usage.original}</td>
                      <td className="px-4 py-3 text-sm text-green-600 dark:text-green-400 font-semibold">{result.comparisonTable.memory_usage.optimized}</td>
                      <td className="px-4 py-3 text-sm text-blue-600 dark:text-blue-400">{result.comparisonTable.memory_usage.improvement}</td>
                    </tr>
                  )}
                  {result.comparisonTable.time_complexity && (
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">Time Complexity</td>
                      <td className="px-4 py-3 text-sm text-red-600 dark:text-red-400">{result.comparisonTable.time_complexity.original}</td>
                      <td className="px-4 py-3 text-sm text-green-600 dark:text-green-400 font-semibold">{result.comparisonTable.time_complexity.optimized}</td>
                      <td className="px-4 py-3 text-sm text-blue-600 dark:text-blue-400">{result.comparisonTable.time_complexity.improvement}</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {/* Code Comparison - Side by Side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h5 className="font-semibold text-red-700 dark:text-red-300 flex items-center space-x-2">
                  <span>Original Code</span>
                  <span className="text-xs bg-red-100 dark:bg-red-900/30 px-2 py-1 rounded">Inefficient</span>
                </h5>
              </div>
              <pre className="bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-lg p-4 text-sm overflow-x-auto max-h-96">
                <code className="text-red-900 dark:text-red-200 font-mono whitespace-pre-wrap">{result.originalCode}</code>
              </pre>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <h5 className="font-semibold text-green-700 dark:text-green-300 flex items-center space-x-2">
                  <span>Optimized Code</span>
                  <span className="text-xs bg-green-100 dark:bg-green-900/30 px-2 py-1 rounded">Optimized</span>
                </h5>
              </div>
              <pre className="bg-green-50 dark:bg-green-900/20 border-2 border-green-200 dark:border-green-800 rounded-lg p-4 text-sm overflow-x-auto max-h-96">
                <code className="text-green-900 dark:text-green-200 font-mono whitespace-pre-wrap">{result.optimizedCode}</code>
              </pre>
            </div>
          </div>

          {/* Improvements Explanation */}
          {result.improvementsExplanation && (
            <div className="mb-4 p-4 bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800 rounded-lg">
              <h5 className="text-md font-semibold text-emerald-900 dark:text-emerald-200 mb-2">Improvements Applied</h5>
              <div className="text-sm text-emerald-800 dark:text-emerald-300 whitespace-pre-line">
                {result.improvementsExplanation}
              </div>
            </div>
          )}

          {/* Expected Improvement */}
          {result.expectedGreenScoreImprovement && (
            <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 border border-green-200 dark:border-green-800 rounded-lg">
              <p className="text-sm font-semibold text-green-900 dark:text-green-200">
                🎯 {result.expectedGreenScoreImprovement}
              </p>
            </div>
          )}
        </div>
      ) : result.codeSuggestions && result.codeSuggestions.length > 0 ? (
        <div className="mb-6">
          <CodeComparison suggestions={result.codeSuggestions} />
        </div>
      ) : (
        <div className="mb-6 bg-gray-50 dark:bg-slate-700 border border-gray-200 dark:border-gray-600 rounded-lg p-4">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Optimized Code</h4>
          <p className="text-sm text-gray-700 dark:text-gray-300">
            The analyzer did not return optimized code for this submission.
          </p>
        </div>
      )}

          {/* Simple Text Suggestions */}
          {result.suggestions && result.suggestions.length > 0 && (
            <div>
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Additional Suggestions</h4>
              <div className="space-y-2">
                {result.suggestions
                  .filter((s: string) => typeof s === 'string')
                  .map((suggestion: string, index: number) => (
                    <div key={index} className="flex items-start p-3 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                      <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      <p className="text-sm text-yellow-800 dark:text-yellow-300">{suggestion}</p>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CodeSubmission
