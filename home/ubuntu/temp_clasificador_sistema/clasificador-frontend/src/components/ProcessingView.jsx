import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Play, 
  Pause, 
  Square, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Zap,
  Database,
  Brain,
  Settings,
  BarChart3
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useToast } from '@/hooks/use-toast'

const ProcessingView = ({ planilla, onProcessingStart, onProcessingComplete, processingData }) => {
  const [processing, setProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStatus, setCurrentStatus] = useState('Listo para procesar')
  const [timeElapsed, setTimeElapsed] = useState(0)
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [processedRows, setProcessedRows] = useState(0)
  const [totalRows, setTotalRows] = useState(0)
  const [currentMethod, setCurrentMethod] = useState('')
  const [error, setError] = useState(null)
  
  const intervalRef = useRef(null)
  const statusIntervalRef = useRef(null)
  const { toast } = useToast()

  useEffect(() => {
    if (planilla) {
      setTotalRows(planilla.total_filas || 0)
    }
  }, [planilla])

  useEffect(() => {
    if (processing) {
      // Timer para tiempo transcurrido
      intervalRef.current = setInterval(() => {
        setTimeElapsed(prev => prev + 1)
      }, 1000)

      // Polling para estado del procesamiento
      statusIntervalRef.current = setInterval(() => {
        checkProcessingStatus()
      }, 2000)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
      if (statusIntervalRef.current) {
        clearInterval(statusIntervalRef.current)
      }
    }

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
      if (statusIntervalRef.current) clearInterval(statusIntervalRef.current)
    }
  }, [processing, planilla])

  const checkProcessingStatus = async () => {
    if (!planilla?.planilla_id) return

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/clasificador/status/${planilla.planilla_id}`)
      if (response.ok) {
        const status = await response.json()
        
        setProcessedRows(status.registros_procesados)
        setProgress(status.progreso)
        setTimeRemaining(status.tiempo_estimado || 0)
        
        // Actualizar estado basado en progreso
        if (status.estado === 'COMPLETADO') {
          setProcessing(false)
          setCurrentStatus('Procesamiento completado')
          setCurrentMethod('COMPLETADO')
          onProcessingComplete()
          toast({
            title: "Procesamiento completado",
            description: `Se procesaron ${status.registros_procesados} registros exitosamente`,
          })
        } else if (status.estado === 'CANCELADO') {
          setProcessing(false)
          setCurrentStatus('Proceso cancelado por el usuario')
          setCurrentMethod('CANCELADO')
        } else if (status.estado === 'ERROR') {
          setProcessing(false)
          setCurrentStatus('Error en el procesamiento')
          setCurrentMethod('ERROR')
          setError('Ocurrió un error durante el procesamiento')
        } else if (status.estado === 'PROCESANDO') {
          // Determinar método actual basado en progreso
          const progressPercent = status.progreso
          if (progressPercent < 25) {
            setCurrentStatus('Subiendo archivo...')
            setCurrentMethod('UPLOAD')
          } else if (progressPercent < 50) {
            setCurrentStatus('Procesando filas...')
            setCurrentMethod('GEMINI')
          } else if (progressPercent < 75) {
            setCurrentStatus('Clasificando con IA...')
            setCurrentMethod('OPENAI')
          } else if (progressPercent < 95) {
            setCurrentStatus('Aplicando reglas...')
            setCurrentMethod('REGLAS')
          } else {
            setCurrentStatus('Guardando resultados...')
            setCurrentMethod('SAVING')
          }
        }
      }
    } catch (err) {
      console.error('Error checking status:', err)
    }
  }

  const startProcessing = async () => {
    if (!planilla?.planilla_id) {
      toast({
        title: "Error",
        description: "No hay planilla para procesar",
        variant: "destructive"
      })
      return
    }

    setProcessing(true)
    setProgress(0)
    setTimeElapsed(0)
    setProcessedRows(0)
    setCurrentStatus('Iniciando procesamiento...')
    setCurrentMethod('INIT')
    setError(null)

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/clasificador/process/${planilla.planilla_id}`, {
        method: 'POST'
      })

      if (response.ok) {
        const result = await response.json()
        onProcessingStart(result)
        toast({
          title: "Procesamiento iniciado",
          description: "El archivo se está procesando en segundo plano",
        })
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Error iniciando procesamiento')
      }
    } catch (err) {
      setProcessing(false)
      setError(err.message)
      toast({
        title: "Error al iniciar procesamiento",
        description: err.message,
        variant: "destructive"
      })
    }
  }

  const cancelProcessing = async () => {
    if (!planilla?.planilla_id) return

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/clasificador/cancel/${planilla.planilla_id}`, {
        method: 'POST'
      })

      if (response.ok) {
        setProcessing(false)
        setCurrentStatus('El proceso fue cancelado por el usuario.')
        setCurrentMethod('CANCELADO')
        toast({
          title: "Proceso cancelado",
          description: "El procesamiento ha sido detenido",
        })
      }
    } catch (err) {
      console.error('Error canceling process:', err)
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getMethodIcon = (method) => {
    switch (method) {
      case 'GEMINI': return <Brain className="h-4 w-4" />
      case 'OPENAI': return <Zap className="h-4 w-4" />
      case 'REGLAS': return <Settings className="h-4 w-4" />
      case 'SAVING': return <Database className="h-4 w-4" />
      case 'COMPLETADO': return <CheckCircle className="h-4 w-4" />
      case 'CANCELADO': return <Square className="h-4 w-4" />
      case 'ERROR': return <AlertCircle className="h-4 w-4" />
      default: return <Clock className="h-4 w-4" />
    }
  }

  const getMethodColor = (method) => {
    switch (method) {
      case 'GEMINI': return 'bg-blue-100 text-blue-800'
      case 'OPENAI': return 'bg-green-100 text-green-800'
      case 'REGLAS': return 'bg-orange-100 text-orange-800'
      case 'SAVING': return 'bg-purple-100 text-purple-800'
      case 'COMPLETADO': return 'bg-green-100 text-green-800'
      case 'CANCELADO': return 'bg-gray-100 text-gray-800'
      case 'ERROR': return 'bg-red-100 text-red-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  if (!planilla) {
    return (
      <div className="max-w-4xl mx-auto">
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            No hay planilla cargada. Por favor, sube un archivo primero.
          </AlertDescription>
        </Alert>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Procesamiento de Datos
          </h1>
          <p className="text-lg text-gray-600">
            Clasificación automática con sistema de cascada IA
          </p>
        </div>
      </motion.div>

      {/* Información de la planilla */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Archivo a Procesar</CardTitle>
            <CardDescription>Información del archivo cargado</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-500">Nombre del archivo</div>
                <div className="font-medium">{planilla.filename}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Total de registros</div>
                <div className="font-medium">{totalRows.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Tiempo estimado</div>
                <div className="font-medium">{formatTime(Math.ceil(totalRows * 1.5))}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Controles de procesamiento */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>Control de Procesamiento</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Button
                  onClick={startProcessing}
                  disabled={processing}
                  className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
                >
                  <Play className="h-4 w-4 mr-2" />
                  {processing ? 'Procesando...' : 'Iniciar Procesamiento'}
                </Button>
                
                {processing && (
                  <Button
                    onClick={cancelProcessing}
                    variant="destructive"
                  >
                    <Square className="h-4 w-4 mr-2" />
                    Cancelar Proceso
                  </Button>
                )}
              </div>

              <div className="flex items-center space-x-2">
                <Badge className={getMethodColor(currentMethod)}>
                  {getMethodIcon(currentMethod)}
                  <span className="ml-1">{currentMethod || 'LISTO'}</span>
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Progreso del procesamiento */}
      <AnimatePresence>
        {(processing || progress > 0) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <span>Progreso del Procesamiento</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Barra de progreso principal */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{currentStatus}</span>
                    <span>{Math.round(progress)}%</span>
                  </div>
                  <Progress value={progress} className="h-3" />
                </div>

                {/* Estadísticas */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {processedRows.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Procesados</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {(totalRows - processedRows).toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Restantes</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {formatTime(timeElapsed)}
                    </div>
                    <div className="text-sm text-gray-600">Transcurrido</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {formatTime(timeRemaining)}
                    </div>
                    <div className="text-sm text-gray-600">Restante</div>
                  </div>
                </div>

                {/* Velocidad de procesamiento */}
                {processing && timeElapsed > 0 && (
                  <div className="text-center">
                    <div className="text-sm text-gray-600">
                      Velocidad: {(processedRows / timeElapsed).toFixed(1)} registros/segundo
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Información del sistema de cascada */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Sistema de Clasificación por Cascada</CardTitle>
            <CardDescription>
              El sistema utiliza múltiples métodos para garantizar la clasificación de todos los registros
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <Brain className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                <div className="font-medium text-blue-900">1. Gemini AI</div>
                <div className="text-xs text-blue-600">Clasificación principal</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <Zap className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <div className="font-medium text-green-900">2. OpenAI</div>
                <div className="text-xs text-green-600">Alternativa robusta</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <Settings className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                <div className="font-medium text-orange-900">3. Reglas</div>
                <div className="text-xs text-orange-600">Clasificación básica</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <Database className="h-8 w-8 text-gray-600 mx-auto mb-2" />
                <div className="font-medium text-gray-900">4. Por Defecto</div>
                <div className="text-xs text-gray-600">Valores seguros</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

export default ProcessingView

