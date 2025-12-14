import React from 'react'
import {
  HeroSection,
  FadeInUp,
  AnimatedHeading,
  StaggerContainer,
  StaggerItem,
  AnimatedCard,
} from './animations'

const About: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section with Full-Screen Background */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&q=80')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundAttachment: 'fixed'
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-slate-900/90 via-slate-800/90 to-slate-900/90"></div>
        </div>
        <HeroSection className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <FadeInUp delay={0.2}>
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 drop-shadow-2xl">About Green Coding Advisor</h1>
          </FadeInUp>
          <FadeInUp delay={0.4}>
            <p className="text-xl text-emerald-100 drop-shadow-lg">
              Empowering developers to write sustainable, energy-efficient code
            </p>
          </FadeInUp>
        </HeroSection>
      </section>

      {/* Mission Section */}
      <section className="py-16 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <FadeInUp>
              <div>
                <AnimatedHeading level={2} className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
                  Our Mission
                </AnimatedHeading>
                <p className="text-lg text-gray-700 dark:text-gray-200 mb-4">
                  At Green Coding Advisor, we believe that every line of code has an environmental impact. 
                  Our mission is to help developers understand, measure, and reduce the carbon footprint 
                  of their software applications.
                </p>
                <p className="text-lg text-gray-700 dark:text-gray-200 mb-4">
                  Through AI-powered analysis and intelligent recommendations, we provide developers 
                  with the tools they need to write more efficient code that consumes less energy and 
                  produces fewer CO₂ emissions.
                </p>
                <p className="text-lg text-gray-700 dark:text-gray-200">
                  Together, we can make software development more sustainable and contribute to a greener future.
                </p>
              </div>
            </FadeInUp>
            <FadeInUp delay={0.2}>
              <div className="rounded-xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2015&q=80" 
                  alt="Sustainable coding" 
                  className="w-full h-auto"
                />
              </div>
            </FadeInUp>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 bg-white dark:bg-slate-800">
        <div className="max-w-6xl mx-auto px-4">
          <FadeInUp>
            <AnimatedHeading level={2} className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-12">
              Our Values
            </AnimatedHeading>
          </FadeInUp>
          <StaggerContainer className="grid md:grid-cols-3 gap-8" staggerDelay={0.15}>
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-slate-700">
                <div className="text-4xl mb-4">🌍</div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Sustainability</h3>
                <p className="text-gray-700 dark:text-gray-200">
                  We're committed to reducing the environmental impact of software development 
                  through innovative technology and best practices.
                </p>
              </div>
            </StaggerItem>
            
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-slate-700">
                <div className="text-4xl mb-4">💡</div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Innovation</h3>
                <p className="text-gray-700 dark:text-gray-200">
                  We leverage cutting-edge AI and machine learning to provide accurate, 
                  actionable insights for code optimization.
                </p>
              </div>
            </StaggerItem>
            
            <StaggerItem>
              <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-slate-700">
                <div className="text-4xl mb-4">🤝</div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Community</h3>
                <p className="text-gray-700 dark:text-gray-200">
                  We believe in building a community of developers who share our vision 
                  of sustainable software development.
                </p>
              </div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-16 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-6xl mx-auto px-4">
          <FadeInUp>
            <AnimatedHeading level={2} className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-12">
              How It Works
            </AnimatedHeading>
          </FadeInUp>
          <StaggerContainer className="grid md:grid-cols-2 gap-8" staggerDelay={0.15}>
            <StaggerItem>
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">1</div>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Submit Your Code</h3>
                  <p className="text-gray-700 dark:text-gray-200">
                    Upload your code files or paste code directly into our platform. 
                    We support multiple programming languages including Python, JavaScript, Java, and C++.
                  </p>
                </div>
              </div>
            </StaggerItem>
            
            <StaggerItem>
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">2</div>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI Analysis</h3>
                  <p className="text-gray-700 dark:text-gray-200">
                    Our advanced AI engine analyzes your code for energy consumption patterns, 
                    complexity, and optimization opportunities.
                  </p>
                </div>
              </div>
            </StaggerItem>
            
            <StaggerItem>
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">3</div>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Get Insights</h3>
                  <p className="text-gray-700 dark:text-gray-200">
                    Receive detailed reports with green scores, energy consumption metrics, 
                    CO₂ emissions, and actionable optimization suggestions.
                  </p>
                </div>
              </div>
            </StaggerItem>
            
            <StaggerItem>
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xl">4</div>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Track Progress</h3>
                  <p className="text-gray-700 dark:text-gray-200">
                    Monitor your improvement over time with comprehensive dashboards, 
                    earn badges, and compete on leaderboards.
                  </p>
                </div>
              </div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>
    </div>
  )
}

export default About
