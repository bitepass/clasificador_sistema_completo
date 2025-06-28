import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Download, 
  Eye, 
  Filter, 
  Search, 
  BarChart3, 
  PieChart, 
  FileSpreadsheet,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useToast } from '@/hooks/use-toast'

const Results = ({ planilla }) => {
  const [results, setResults] = useState([])
  const [filteredResults, setFilteredResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterCalificacion, setFilterCalificacion] = useState('')
  const [filterJurisdiccion, setFilterJurisdiccion] = useState('')
  const [stats, setStats] = useState({})
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage] = useState(10)
  const { toast } = useToast()

  useEffect(() => {
    if (planilla?.planilla_id) {
      loadResults()
    }
  }, [planilla])

  useEffect(() => {
    applyFilters()
  }, [results, searchTerm, filterCalificacion, filterJurisdiccion])

  const loadResults = async () => {
    setLoading(true)
    try {
      // Simular carga de resultados desde la API
      // En implementación real, esto vendría de /api/clasificador/results/{planilla_id}
      const mockResults = generateMockResults()
      setResults(mockResults)
      calculateStats(mockResults)
    } catch (error) {
      console.error('Error loading results:', error)
      toast({
        title: "Error",
        description: "No se pudieron cargar los resultados",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const generateMockResults = () => {
    const calificaciones = [
      'ROBO_SIMPLE', 'ROBO_ASALTO_VIA_PUBLICA', 'HOMICIDIO_SIMPLE', 
      'LESIONES_ARMA_FUEGO', 'SUSTRACCION_AUTOMOTOR_LEVANTAMIENTO'
    ]
    const jurisdicciones = ['URBANA', 'RURAL', 'MIXTA']
    const metodos = ['GEMINI', 'OPENAI', 'REGLAS', 'DEFECTO']
    
    return Array.from({ length: planilla?.total_filas || 50 }, (_, i) => ({
      id: i + 1,
      id_hecho: `H${(i + 1).toString().padStart(4, '0')}`,
      nro_registro: `R${(i + 1).toString().padStart(6, '0')}`,
      fecha_hecho: new Date(2024, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28) + 1).toISOString().split('T')[0],
      calificacion: calificaciones[Math.floor(Math.random() * calificaciones.length)],
      jurisdiccion: jurisdicciones[Math.floor(Math.random() * jurisdicciones.length)],
      modalidad: 'MODALIDAD_' + calificaciones[Math.floor(Math.random() * calificaciones.length)],
      victimas: Math.random() > 0.5 ? 'FEMENINO' : 'MASCULINO',
      armas: Math.random() > 0.7 ? 'FUEGO' : Math.random() > 0.5 ? 'BLANCA' : 'NINGUNA',
      lugar: Math.random() > 0.6 ? 'VIA_PUBLICA' : Math.random() > 0.3 ? 'FINCA' : 'COMERCIO',
      metodo_clasificacion: metodos[Math.floor(Math.random() * metodos.length)],
      confianza: (Math.random() * 0.4 + 0.6).toFixed(2),
      tiempo_procesamiento: Math.floor(Math.random() * 3000) + 500
    }))
  }

  const calculateStats = (data) => {
    const stats = {
      total: data.length,
      porCalificacion: {},
      porJurisdiccion: {},
      porMetodo: {},
      tiempoPromedio: 0
    }

    data.forEach(item => {
      // Por calificación
      stats.porCalificacion[item.calificacion] = (stats.porCalificacion[item.calificacion] || 0) + 1
      
      // Por jurisdicción
      stats.porJurisdiccion[item.jurisdiccion] = (stats.porJurisdiccion[item.jurisdiccion] || 0) + 1
      
      // Por método
      stats.porMetodo[item.metodo_clasificacion] = (stats.porMetodo[item.metodo_clasificacion] || 0) + 1
      
      // Tiempo promedio
      stats.tiempoPromedio += item.tiempo_procesamiento
    })

    stats.tiempoPromedio = Math.round(stats.tiempoPromedio / data.length)
    setStats(stats)
  }

  const applyFilters = () => {
    let filtered = results

    if (searchTerm) {
      filtered = filtered.filter(item => 
        item.id_hecho.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.nro_registro.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.calificacion.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (filterCalificacion) {
      filtered = filtered.filter(item => item.calificacion === filterCalificacion)
    }

    if (filterJurisdiccion) {
      filtered = filtered.filter(item => item.jurisdiccion === filterJurisdiccion)
    }

    setFilteredResults(filtered)
    setCurrentPage(1)
  }

  const downloadExcel = async () => {
    if (!planilla?.planilla_id) {
      toast({
        title: "Error",
        description: "No hay planilla para descargar",
        variant: "destructive"
      })
      return
    }

    try {
      const response = await fetch(`/api/clasificador/generate-excel/${planilla.planilla_id}`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `clasificado_${planilla.filename}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
        
        toast({
          title: "Descarga iniciada",
          description: "El archivo Excel se está descargando",
        })
      } else {
        throw new Error('Error al generar el archivo')
      }
    } catch (error) {
      toast({
        title: "Error en la descarga",
        description: error.message,
        variant: "destructive"
      })
    }
  }

  const getMethodBadgeColor = (method) => {
    switch (method) {
      case 'GEMINI': return 'bg-blue-100 text-blue-800'
      case 'OPENAI': return 'bg-green-100 text-green-800'
      case 'REGLAS': return 'bg-orange-100 text-orange-800'
      case 'DEFECTO': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getConfidenceColor = (confidence) => {
    const conf = parseFloat(confidence)
    if (conf >= 0.8) return 'text-green-600'
    if (conf >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Paginación
  const totalPages = Math.ceil(filteredResults.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentItems = filteredResults.slice(startIndex, endIndex)

  if (!planilla) {
    return (
      <div className="max-w-4xl mx-auto">
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            No hay planilla procesada. Por favor, procesa un archivo primero.
          </AlertDescription>
        </Alert>
      </div>
    )
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
              Resultados de Clasificación
            </h1>
            <p className="text-lg text-gray-600">
              Archivo: {planilla.filename}
            </p>
          </div>
          <Button 
            onClick={downloadExcel}
            className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700"
          >
            <Download className="h-4 w-4 mr-2" />
            Descargar Excel
          </Button>
        </div>
      </motion.div>

      {/* Estadísticas */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-4 gap-6"
      >
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Procesados</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total?.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">registros clasificados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tiempo Promedio</CardTitle>
            <Clock className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(stats.tiempoPromedio / 1000).toFixed(1)}s</div>
            <p className="text-xs text-muted-foreground">por registro</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Método Principal</CardTitle>
            <BarChart3 className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Object.entries(stats.porMetodo || {}).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">más utilizado</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Delito Principal</CardTitle>
            <PieChart className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold">
              {Object.entries(stats.porCalificacion || {}).sort((a, b) => b[1] - a[1])[0]?.[0]?.replace(/_/g, ' ') || 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">más frecuente</p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Filtros */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Filter className="h-5 w-5" />
              <span>Filtros y Búsqueda</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Buscar por ID o calificación..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={filterCalificacion} onValueChange={setFilterCalificacion}>
                <SelectTrigger>
                  <SelectValue placeholder="Filtrar por calificación" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todas las calificaciones</SelectItem>
                  {Object.keys(stats.porCalificacion || {}).map(cal => (
                    <SelectItem key={cal} value={cal}>
                      {cal.replace(/_/g, ' ')} ({stats.porCalificacion[cal]})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select value={filterJurisdiccion} onValueChange={setFilterJurisdiccion}>
                <SelectTrigger>
                  <SelectValue placeholder="Filtrar por jurisdicción" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todas las jurisdicciones</SelectItem>
                  {Object.keys(stats.porJurisdiccion || {}).map(jur => (
                    <SelectItem key={jur} value={jur}>
                      {jur} ({stats.porJurisdiccion[jur]})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Button 
                variant="outline" 
                onClick={() => {
                  setSearchTerm('')
                  setFilterCalificacion('')
                  setFilterJurisdiccion('')
                }}
              >
                Limpiar Filtros
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Tabla de resultados */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Eye className="h-5 w-5" />
                <span>Resultados Clasificados</span>
              </div>
              <Badge variant="outline">
                {filteredResults.length} de {results.length} registros
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID Hecho</TableHead>
                    <TableHead>Registro</TableHead>
                    <TableHead>Fecha</TableHead>
                    <TableHead>Calificación</TableHead>
                    <TableHead>Jurisdicción</TableHead>
                    <TableHead>Víctimas</TableHead>
                    <TableHead>Armas</TableHead>
                    <TableHead>Lugar</TableHead>
                    <TableHead>Método</TableHead>
                    <TableHead>Confianza</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {currentItems.map((item) => (
                    <TableRow key={item.id}>
                      <TableCell className="font-medium">{item.id_hecho}</TableCell>
                      <TableCell>{item.nro_registro}</TableCell>
                      <TableCell>{item.fecha_hecho}</TableCell>
                      <TableCell>
                        <div className="max-w-32 truncate" title={item.calificacion}>
                          {item.calificacion.replace(/_/g, ' ')}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{item.jurisdiccion}</Badge>
                      </TableCell>
                      <TableCell>{item.victimas}</TableCell>
                      <TableCell>{item.armas}</TableCell>
                      <TableCell>{item.lugar}</TableCell>
                      <TableCell>
                        <Badge className={getMethodBadgeColor(item.metodo_clasificacion)}>
                          {item.metodo_clasificacion}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <span className={`font-medium ${getConfidenceColor(item.confianza)}`}>
                          {(parseFloat(item.confianza) * 100).toFixed(0)}%
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Paginación */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-4">
                <div className="text-sm text-gray-500">
                  Mostrando {startIndex + 1} a {Math.min(endIndex, filteredResults.length)} de {filteredResults.length} resultados
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                  >
                    Anterior
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                  >
                    Siguiente
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

export default Results

