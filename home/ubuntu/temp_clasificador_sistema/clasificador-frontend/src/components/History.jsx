import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  History as HistoryIcon, 
  Calendar, 
  FileSpreadsheet, 
  Download, 
  Eye, 
  RefreshCw,
  CheckCircle,
  Clock,
  AlertCircle,
  X,
  Play,
  BarChart3
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'

const History = ({ onPlanillaSelect }) => {
  const [planillas, setPlanillas] = useState([])
  const [filteredPlanillas, setFilteredPlanillas] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterEstado, setFilterEstado] = useState('')
  const [sortBy, setSortBy] = useState('fecha_desc')
  const { toast } = useToast()

  useEffect(() => {
    loadPlanillas()
  }, [])

  useEffect(() => {
    applyFilters()
  }, [planillas, searchTerm, filterEstado, sortBy])

  const loadPlanillas = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/clasificador/planillas')
      if (response.ok) {
        const data = await response.json()
        setPlanillas(data)
      } else {
        // Usar datos simulados si la API no está disponible
        const mockData = generateMockPlanillas()
        setPlanillas(mockData)
      }
    } catch (error) {
      console.error('Error loading planillas:', error)
      // Usar datos simulados en caso de error
      const mockData = generateMockPlanillas()
      setPlanillas(mockData)
    } finally {
      setLoading(false)
    }
  }

  const generateMockPlanillas = () => {
    const estados = ['COMPLETADO', 'PROCESANDO', 'ERROR', 'CANCELADO']
    const partidos = ['San Martín', 'José C. Paz', 'Malvinas Argentinas', 'San Miguel']
    
    return Array.from({ length: 15 }, (_, i) => ({
      id: i + 1,
      nombre_archivo: `planilla_${partidos[i % partidos.length].toLowerCase().replace(' ', '_')}_${2024 + Math.floor(i / 5)}_${String(i % 12 + 1).padStart(2, '0')}.xlsx`,
      fecha_subida: new Date(2024, i % 12, Math.floor(Math.random() * 28) + 1).toISOString(),
      partido: partidos[i % partidos.length],
      total_registros: Math.floor(Math.random() * 500) + 50,
      registros_procesados: estados[i % estados.length] === 'COMPLETADO' ? Math.floor(Math.random() * 500) + 50 : Math.floor(Math.random() * 300),
      estado: estados[i % estados.length],
      archivo_resultado: estados[i % estados.length] === 'COMPLETADO' ? `clasificado_planilla_${i + 1}.xlsx` : null,
      observaciones: estados[i % estados.length] === 'ERROR' ? 'Error en la clasificación automática' : null,
      progreso: estados[i % estados.length] === 'COMPLETADO' ? 100 : Math.floor(Math.random() * 80) + 10
    }))
  }

  const applyFilters = () => {
    let filtered = [...planillas]

    // Filtro por búsqueda
    if (searchTerm) {
      filtered = filtered.filter(planilla =>
        planilla.nombre_archivo.toLowerCase().includes(searchTerm.toLowerCase()) ||
        planilla.partido?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filtro por estado
    if (filterEstado) {
      filtered = filtered.filter(planilla => planilla.estado === filterEstado)
    }

    // Ordenamiento
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'fecha_desc':
          return new Date(b.fecha_subida) - new Date(a.fecha_subida)
        case 'fecha_asc':
          return new Date(a.fecha_subida) - new Date(b.fecha_subida)
        case 'nombre_asc':
          return a.nombre_archivo.localeCompare(b.nombre_archivo)
        case 'registros_desc':
          return b.total_registros - a.total_registros
        default:
          return 0
      }
    })

    setFilteredPlanillas(filtered)
  }

  const getEstadoBadge = (estado) => {
    switch (estado) {
      case 'COMPLETADO':
        return <Badge className="bg-green-100 text-green-800"><CheckCircle className="h-3 w-3 mr-1" />Completado</Badge>
      case 'PROCESANDO':
        return <Badge className="bg-blue-100 text-blue-800"><Clock className="h-3 w-3 mr-1" />Procesando</Badge>
      case 'ERROR':
        return <Badge className="bg-red-100 text-red-800"><AlertCircle className="h-3 w-3 mr-1" />Error</Badge>
      case 'CANCELADO':
        return <Badge className="bg-gray-100 text-gray-800"><X className="h-3 w-3 mr-1" />Cancelado</Badge>
      default:
        return <Badge variant="outline">{estado}</Badge>
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleRepeatAnalysis = (planilla) => {
    onPlanillaSelect(planilla)
    toast({
      title: "Planilla seleccionada",
      description: `Se ha seleccionado ${planilla.nombre_archivo} para nuevo análisis`,
    })
  }

  const handleDownload = async (planilla) => {
    if (!planilla.archivo_resultado) {
      toast({
        title: "Error",
        description: "No hay archivo de resultados disponible",
        variant: "destructive"
      })
      return
    }

    try {
      const response = await fetch(`/api/clasificador/generate-excel/${planilla.id}`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = planilla.archivo_resultado
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
        
        toast({
          title: "Descarga iniciada",
          description: "El archivo se está descargando",
        })
      } else {
        throw new Error('Error al descargar el archivo')
      }
    } catch (error) {
      toast({
        title: "Error en la descarga",
        description: error.message,
        variant: "destructive"
      })
    }
  }

  const handleViewResults = (planilla) => {
    onPlanillaSelect(planilla)
    // Navegar a resultados
    window.location.href = '/results'
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Historial de Planillas
            </h1>
            <p className="text-lg text-gray-600">
              Gestiona y revisa todas las planillas procesadas
            </p>
          </div>
          <Button 
            onClick={loadPlanillas}
            disabled={loading}
            variant="outline"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Actualizar
          </Button>
        </div>
      </motion.div>

      {/* Filtros */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Filtros y Búsqueda</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Input
                placeholder="Buscar por nombre o partido..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              
              <Select value={filterEstado} onValueChange={setFilterEstado}>
                <SelectTrigger>
                  <SelectValue placeholder="Filtrar por estado" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos los estados</SelectItem>
                  <SelectItem value="COMPLETADO">Completado</SelectItem>
                  <SelectItem value="PROCESANDO">Procesando</SelectItem>
                  <SelectItem value="ERROR">Error</SelectItem>
                  <SelectItem value="CANCELADO">Cancelado</SelectItem>
                </SelectContent>
              </Select>

              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger>
                  <SelectValue placeholder="Ordenar por" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="fecha_desc">Fecha (más reciente)</SelectItem>
                  <SelectItem value="fecha_asc">Fecha (más antiguo)</SelectItem>
                  <SelectItem value="nombre_asc">Nombre (A-Z)</SelectItem>
                  <SelectItem value="registros_desc">Más registros</SelectItem>
                </SelectContent>
              </Select>

              <Button 
                variant="outline" 
                onClick={() => {
                  setSearchTerm('')
                  setFilterEstado('')
                  setSortBy('fecha_desc')
                }}
              >
                Limpiar
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Timeline de planillas */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <HistoryIcon className="h-5 w-5" />
              <span>Timeline de Procesamiento</span>
              <Badge variant="outline">{filteredPlanillas.length} planillas</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <RefreshCw className="h-6 w-6 animate-spin mr-2" />
                <span>Cargando historial...</span>
              </div>
            ) : filteredPlanillas.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No se encontraron planillas que coincidan con los filtros
              </div>
            ) : (
              <div className="space-y-4">
                {filteredPlanillas.map((planilla, index) => (
                  <motion.div
                    key={planilla.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                    className="flex items-center space-x-4 p-4 border rounded-lg hover:shadow-md transition-shadow"
                  >
                    {/* Timeline indicator */}
                    <div className="flex flex-col items-center">
                      <div className={`w-3 h-3 rounded-full ${
                        planilla.estado === 'COMPLETADO' ? 'bg-green-500' :
                        planilla.estado === 'PROCESANDO' ? 'bg-blue-500' :
                        planilla.estado === 'ERROR' ? 'bg-red-500' : 'bg-gray-500'
                      }`} />
                      {index < filteredPlanillas.length - 1 && (
                        <div className="w-px h-8 bg-gray-200 mt-2" />
                      )}
                    </div>

                    {/* Contenido principal */}
                    <div className="flex-1 grid grid-cols-1 md:grid-cols-6 gap-4 items-center">
                      {/* Información del archivo */}
                      <div className="md:col-span-2">
                        <div className="flex items-center space-x-2 mb-1">
                          <FileSpreadsheet className="h-4 w-4 text-blue-600" />
                          <span className="font-medium text-sm">{planilla.nombre_archivo}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <Calendar className="h-3 w-3" />
                          <span>{formatDate(planilla.fecha_subida)}</span>
                        </div>
                        {planilla.partido && (
                          <Badge variant="outline" className="mt-1 text-xs">
                            {planilla.partido}
                          </Badge>
                        )}
                      </div>

                      {/* Estado */}
                      <div>
                        {getEstadoBadge(planilla.estado)}
                      </div>

                      {/* Progreso */}
                      <div className="text-center">
                        <div className="text-sm font-medium">
                          {planilla.registros_procesados.toLocaleString()} / {planilla.total_registros.toLocaleString()}
                        </div>
                        <div className="text-xs text-gray-500">registros</div>
                        {planilla.estado === 'PROCESANDO' && (
                          <div className="w-full bg-gray-200 rounded-full h-1 mt-1">
                            <div 
                              className="bg-blue-600 h-1 rounded-full transition-all duration-300"
                              style={{ width: `${planilla.progreso}%` }}
                            />
                          </div>
                        )}
                      </div>

                      {/* Observaciones */}
                      <div className="text-xs text-gray-500">
                        {planilla.observaciones || 'Sin observaciones'}
                      </div>

                      {/* Acciones */}
                      <div className="flex space-x-2">
                        {planilla.estado === 'COMPLETADO' && (
                          <>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleViewResults(planilla)}
                              title="Ver resultados"
                            >
                              <Eye className="h-3 w-3" />
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleDownload(planilla)}
                              title="Descargar Excel"
                            >
                              <Download className="h-3 w-3" />
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleRepeatAnalysis(planilla)}
                              title="Repetir análisis"
                            >
                              <Play className="h-3 w-3" />
                            </Button>
                          </>
                        )}
                        {planilla.estado === 'PROCESANDO' && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleViewResults(planilla)}
                            title="Ver progreso"
                          >
                            <BarChart3 className="h-3 w-3" />
                          </Button>
                        )}
                        {(planilla.estado === 'ERROR' || planilla.estado === 'CANCELADO') && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleRepeatAnalysis(planilla)}
                            title="Reintentar"
                          >
                            <RefreshCw className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Estadísticas del historial */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-4 gap-6"
      >
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Planillas</CardTitle>
            <FileSpreadsheet className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{planillas.length}</div>
            <p className="text-xs text-muted-foreground">archivos procesados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completadas</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {planillas.filter(p => p.estado === 'COMPLETADO').length}
            </div>
            <p className="text-xs text-muted-foreground">exitosamente</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">En Proceso</CardTitle>
            <Clock className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {planillas.filter(p => p.estado === 'PROCESANDO').length}
            </div>
            <p className="text-xs text-muted-foreground">actualmente</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Registros</CardTitle>
            <BarChart3 className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {planillas.reduce((sum, p) => sum + p.registros_procesados, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">clasificados</p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

export default History

