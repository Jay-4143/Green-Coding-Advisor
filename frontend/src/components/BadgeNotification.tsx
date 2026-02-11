import React, { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import confetti from 'canvas-confetti'

interface Badge {
    name: string
    description: string
    icon: string
}

interface BadgeNotificationProps {
    badge: Badge | null
    onClose: () => void
}

const BadgeNotification: React.FC<BadgeNotificationProps> = ({ badge, onClose }) => {
    useEffect(() => {
        if (badge) {
            // Trigger confetti
            const duration = 3000
            const end = Date.now() + duration

            const frame = () => {
                confetti({
                    particleCount: 2,
                    angle: 60,
                    spread: 55,
                    origin: { x: 0 },
                    colors: ['#10B981', '#3B82F6', '#F59E0B']
                })
                confetti({
                    particleCount: 2,
                    angle: 120,
                    spread: 55,
                    origin: { x: 1 },
                    colors: ['#10B981', '#3B82F6', '#F59E0B']
                })

                if (Date.now() < end) {
                    requestAnimationFrame(frame)
                }
            }
            frame()

            // Auto close after 5 seconds
            const timer = setTimeout(() => {
                onClose()
            }, 5000)

            return () => clearTimeout(timer)
        }
    }, [badge, onClose])

    return (
        <AnimatePresence>
            {badge && (
                <div className="fixed inset-0 flex items-center justify-center z-[100] pointer-events-none">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.5, y: 50 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.8, y: -50 }}
                        transition={{ type: "spring", stiffness: 300, damping: 25 }}
                        className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-8 max-w-sm w-full mx-4 border-2 border-green-500 pointer-events-auto relative overflow-hidden"
                    >
                        {/* Background decorative elements */}
                        <div className="absolute -top-10 -right-10 w-32 h-32 bg-green-100 dark:bg-green-900/20 rounded-full blur-2xl"></div>
                        <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-blue-100 dark:bg-blue-900/20 rounded-full blur-2xl"></div>

                        <div className="relative text-center">
                            <motion.div
                                initial={{ rotate: -180, scale: 0 }}
                                animate={{ rotate: 0, scale: 1 }}
                                transition={{ type: "spring", delay: 0.2 }}
                                className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-green-100 to-emerald-200 dark:from-green-900/40 dark:to-emerald-800/40 rounded-full flex items-center justify-center shadow-inner"
                            >
                                <span className="text-5xl">{badge.icon}</span>
                            </motion.div>

                            <motion.h3
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.3 }}
                                className="text-2xl font-bold text-gray-900 dark:text-white mb-2"
                            >
                                New Badge Unlocked!
                            </motion.h3>

                            <motion.p
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.4 }}
                                className="text-lg font-semibold text-green-600 dark:text-green-400 mb-2"
                            >
                                {badge.name}
                            </motion.p>

                            <motion.p
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.5 }}
                                className="text-gray-600 dark:text-gray-300 mb-6"
                            >
                                {badge.description}
                            </motion.p>

                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={onClose}
                                className="px-6 py-2 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-full font-semibold shadow-lg hover:shadow-xl transition-shadow"
                            >
                                Awesome!
                            </motion.button>
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    )
}

export default BadgeNotification
