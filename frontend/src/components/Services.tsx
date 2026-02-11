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
  const isAuthenticated = Boolean(localStorage.getItem('access_token'))

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

        {/* Content */}
        <HeroSection className="relative z-10 text-center px-4 max-w-4xl mx-auto">
          <FadeInUp delay={0.2}>
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 drop-shadow-2xl">
              Our Services
            </h1>
          </FadeInUp>
          <FadeInUp delay={0.4}>
            <p className="text-xl md:text-2xl text-emerald-100 mb-8 drop-shadow-lg">
              Comprehensive solutions for sustainable software development
            </p>
          </FadeInUp>
          <FadeInUp delay={0.6}>
            <p className="text-lg text-white/90 mb-10 max-w-2xl mx-auto drop-shadow-md">
              From code analysis to team training, we provide everything you need to build greener, more efficient applications.
            </p>
          </FadeInUp>
          <FadeInUp delay={0.8}>
            <div className="flex gap-4 justify-center flex-wrap">
              {!isAuthenticated && (
                <motion.div
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Link
                    to="/signup"
                    className="inline-block px-8 py-4 bg-emerald-600 text-white rounded-lg font-semibold text-lg shadow-lg"
                  >
                    Start for Free
                  </Link>
                </motion.div>
              )}
              {/* <motion.div
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.98 }}
              >
                <Link
                  to="/contact"
                  className="inline-block px-8 py-4 bg-white/10 backdrop-blur-md text-white rounded-lg font-semibold text-lg border-2 border-white/30"
                >
                  Contact Us
                </Link>
              </motion.div> */}
            </div>
          </FadeInUp>
        </HeroSection>
      </section>

      {/* Services Grid */}
      <section className="py-20 bg-gray-50 dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <AnimatedHeading level={2} className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-4">
              What We Offer
            </AnimatedHeading>
            <p className="text-xl text-center text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto">
              Tools and strategies to minimize your digital carbon footprint
            </p>
          </FadeInUp>

          <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-8" staggerDelay={0.1}>
            {/* Service 1 */}
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-3xl">🔍</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Code Impact Analysis</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Deep analysis of your codebase to identify energy-intensive patterns and provide optimization suggestions.
                </p>
                <Link to="/analysis" className="text-emerald-600 dark:text-emerald-400 font-semibold hover:text-emerald-700 flex items-center">
                  Learn more <span className="ml-2">→</span>
                </Link>
              </div>
            </StaggerItem>

            {/* Service 2 */}
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-3xl">🤖</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">AI Optimization</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Real-time AI-powered code refactoring suggestions to improve performance and reduce carbon emissions.
                </p>
                <Link to="/chatbot" className="text-emerald-600 dark:text-emerald-400 font-semibold hover:text-emerald-700 flex items-center">
                  Try Chatbot <span className="ml-2">→</span>
                </Link>
              </div>
            </StaggerItem>

            {/* Service 3 */}
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-3xl">📊</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Sustainability Reporting</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Detailed environmental impact reports and dashboards to track your team's progress over time.
                </p>
                <Link to="/dashboard" className="text-emerald-600 dark:text-emerald-400 font-semibold hover:text-emerald-700 flex items-center">
                  View Demo <span className="ml-2">→</span>
                </Link>
              </div>
            </StaggerItem>

            {/* Service 4 */}
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-3xl">🎓</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Team Training</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Workshops and resources to educate your development team on green coding principles and best practices.
                </p>
                <Link to="/about" className="text-emerald-600 dark:text-emerald-400 font-semibold hover:text-emerald-700 flex items-center">
                  Get details <span className="ml-2">→</span>
                </Link>
              </div>
            </StaggerItem>

            {/* Service 5 */}
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-teal-100 dark:bg-teal-900/30 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-3xl">🔌</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">CI/CD Integration</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Seamlessly integrate green checks into your deployment pipeline to prevent regression.
                </p>
                <Link to="/settings" className="text-emerald-600 dark:text-emerald-400 font-semibold hover:text-emerald-700 flex items-center">
                  See integrations <span className="ml-2">→</span>
                </Link>
              </div>
            </StaggerItem>

            {/* Service 6 */}
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-3xl">🏆</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Certification</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Get certified as a Green Coding Organization when you meet our sustainability standards.
                </p>
                <Link to="/badges" className="text-emerald-600 dark:text-emerald-400 font-semibold hover:text-emerald-700 flex items-center">
                  View badges <span className="ml-2">→</span>
                </Link>
              </div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* Pricing/CTA Section */}
      <section className="py-20 bg-emerald-900 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <FadeInUp>
            <h2 className="text-4xl font-bold mb-6">Start Your Green Journey Today</h2>
            <p className="text-xl text-emerald-100 mb-10">
              Join leading tech companies in the movement towards sustainable software engineering.
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              {!isAuthenticated && (
                <motion.div whileHover={{ scale: 1.05, y: -2 }} whileTap={{ scale: 0.98 }}>
                  <Link
                    to="/signup"
                    className="inline-block px-8 py-4 bg-white text-emerald-900 rounded-lg font-bold text-lg hover:bg-emerald-50 transition-all shadow-lg"
                  >
                    Sign Up Free
                  </Link>
                </motion.div>
              )}
              <motion.div whileHover={{ scale: 1.05, y: -2 }} whileTap={{ scale: 0.98 }}>
                <Link
                  to="/contact"
                  className="inline-block px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-bold text-lg hover:bg-white/10 transition-all"
                >
                  Contact Sales
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
