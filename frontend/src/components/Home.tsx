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

const Home: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section with Full-Screen Background */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background Video/Image */}
        <div
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80')`,
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
              Green Coding Advisor
            </h1>
          </FadeInUp>
          <FadeInUp delay={0.4}>
            <p className="text-xl md:text-2xl text-emerald-100 mb-8 drop-shadow-lg">
              AI-Enhanced Platform for Sustainable Coding Practices
            </p>
          </FadeInUp>
          <FadeInUp delay={0.6}>
            <p className="text-lg text-white/90 mb-10 max-w-2xl mx-auto drop-shadow-md">
              Analyze your code's environmental impact, reduce energy consumption, and contribute to a greener future through intelligent coding practices.
            </p>
          </FadeInUp>
          <FadeInUp delay={0.8}>
            <div className="flex gap-4 justify-center flex-wrap">

              <motion.div
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.98 }}
              >
                <Link
                  to="/about"
                  className="inline-block px-8 py-4 bg-white/10 backdrop-blur-md text-white rounded-lg font-semibold text-lg border-2 border-white/30"
                >
                  Learn More
                </Link>
              </motion.div>
            </div>
          </FadeInUp>
        </HeroSection>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <AnimatedHeading level={2} className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-4">
              Why Choose Green Coding Advisor?
            </AnimatedHeading>
            <p className="text-xl text-center text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto">
              Empower your development team with tools to write more efficient, sustainable code
            </p>
          </FadeInUp>

          <StaggerContainer className="grid md:grid-cols-3 gap-8" staggerDelay={0.15}>
            <StaggerItem>
              <div className="bg-gradient-to-br from-emerald-50 to-green-50 dark:from-emerald-900/30 dark:to-green-900/30 rounded-xl p-8 shadow-lg border border-emerald-200 dark:border-emerald-800">
                <div className="text-5xl mb-4">🌱</div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Carbon Footprint Analysis</h3>
                <p className="text-gray-700 dark:text-gray-200">
                  Get real-time analysis of your code's energy consumption and CO₂ emissions. Understand the environmental impact of every line of code.
                </p>
              </div>
            </StaggerItem>

            <StaggerItem>
              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-xl p-8 shadow-lg border border-blue-200 dark:border-blue-800">
                <div className="text-5xl mb-4">🤖</div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI-Powered Suggestions</h3>
                <p className="text-gray-700 dark:text-gray-200">
                  Receive intelligent recommendations to optimize your code for better performance and lower energy consumption.
                </p>
              </div>
            </StaggerItem>

            <StaggerItem>
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/30 dark:to-pink-900/30 rounded-xl p-8 shadow-lg border border-purple-200 dark:border-purple-800">
                <div className="text-5xl mb-4">📊</div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Comprehensive Analytics</h3>
                <p className="text-gray-700 dark:text-gray-200">
                  Track your progress with detailed metrics, badges, and leaderboards. See your impact on the environment in real-time.
                </p>
              </div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative py-20 text-white overflow-hidden">
        <div
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundAttachment: 'fixed'
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-slate-900/90 via-slate-800/90 to-slate-900/90"></div>
        </div>
        <div className="relative z-10 max-w-7xl mx-auto px-4">
          <StaggerContainer className="grid md:grid-cols-4 gap-8 text-center" staggerDelay={0.1}>
            <StaggerItem>
              <div>
                <div className="text-5xl font-bold mb-2">1000+</div>
                <div className="text-emerald-100">Code Analyses</div>
              </div>
            </StaggerItem>
            <StaggerItem>
              <div>
                <div className="text-5xl font-bold mb-2">500+</div>
                <div className="text-emerald-100">Active Users</div>
              </div>
            </StaggerItem>
            <StaggerItem>
              <div>
                <div className="text-5xl font-bold mb-2">50%</div>
                <div className="text-emerald-100">Avg. Energy Reduction</div>
              </div>
            </StaggerItem>
            <StaggerItem>
              <div>
                <div className="text-5xl font-bold mb-2">10K+</div>
                <div className="text-emerald-100">CO₂ Saved (g)</div>
              </div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <FadeInUp>
            <AnimatedHeading level={2} className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Ready to Make a Difference?
            </AnimatedHeading>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
              Join thousands of developers committed to sustainable coding practices
            </p>
            <motion.div
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.98 }}
            >
              <Link
                to="/journey"
                className="inline-block px-10 py-5 bg-emerald-600 text-white rounded-lg font-semibold text-lg shadow-lg"
              >
                Start Your Journey
              </Link>
            </motion.div>
          </FadeInUp>
        </div>
      </section>
    </div >
  )
}

export default Home
