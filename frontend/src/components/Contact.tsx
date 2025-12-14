import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  FadeInUp,
  AnimatedHeading,
  StaggerContainer,
  StaggerItem,
} from './animations'

const Contact: React.FC = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
    // TODO: Wire to backend/email service when available
  }

  return (
    <div className="min-h-screen relative">
      {/* Full-Screen Background */}
      <div 
        className="fixed inset-0 z-0"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundAttachment: 'fixed'
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/90 via-slate-800/90 to-slate-900/90"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex items-center justify-center py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-md rounded-2xl shadow-2xl p-8 md:p-12 space-y-6">
            <FadeInUp>
              <div className="text-center mb-8">
                <AnimatedHeading level={1} className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
                  Contact Us
                </AnimatedHeading>
                <p className="text-lg text-gray-600 dark:text-gray-300">
                  Have questions or feedback? Reach out and we&apos;ll get back to you soon.
                </p>
              </div>
            </FadeInUp>

            {submitted ? (
              <FadeInUp>
                <div className="p-6 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 border-2 border-emerald-200 dark:border-emerald-800 text-center">
                  <div className="text-5xl mb-4">✅</div>
                  <h3 className="text-xl font-semibold text-emerald-800 dark:text-emerald-200 mb-2">Thank You!</h3>
                  <p className="text-emerald-700 dark:text-emerald-300">
                    Thanks for contacting us! We&apos;ll be in touch soon.
                  </p>
                </div>
              </FadeInUp>
            ) : (
              <FadeInUp delay={0.2}>
                <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Name
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    className="w-full border-2 border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 bg-white dark:bg-slate-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full border-2 border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 bg-white dark:bg-slate-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                    placeholder="your.email@example.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Message
                  </label>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    required
                    rows={6}
                    className="w-full border-2 border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 bg-white dark:bg-slate-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all resize-none"
                    placeholder="Tell us how we can help..."
                  />
                </div>
                  <motion.button
                    type="submit"
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    className="w-full px-6 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-lg font-semibold text-lg transition-all shadow-lg"
                  >
                    Send Message
                  </motion.button>
                </form>
              </FadeInUp>
            )}

            {/* Contact Info */}
            <FadeInUp delay={0.4}>
              <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
                <StaggerContainer className="grid md:grid-cols-3 gap-6 text-center" staggerDelay={0.1}>
                  <StaggerItem>
                    <div>
                      <div className="text-3xl mb-2">📧</div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Email</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">vasanijay3008@gmail.com</p>
                    </div>
                  </StaggerItem>
                  <StaggerItem>
                    <div>
                      <div className="text-3xl mb-2">🌐</div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Website</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">www.greencoding.com</p>
                    </div>
                  </StaggerItem>
                  <StaggerItem>
                    <div>
                      <div className="text-3xl mb-2">💬</div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Chat</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Available 24/7</p>
                    </div>
                  </StaggerItem>
                </StaggerContainer>
              </div>
            </FadeInUp>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Contact
