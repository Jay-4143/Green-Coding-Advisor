import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
    FadeInUp,
    AnimatedHeading,
    StaggerContainer,
    StaggerItem,
} from './animations'

const Journey: React.FC = () => {
    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900 pt-16">
            {/* Hero Section */}
            <section className="relative py-20 bg-emerald-900 overflow-hidden">
                <div className="absolute inset-0 opacity-20">
                    <img
                        src="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=2813&q=80"
                        alt="Forest path"
                        className="w-full h-full object-cover"
                    />
                </div>
                <div className="relative max-w-7xl mx-auto px-4 text-center">
                    <FadeInUp>
                        <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
                            Your Green Coding Journey
                        </h1>
                        <p className="text-xl text-emerald-100 max-w-3xl mx-auto">
                            Every line of code has an impact. Discover how you can become a sustainable software engineer and contribute to a greener planet.
                        </p>
                    </FadeInUp>
                </div>
            </section>

            {/* The Path */}
            <section className="py-20">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="relative">
                        {/* Connecting Line */}
                        <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-emerald-200 dark:bg-emerald-900 hidden md:block"></div>

                        <StaggerContainer className="space-y-24" staggerDelay={0.2}>
                            {/* Step 1 */}
                            <StaggerItem>
                                <div className="relative flex items-center justify-between md:flex-row flex-col">
                                    <div className="md:w-5/12 text-right order-1 md:order-1 pr-8">
                                        <h3 className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">1. Awareness</h3>
                                        <p className="text-lg text-gray-700 dark:text-gray-300">
                                            Understand that digital products consume electricity and emit CO2. Your first step is simply recognizing that software has an environmental cost.
                                        </p>
                                    </div>
                                    <div className="absolute left-1/2 transform -translate-x-1/2 w-12 h-12 bg-emerald-500 rounded-full border-4 border-white dark:border-slate-800 flex items-center justify-center z-10 order-2 md:order-2">
                                        <span className="text-white font-bold">1</span>
                                    </div>
                                    <div className="md:w-5/12 pl-8 order-3 md:order-3"></div>
                                </div>
                            </StaggerItem>

                            {/* Step 2 */}
                            <StaggerItem>
                                <div className="relative flex items-center justify-between md:flex-row flex-col">
                                    <div className="md:w-5/12 text-right order-1 md:order-1 pr-8"></div>
                                    <div className="absolute left-1/2 transform -translate-x-1/2 w-12 h-12 bg-blue-500 rounded-full border-4 border-white dark:border-slate-800 flex items-center justify-center z-10 order-2 md:order-2">
                                        <span className="text-white font-bold">2</span>
                                    </div>
                                    <div className="md:w-5/12 pl-8 order-3 md:order-3">
                                        <h3 className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">2. Measurement</h3>
                                        <p className="text-lg text-gray-700 dark:text-gray-300">
                                            You can't improve what you don't measure. Use our tools to analyze your code's carbon footprint and energy consumption.
                                        </p>
                                    </div>
                                </div>
                            </StaggerItem>

                            {/* Step 3 */}
                            <StaggerItem>
                                <div className="relative flex items-center justify-between md:flex-row flex-col">
                                    <div className="md:w-5/12 text-right order-1 md:order-1 pr-8">
                                        <h3 className="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-2">3. Optimization</h3>
                                        <p className="text-lg text-gray-700 dark:text-gray-300">
                                            Apply efficient algorithms, reduce bloat, and optimize resource usage. Our AI advisor provides actionable tips to reduce your impact.
                                        </p>
                                    </div>
                                    <div className="absolute left-1/2 transform -translate-x-1/2 w-12 h-12 bg-purple-500 rounded-full border-4 border-white dark:border-slate-800 flex items-center justify-center z-10 order-2 md:order-2">
                                        <span className="text-white font-bold">3</span>
                                    </div>
                                    <div className="md:w-5/12 pl-8 order-3 md:order-3"></div>
                                </div>
                            </StaggerItem>

                            {/* Step 4 */}
                            <StaggerItem>
                                <div className="relative flex items-center justify-between md:flex-row flex-col">
                                    <div className="md:w-5/12 text-right order-1 md:order-1 pr-8"></div>
                                    <div className="absolute left-1/2 transform -translate-x-1/2 w-12 h-12 bg-orange-500 rounded-full border-4 border-white dark:border-slate-800 flex items-center justify-center z-10 order-2 md:order-2">
                                        <span className="text-white font-bold">4</span>
                                    </div>
                                    <div className="md:w-5/12 pl-8 order-3 md:order-3">
                                        <h3 className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-2">4. Advocacy</h3>
                                        <p className="text-lg text-gray-700 dark:text-gray-300">
                                            Share your knowledge. Lead by example. Encourage your team and organization to adopt green coding practices.
                                        </p>
                                    </div>
                                </div>
                            </StaggerItem>
                        </StaggerContainer>
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-20 bg-gray-900 text-white text-center">
                <div className="max-w-4xl mx-auto px-4">
                    <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to take the first step?</h2>
                    <p className="text-lg text-gray-300 mb-8">
                        Join our community and start making a difference today.
                    </p>
                    <Link
                        to="/submit"
                        className="inline-block px-10 py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold text-lg transition-colors"
                    >
                        Submit Your Code
                    </Link>
                </div>
            </section>
        </div>
    )
}

export default Journey
