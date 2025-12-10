import React from 'react'
import { Link } from 'react-router-dom'

const Home: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section with Background Image */}
      <section 
        className="relative min-h-[90vh] flex items-center justify-center bg-gradient-to-br from-emerald-900 via-green-800 to-teal-900"
        style={{
          backgroundImage: `url('/images/1.jpg')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundBlendMode: 'overlay'
        }}
      >
        <div className="absolute inset-0 bg-black/50"></div>
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 drop-shadow-lg">
            Green Coding Advisor
          </h1>
          <p className="text-xl md:text-2xl text-emerald-100 mb-8 drop-shadow-md">
            AI-Enhanced Platform for Sustainable Coding Practices
          </p>
          <p className="text-lg text-white/90 mb-10 max-w-2xl mx-auto">
            Analyze your code's environmental impact, reduce energy consumption, and contribute to a greener future through intelligent coding practices.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link 
              to="/submit" 
              className="px-8 py-4 bg-emerald-600 text-white rounded-lg font-semibold text-lg hover:bg-emerald-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              Get Started
            </Link>
            <Link 
              to="/about" 
              className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white rounded-lg font-semibold text-lg hover:bg-white/20 transition-all border-2 border-white/30"
            >
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">Why Choose Green Coding Advisor?</h2>
          <p className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto">
            Empower your development team with tools to write more efficient, sustainable code
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">🌱</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Carbon Footprint Analysis</h3>
              <p className="text-gray-700">
                Get real-time analysis of your code's energy consumption and CO₂ emissions. Understand the environmental impact of every line of code.
              </p>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI-Powered Suggestions</h3>
              <p className="text-gray-700">
                Receive intelligent recommendations to optimize your code for better performance and lower energy consumption.
              </p>
            </div>
            
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Comprehensive Analytics</h3>
              <p className="text-gray-700">
                Track your progress with detailed metrics, badges, and leaderboards. See your impact on the environment in real-time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section 
        className="py-20 bg-gradient-to-r from-emerald-600 to-teal-600 text-white"
        style={{
          backgroundImage: `url('/images/2.jpg')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundBlendMode: 'overlay'
        }}
      >
        <div className="absolute inset-0 bg-emerald-900/70"></div>
        <div className="relative z-10 max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold mb-2">1000+</div>
              <div className="text-emerald-100">Code Analyses</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">500+</div>
              <div className="text-emerald-100">Active Users</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">50%</div>
              <div className="text-emerald-100">Avg. Energy Reduction</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">10K+</div>
              <div className="text-emerald-100">CO₂ Saved (g)</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Ready to Make a Difference?</h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of developers committed to sustainable coding practices
          </p>
          <Link 
            to="/signup" 
            className="inline-block px-10 py-5 bg-emerald-600 text-white rounded-lg font-semibold text-lg hover:bg-emerald-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            Start Your Journey
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home

