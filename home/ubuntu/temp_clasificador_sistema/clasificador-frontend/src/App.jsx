import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Toaster } from '@/components/ui/toaster'
import './App.css'

// Componentes principales
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'
import FileUpload from './components/FileUpload'
import ProcessingView from './components/ProcessingView'
import Results from './components/Results'
import Reports from './components/Reports'
import HeatMap from './components/HeatMap'
import History from './components/History'

function App() {
  const [currentStep, setCurrentStep] = useState('upload')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [currentPlanilla, setCurrentPlanilla] = useState(null)
  const [processingData, setProcessingData] = useState(null)

  // Pasos del breadcrumb
  const steps = [
    { id: 'upload', name: 'Cargar', icon: '📁' },
    { id: 'process', name: 'Procesar', icon: '⚙️' },
    { id: 'results', name: 'Resultados', icon: '📊' },
    { id: 'download', name: 'Descargar', icon: '⬇️' }
  ]

  const handleStepChange = (step) => {
    setCurrentStep(step)
  }

  const handleFileUploaded = (planillaData) => {
    setCurrentPlanilla(planillaData)
    setCurrentStep('process')
  }

  const handleProcessingStart = (data) => {
    setProcessingData(data)
    setCurrentStep('processing')
  }

  const handleProcessingComplete = () => {
    setCurrentStep('results')
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Header 
          sidebarOpen={sidebarOpen} 
          setSidebarOpen={setSidebarOpen}
          currentStep={currentStep}
          steps={steps}
        />
        
        <div className="flex">
          <Sidebar 
            open={sidebarOpen} 
            setOpen={setSidebarOpen}
            currentStep={currentStep}
            onStepChange={handleStepChange}
          />
          
          <main className="flex-1 p-6 lg:ml-64">
            <div className="max-w-7xl mx-auto">
              <AnimatePresence mode="wait">
                <Routes>
                  <Route 
                    path="/" 
                    element={
                      <motion.div
                        key="dashboard"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Dashboard 
                          currentStep={currentStep}
                          onStepChange={handleStepChange}
                        />
                      </motion.div>
                    } 
                  />
                  
                  <Route 
                    path="/upload" 
                    element={
                      <motion.div
                        key="upload"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <FileUpload 
                          onFileUploaded={handleFileUploaded}
                          currentPlanilla={currentPlanilla}
                        />
                      </motion.div>
                    } 
                  />
                  
                  <Route 
                    path="/process" 
                    element={
                      <motion.div
                        key="process"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <ProcessingView 
                          planilla={currentPlanilla}
                          onProcessingStart={handleProcessingStart}
                          onProcessingComplete={handleProcessingComplete}
                          processingData={processingData}
                        />
                      </motion.div>
                    } 
                  />
                  
                  <Route 
                    path="/results" 
                    element={
                      <motion.div
                        key="results"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Results 
                          planilla={currentPlanilla}
                        />
                      </motion.div>
                    } 
                  />
                  
                  <Route 
                    path="/reports" 
                    element={
                      <motion.div
                        key="reports"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Reports />
                      </motion.div>
                    } 
                  />
                  
                  <Route 
                    path="/heatmap" 
                    element={
                      <motion.div
                        key="heatmap"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <HeatMap />
                      </motion.div>
                    } 
                  />
                  
                  <Route 
                    path="/history" 
                    element={
                      <motion.div
                        key="history"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <History 
                          onPlanillaSelect={setCurrentPlanilla}
                        />
                      </motion.div>
                    } 
                  />
                </Routes>
              </AnimatePresence>
            </div>
          </main>
        </div>
        
        <Toaster />
      </div>
    </Router>
  )
}

export default App

