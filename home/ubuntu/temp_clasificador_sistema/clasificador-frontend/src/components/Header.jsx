import { useState } from 'react'
import { motion } from 'framer-motion'
import { Menu, X, Shield, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const Header = ({ sidebarOpen, setSidebarOpen, currentStep, steps }) => {
  const getCurrentStepIndex = () => {
    return steps.findIndex(step => step.id === currentStep)
  }

  const getStepStatus = (stepIndex, currentIndex) => {
    if (stepIndex < currentIndex) return 'completed'
    if (stepIndex === currentIndex) return 'current'
    return 'pending'
  }

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo y título */}
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden mr-2"
            >
              {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
            
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Sistema de Clasificación
                </h1>
                <p className="text-sm text-gray-500 hidden sm:block">
                  Hechos Delictivos
                </p>
              </div>
            </div>
          </div>

          {/* Breadcrumb de pasos */}
          <div className="hidden md:flex items-center space-x-2">
            {steps.map((step, index) => {
              const currentIndex = getCurrentStepIndex()
              const status = getStepStatus(index, currentIndex)
              
              return (
                <div key={step.id} className="flex items-center">
                  <motion.div
                    className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-200 ${
                      status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : status === 'current'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <span className="text-base">{step.icon}</span>
                    <span>{step.name}</span>
                    {status === 'completed' && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-2 h-2 bg-green-500 rounded-full"
                      />
                    )}
                  </motion.div>
                  
                  {index < steps.length - 1 && (
                    <ChevronRight className="h-4 w-4 text-gray-400 mx-1" />
                  )}
                </div>
              )
            })}
          </div>

          {/* Estado actual en móvil */}
          <div className="md:hidden">
            <Badge variant="outline" className="bg-blue-50 text-blue-700">
              {steps.find(s => s.id === currentStep)?.name || 'Inicio'}
            </Badge>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

