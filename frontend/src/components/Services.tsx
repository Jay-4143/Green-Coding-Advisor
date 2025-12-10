import React from 'react'
import { Link } from 'react-router-dom'

const Services: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section 
        className="relative py-24 bg-gradient-to-br from-emerald-900 via-green-800 to-teal-900"
        style={{
          backgroundImage: `url('/images/5.png')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundBlendMode: 'overlay'
        }}
      >
        <div className="absolute inset-0 bg-black/60"></div>
        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">Our Services</h1>
          <p className="text-xl text-emerald-100">
            Comprehensive tools for sustainable software development
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Code Analysis */}
            <div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Code Analysis</h3>
              <p className="text-gray-700 mb-4">
                Deep analysis of your code's energy consumption, complexity, and environmental impact. 
                Get detailed metrics on CPU usage, memory consumption, and CO₂ emissions.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>Multi-language support</li>
                <li>Real-time analysis</li>
                <li>Detailed performance metrics</li>
              </ul>
              <Link 
                to="/submit" 
                className="inline-block mt-4 px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
              >
                Try Now
              </Link>
            </div>

            {/* AI Recommendations */}
            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI Recommendations</h3>
              <p className="text-gray-700 mb-4">
                Receive intelligent, actionable suggestions to optimize your code for better 
                performance and lower energy consumption. Powered by advanced machine learning.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>Context-aware suggestions</li>
                <li>Before/after code comparisons</li>
                <li>Severity-based prioritization</li>
              </ul>
              <Link 
                to="/submit" 
                className="inline-block mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Try Now
              </Link>
            </div>

            {/* Analytics Dashboard */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Analytics Dashboard</h3>
              <p className="text-gray-700 mb-4">
                Track your progress with comprehensive dashboards showing your green score history, 
                energy savings, and environmental impact over time.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>Visual charts and graphs</li>
                <li>Historical data tracking</li>
                <li>Customizable reports</li>
              </ul>
              <Link 
                to="/dashboard" 
                className="inline-block mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                View Dashboard
              </Link>
            </div>

            {/* Team Collaboration */}
            <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">👥</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Team Collaboration</h3>
              <p className="text-gray-700 mb-4">
                Work together with your team to achieve sustainability goals. Create teams, 
                share projects, and compete on team leaderboards.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>Team creation and management</li>
                <li>Shared projects</li>
                <li>Team leaderboards</li>
              </ul>
              <Link 
                to="/teams" 
                className="inline-block mt-4 px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
              >
                Join Team
              </Link>
            </div>

            {/* Badge System */}
            <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">🏆</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Gamification</h3>
              <p className="text-gray-700 mb-4">
                Earn badges and achievements as you improve your coding practices. 
                Track your streaks and compete on global leaderboards.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>Multiple badge types</li>
                <li>Streak tracking</li>
                <li>Global leaderboards</li>
              </ul>
              <Link 
                to="/badges" 
                className="inline-block mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                View Badges
              </Link>
            </div>

            {/* AI Chatbot */}
            <div className="bg-gradient-to-br from-teal-50 to-green-50 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-5xl mb-4">💬</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI Chatbot</h3>
              <p className="text-gray-700 mb-4">
                Get instant answers to your questions about green coding practices, 
                optimization techniques, and best practices from our AI assistant.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>24/7 availability</li>
                <li>Context-aware responses</li>
                <li>Question suggestions</li>
              </ul>
              <Link 
                to="/chatbot" 
                className="inline-block mt-4 px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
              >
                Chat Now
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-600 to-teal-600 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-8 text-emerald-100">
            Join thousands of developers making a positive environmental impact
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link 
              to="/signup" 
              className="px-8 py-4 bg-white text-emerald-600 rounded-lg font-semibold text-lg hover:bg-emerald-50 transition-all shadow-lg"
            >
              Sign Up Free
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
    </div>
  )
}

export default Services

