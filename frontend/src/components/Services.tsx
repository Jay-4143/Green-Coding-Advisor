import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  HeroSection,
  FadeInUp,
  AnimatedHeading,
  StaggerContainer,
  StaggerItem,
} from './animations'

const Services: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section with Full-Screen Background */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundAttachment: 'fixed'
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-slate-900/90 via-slate-800/90 to-slate-900/90"></div>
        </div>
        <HeroSection className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <FadeInUp delay={0.2}>
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 drop-shadow-2xl">Our Services</h1>
          </FadeInUp>
          <FadeInUp delay={0.4}>
            <p className="text-xl text-emerald-100 drop-shadow-lg">
              Comprehensive tools for sustainable software development
            </p>
          </FadeInUp>
        </HeroSection>
      </section>

      {/* Services Grid */}
      <section className="py-20 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4">
          <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-8" staggerDelay={0.1}>
            {/* Code Analysis */}
            <StaggerItem>
              <div className="bg-gradient-to-br from-emerald-50 to-green-50 dark:from-emerald-900/30 dark:to-green-900/30 rounded-xl p-8 shadow-lg border border-emerald-200 dark:border-emerald-800">
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Code Analysis</h3>
              <p className="text-gray-700 dark:text-gray-200 mb-4">
                Deep analysis of your code's energy consumption, complexity, and environmental impact. 
                Get detailed metrics on CPU usage, memory consumption, and CO₂ emissions.
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 mb-4">
                <li>Multi-language support</li>
                <li>Real-time analysis</li>
                <li>Detailed performance metrics</li>
              </ul>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                  <Link 
                    to="/submit" 
                    className="inline-block mt-4 px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
                  >
                    Try Now
                  </Link>
                </motion.div>
              </div>
            </StaggerItem>

            {/* AI Recommendations */}
            <StaggerItem>
              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-xl p-8 shadow-lg border border-blue-200 dark:border-blue-800">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI Recommendations</h3>
              <p className="text-gray-700 dark:text-gray-200 mb-4">
                Receive intelligent, actionable suggestions to optimize your code for better 
                performance and lower energy consumption. Powered by advanced machine learning.
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 mb-4">
                <li>Context-aware suggestions</li>
                <li>Before/after code comparisons</li>
                <li>Severity-based prioritization</li>
              </ul>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                  <Link 
                    to="/submit" 
                    className="inline-block mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Try Now
                  </Link>
                </motion.div>
              </div>
            </StaggerItem>

            {/* Analytics Dashboard */}
            <StaggerItem>
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/30 dark:to-pink-900/30 rounded-xl p-8 shadow-lg border border-purple-200 dark:border-purple-800">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Analytics Dashboard</h3>
              <p className="text-gray-700 dark:text-gray-200 mb-4">
                Track your progress with comprehensive dashboards showing your green score history, 
                energy savings, and environmental impact over time.
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 mb-4">
                <li>Visual charts and graphs</li>
                <li>Historical data tracking</li>
                <li>Customizable reports</li>
              </ul>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                  <Link 
                    to="/dashboard" 
                    className="inline-block mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                  >
                    View Dashboard
                  </Link>
                </motion.div>
              </div>
            </StaggerItem>

            {/* Team Collaboration */}
            <StaggerItem>
              <div className="bg-gradient-to-br from-orange-50 to-yellow-50 dark:from-orange-900/30 dark:to-yellow-900/30 rounded-xl p-8 shadow-lg border border-orange-200 dark:border-orange-800">
              <div className="text-5xl mb-4">👥</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Team Collaboration</h3>
              <p className="text-gray-700 dark:text-gray-200 mb-4">
                Work together with your team to achieve sustainability goals. Create teams, 
                share projects, and compete on team leaderboards.
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 mb-4">
                <li>Team creation and management</li>
                <li>Shared projects</li>
                <li>Team leaderboards</li>
              </ul>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                  <Link 
                    to="/teams" 
                    className="inline-block mt-4 px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
                  >
                    Join Team
                  </Link>
                </motion.div>
              </div>
            </StaggerItem>

            {/* Badge System */}
            <StaggerItem>
              <div className="bg-gradient-to-br from-indigo-50 to-blue-50 dark:from-indigo-900/30 dark:to-blue-900/30 rounded-xl p-8 shadow-lg border border-indigo-200 dark:border-indigo-800">
              <div className="text-5xl mb-4">🏆</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Gamification</h3>
              <p className="text-gray-700 dark:text-gray-200 mb-4">
                Earn badges and achievements as you improve your coding practices. 
                Track your streaks and compete on global leaderboards.
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 mb-4">
                <li>Multiple badge types</li>
                <li>Streak tracking</li>
                <li>Global leaderboards</li>
              </ul>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                  <Link 
                    to="/badges" 
                    className="inline-block mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                  >
                    View Badges
                  </Link>
                </motion.div>
              </div>
            </StaggerItem>

            {/* AI Chatbot */}
            <StaggerItem>
              <div className="bg-gradient-to-br from-teal-50 to-green-50 dark:from-teal-900/30 dark:to-green-900/30 rounded-xl p-8 shadow-lg border border-teal-200 dark:border-teal-800">
              <div className="text-5xl mb-4">💬</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI Chatbot</h3>
              <p className="text-gray-700 dark:text-gray-200 mb-4">
                Get instant answers to your questions about green coding practices, 
                optimization techniques, and best practices from our AI assistant.
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 mb-4">
                <li>24/7 availability</li>
                <li>Context-aware responses</li>
                <li>Question suggestions</li>
              </ul>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                  <Link 
                    to="/chatbot" 
                    className="inline-block mt-4 px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
                  >
                    Chat Now
                  </Link>
                </motion.div>
              </div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-20 text-white overflow-hidden">
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundAttachment: 'fixed'
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-slate-900/90 via-slate-800/90 to-slate-900/90"></div>
        </div>
        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <FadeInUp>
            <AnimatedHeading level={2} className="text-4xl font-bold mb-4 text-white">
              Ready to Get Started?
            </AnimatedHeading>
            <p className="text-xl mb-8 text-emerald-100">
              Join thousands of developers making a positive environmental impact
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              <motion.div whileHover={{ scale: 1.05, y: -2 }} whileTap={{ scale: 0.98 }}>
                <Link 
                  to="/signup" 
                  className="inline-block px-8 py-4 bg-white text-emerald-600 rounded-lg font-semibold text-lg hover:bg-emerald-50 transition-all shadow-lg"
                >
                  Sign Up Free
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05, y: -2 }} whileTap={{ scale: 0.98 }}>
                <Link 
                  to="/about" 
                  className="inline-block px-8 py-4 bg-white/10 backdrop-blur-md text-white rounded-lg font-semibold text-lg hover:bg-white/20 transition-all border-2 border-white/30"
                >
                  Learn More
                </Link>
              </motion.div>
            </div>
          </FadeInUp>
        </div>
      </section>
    </div>
  )
}

export default Services
