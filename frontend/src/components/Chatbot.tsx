import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import apiClient from '../api/client'
import {
  FadeInUp,
} from './animations'

interface Message {
  id: number
  type: 'user' | 'bot'
  content: string
  timestamp: Date
  suggestions?: string[]
  relatedTopics?: string[]
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I am the **Green Coding Architect**, powered by LLaMA-2. I'm here to help you design energy-efficient, sustainable software systems.\n\nAsk me about algorithms, system design, or code optimization!",
      timestamp: new Date(),
      suggestions: [
        "How to optimize a nested loop?",
        "Explain Big-O complexity impact on energy.",
        "Best practices for sustainable web development?"
      ]
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputMessage.trim() || loading) return

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages([...messages, userMessage])
    setInputMessage('')
    setLoading(true)

    try {
      const response = await apiClient.post('/chat/answer', {
        message: inputMessage,
        context: null
      })

      const botMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.answer,
        timestamp: new Date(),
        suggestions: response.data.suggestions,
        relatedTopics: response.data.related_topics
      }

      setMessages([...messages, userMessage, botMessage])
    } catch (error: any) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages([...messages, userMessage, errorMessage])
      console.error('Error sending message:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInputMessage(suggestion)
  }

  return (
    <div className="space-y-6">
      <FadeInUp>
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold mb-2">Green Coding Architect</h1>
              <p className="text-green-100">
                AI-Powered Sustainable Software Engineering Advisor
              </p>
            </div>
            <span className="bg-white/20 px-3 py-1 rounded-full text-xs font-semibold backdrop-blur-sm">
              Powered by LLaMA-2
            </span>
          </div>
        </div>
      </FadeInUp>

      <div className="bg-white rounded-lg shadow-md h-[600px] flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg p-4 ${message.type === 'user'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-gray-100 dark:bg-slate-700 text-gray-900 dark:text-white'
                    }`}
                >
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-3 space-y-2">
                      <p className="text-sm font-medium opacity-75">Suggested questions:</p>
                      {message.suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => handleSuggestionClick(suggestion)}
                          className={`block text-sm p-2 rounded ${message.type === 'user'
                            ? 'bg-emerald-700 hover:bg-emerald-800'
                            : 'bg-white dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-600 text-gray-700 dark:text-gray-300'
                            }`}
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                  {message.relatedTopics && message.relatedTopics.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {message.relatedTopics.map((topic, index) => (
                        <span
                          key={index}
                          className={`text-xs px-2 py-1 rounded ${message.type === 'user'
                            ? 'bg-emerald-700'
                            : 'bg-gray-200 dark:bg-slate-600 text-gray-600 dark:text-gray-300'
                            }`}
                        >
                          {topic.replace('_', ' ')}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 dark:bg-slate-700 rounded-lg p-4">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="border-t border-gray-200 dark:border-slate-700 p-4">
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask a question about green coding..."
              className="flex-1 border border-gray-300 dark:border-gray-600 rounded-md px-4 py-2 bg-white dark:bg-slate-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              disabled={loading}
            />
            <motion.button
              type="submit"
              disabled={loading || !inputMessage.trim()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              className="px-6 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </motion.button>
          </form>
        </div>
      </div>

      <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <p className="text-sm text-blue-800 dark:text-blue-300">
          💡 <strong>Tip:</strong> Ask me about loop optimization, data structures, memory usage, algorithm complexity, or any green coding practices!
        </p>
      </div>
    </div>
  )
}

export default Chatbot

