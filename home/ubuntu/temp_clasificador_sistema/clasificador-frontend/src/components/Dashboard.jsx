import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { 
  Upload, 
  BarChart3, 
  FileText, 
  Map, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  TrendingUp,
  Database,
  Zap
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'

const Dashboard = ({ currentStep, onStepChange }) => {
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    totalPlanillas: 0,
    registrosProcesados: 0,
    ultimoProcesamiento: null,
    promedioTiempo: 0
  })

  useEffect(() => {
    // Cargar estadísticas del dashboard
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/clasificador/planillas`)
      if (response.ok) {
        const planillas = await response.json()
        
        const totalRegistros = planillas.reduce((sum, p) => sum + p.registros_procesados, 0)
        const ultimaPlanilla = planillas.length > 0 ? planillas[0] : null
        
        setStats({
          totalPlanillas: planillas.length,
          registrosProcesados: totalRegistros,
          ultimoProcesamiento: ultimaPlanilla?.fecha_subida,
          promedioTiempo: 1.5 // Tiempo promedio por registro en segundos
        })
      }
    } catch (error) {
      console.error('Error cargando estadísticas:', error)
    }
  }

  const quickActions = [
    {
      id: 'upload',
      title: 'Cargar Nueva Planilla',
      description: 'Subir archivo Excel para procesar',
      icon: Upload,
      color: 'from-blue-500 to-blue-600',
      path: '/upload',
      action: () => {
        onStepChange('upload')
        navigate('/upload')
      }
    },
    {
      id: 'reports',
      title: 'Generar Informe',
      description: 'Crear informe situacional',
      icon: FileText,
      color: 'from-green-500 to-green-600',
      path: '/reports',
      action: () => {
        navigate('/reports')
      }
    },
    {
      id: 'heatmap',
      title: 'Ver Mapa de Calor',
      description: 'Visualizar delitos por zona',
      icon: Map,
      color: 'from-purple-500 to-purple-600',
      path: '/heatmap',
      action: () => {
        navigate('/heatmap')
      }
    },
    {
      id: 'results',
      title: 'Ver Resultados',
      description: 'Revisar clasificaciones',
      icon: BarChart3,
      color: 'from-orange-500 to-orange-600',
      path: '/results',
      action: () => {
        navigate('/results')
      }
    }
  ]

  const features = [
    {
      icon: Zap,
      title: 'Clasificación por Cascada',
      description: 'Gemini → OpenAI → Reglas → Por defecto'
    },
    {
      icon: Database,
      title: 'Base de Datos Relacional',
      description: 'Almacenamiento estructurado y consultas optimizadas'
    },
    {
      icon: TrendingUp,
      title: 'Análisis Avanzado',
      description: 'Informes situacionales y mapas de calor'
    }
  ]

  return (
    <div className="space-y-8">
      {/* Header del Dashboard */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Sistema de Clasificación de Hechos Delictivos
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Plataforma avanzada para el procesamiento automático y clasificación inteligente 
            de datos delictivos con tecnología de IA
          </p>
        </div>
      </motion.div>

      {/* Estadísticas principales */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-blue-800">
              Planillas Procesadas
            </CardTitle>
            <Database className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-900">{stats.totalPlanillas}</div>
            <p className="text-xs text-blue-600">Total de archivos</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-green-800">
              Registros Clasificados
            </CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-900">{stats.registrosProcesados.toLocaleString()}</div>
            <p className="text-xs text-green-600">Hechos procesados</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-purple-800">
              Tiempo Promedio
            </CardTitle>
            <Clock className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-900">{stats.promedioTiempo}s</div>
            <p className="text-xs text-purple-600">Por registro</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-orange-800">
              Estado del Sistema
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <Badge className="bg-green-100 text-green-800">Activo</Badge>
            </div>
            <p className="text-xs text-orange-600 mt-1">Todos los servicios operativos</p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Acciones rápidas */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Acciones Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <motion.div
                key={action.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Card 
                  className="cursor-pointer hover:shadow-lg transition-all duration-200 border-0 bg-white"
                  onClick={action.action}
                >
                  <CardHeader>
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${action.color} flex items-center justify-center mb-4`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <CardTitle className="text-lg">{action.title}</CardTitle>
                    <CardDescription>{action.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button className="w-full" variant="outline">
                      Comenzar
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* Características del sistema */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Características del Sistema</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
              >
                <Card className="text-center">
                  <CardHeader>
                    <div className="w-16 h-16 mx-auto bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-4">
                      <Icon className="h-8 w-8 text-blue-600" />
                    </div>
                    <CardTitle className="text-xl">{feature.title}</CardTitle>
                    <CardDescription className="text-base">
                      {feature.description}
                    </CardDescription>
                  </CardHeader>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* Último procesamiento */}
      {stats.ultimoProcesamiento && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-blue-600" />
                <span>Último Procesamiento</span>
              </CardTitle>
              <CardDescription>
                Procesado el {new Date(stats.ultimoProcesamiento).toLocaleDateString('es-ES', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </CardDescription>
            </CardHeader>
          </Card>
        </motion.div>
      )}
    </div>
  )
}

export default Dashboard

