import React from 'react'

const About: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section 
        className="relative py-24 bg-gradient-to-br from-emerald-900 via-green-800 to-teal-900"
        style={{
          backgroundImage: `url('/images/3.jfif')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundBlendMode: 'overlay'
        }}
      >
        <div className="absolute inset-0 bg-black/60"></div>
        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">About Green Coding Advisor</h1>
          <p className="text-xl text-emerald-100">
            Empowering developers to write sustainable, energy-efficient code
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">Our Mission</h2>
              <p className="text-lg text-gray-700 mb-4">
                At Green Coding Advisor, we believe that every line of code has an environmental impact. 
                Our mission is to help developers understand, measure, and reduce the carbon footprint 
                of their software applications.
              </p>
              <p className="text-lg text-gray-700 mb-4">
                Through AI-powered analysis and intelligent recommendations, we provide developers 
                with the tools they need to write more efficient code that consumes less energy and 
                produces fewer CO₂ emissions.
              </p>
              <p className="text-lg text-gray-700">
                Together, we can make software development more sustainable and contribute to a greener future.
              </p>
            </div>
            <div className="rounded-xl overflow-hidden shadow-2xl">
              <img 
                src="/images/4.jpg" 
                alt="Sustainable coding" 
                className="w-full h-auto"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none'
                }}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <div className="text-4xl mb-4">🌍</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Sustainability</h3>
              <p className="text-gray-700">
                We're committed to reducing the environmental impact of software development 
                through innovative technology and best practices.
              </p>
            </div>
            
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <div className="text-4xl mb-4">💡</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Innovation</h3>
              <p className="text-gray-700">
                We leverage cutting-edge AI and machine learning to provide accurate, 
                actionable insights for code optimization.
              </p>
            </div>
            
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <div className="text-4xl mb-4">🤝</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Community</h3>
              <p className="text-gray-700">
                We believe in building a community of developers who share our vision 
                of sustainable software development.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">How It Works</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">1</div>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">Submit Your Code</h3>
                <p className="text-gray-700">
                  Upload your code files or paste code directly into our platform. 
                  We support multiple programming languages including Python, JavaScript, Java, and C++.
                </p>
              </div>
            </div>
            
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">2</div>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">AI Analysis</h3>
                <p className="text-gray-700">
                  Our advanced AI engine analyzes your code for energy consumption patterns, 
                  complexity, and optimization opportunities.
                </p>
              </div>
            </div>
            
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">3</div>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">Get Insights</h3>
                <p className="text-gray-700">
                  Receive detailed reports with green scores, energy consumption metrics, 
                  CO₂ emissions, and actionable optimization suggestions.
                </p>
              </div>
            </div>
            
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">4</div>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">Track Progress</h3>
                <p className="text-gray-700">
                  Monitor your improvement over time with comprehensive dashboards, 
                  earn badges, and compete on leaderboards.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default About

