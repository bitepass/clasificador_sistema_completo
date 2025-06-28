import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Map, 
  Download, 
  Filter, 
  Layers, 
  MapPin, 
  BarChart3,
  Calendar,
  RefreshCw,
  Eye,
  Settings
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Slider } from '@/components/ui/slider'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { useToast } from '@/hooks/use-toast'

const HeatMap = () => {
  const [selectedPartido, setSelectedPartido] = useState('San Martín')
  const [selectedDelito, setSelectedDelito] = useState('todos')
  const [intensidad, setIntensidad] = useState([70])
  const [mostrarEtiquetas, setMostrarEtiquetas] = useState(true)
  const [tipoVisualizacion, setTipoVisualizacion] = useState('calor')
  const [loading, setLoading] = useState(false)
  const [datosDelitos, setDatosDelitos] = useState([])
  const { toast } = useToast()

  const partidos = [
    'San Martín',
    'José C. Paz',
    'Malvinas Argentinas',
    'San Miguel',
    'Tres de Febrero'
  ]

  const tiposDelito = [
    { value: 'todos', label: 'Todos los delitos' },
    { value: 'robos', label: 'Robos' },
    { value: 'homicidios', label: 'Homicidios' },
    { value: 'lesiones', label: 'Lesiones' },
    { value: 'sustracciones', label: 'Sustracciones' }
  ]

  const tiposVisualizacion = [
    { value: 'calor', label: 'Mapa de Calor', icon: '🔥' },
    { value: 'puntos', label: 'Puntos', icon: '📍' },
    { value: 'clusters', label: 'Clusters', icon: '🎯' }
  ]

  const zonas = [
    {
      id: 1,
      nombre: 'Centro',
      coordenadas: { lat: -34.5722, lng: -58.5358 },
      delitos: 45,
      intensidad: 'alta',
      tipos: { robos: 28, lesiones: 12, otros: 5 }
    },
    {
      id: 2,
      nombre: 'Villa Ballester',
      coordenadas: { lat: -34.5489, lng: -58.5503 },
      delitos: 32,
      intensidad: 'media',
      tipos: { robos: 20, lesiones: 8, otros: 4 }
    },
    {
      id: 3,
      nombre: 'Chilavert',
      coordenadas: { lat: -34.5856, lng: -58.5167 },
      delitos: 28,
      intensidad: 'media',
      tipos: { robos: 18, lesiones: 6, otros: 4 }
    },
    {
      id: 4,
      nombre: 'Villa Maipú',
      coordenadas: { lat: -34.5611, lng: -58.5444 },
      delitos: 19,
      intensidad: 'baja',
      tipos: { robos: 12, lesiones: 4, otros: 3 }
    },
    {
      id: 5,
      nombre: 'José León Suárez',
      coordenadas: { lat: -34.5333, lng: -58.5667 },
      delitos: 38,
      intensidad: 'alta',
      tipos: { robos: 24, lesiones: 10, otros: 4 }
    }
  ]

  useEffect(() => {
    cargarDatosMapa()
  }, [selectedPartido, selectedDelito])

  const cargarDatosMapa = async () => {
    setLoading(true)
    try {
      // Simular carga de datos
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // En implementación real, esto vendría de la API
      const datosFiltrados = zonas.filter(zona => {
        if (selectedDelito === 'todos') return true
        return zona.tipos[selectedDelito] > 0
      })
      
      setDatosDelitos(datosFiltrados)
    } catch (error) {
      console.error('Error cargando datos del mapa:', error)
      toast({
        title: "Error",
        description: "No se pudieron cargar los datos del mapa",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const descargarMapa = async () => {
    try {
      // Simular generación y descarga del mapa
      toast({
        title: "Generando imagen",
        description: "El mapa se está procesando...",
      })

      await new Promise(resolve => setTimeout(resolve, 2000))

      // Simular descarga
      const canvas = document.createElement('canvas')
      canvas.width = 800
      canvas.height = 600
      const ctx = canvas.getContext('2d')
      
      // Crear imagen simple del mapa
      ctx.fillStyle = '#f0f9ff'
      ctx.fillRect(0, 0, 800, 600)
      ctx.fillStyle = '#1e40af'
      ctx.font = '24px Arial'
      ctx.fillText(`Mapa de Calor - ${selectedPartido}`, 50, 50)
      
      // Agregar puntos de calor simulados
      datosDelitos.forEach((zona, index) => {
        const x = 100 + (index * 150)
        const y = 200 + (Math.random() * 200)
        const radius = zona.delitos
        
        ctx.fillStyle = zona.intensidad === 'alta' ? '#ef4444' : 
                       zona.intensidad === 'media' ? '#f59e0b' : '#10b981'
        ctx.beginPath()
        ctx.arc(x, y, radius, 0, 2 * Math.PI)
        ctx.fill()
        
        ctx.fillStyle = '#000'
        ctx.font = '12px Arial'
        ctx.fillText(zona.nombre, x - 30, y + radius + 15)
      })

      canvas.toBlob(blob => {
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `mapa_calor_${selectedPartido}_${new Date().toISOString().split('T')[0]}.png`
        document.body.appendChild(a)
        a.click()
        URL.revokeObjectURL(url)
        document.body.removeChild(a)
      })

      toast({
        title: "Mapa descargado",
        description: "La imagen del mapa se ha guardado exitosamente",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo descargar el mapa",
        variant: "destructive"
      })
    }
  }

  const getIntensidadColor = (intensidad) => {
    switch (intensidad) {
      case 'alta': return 'bg-red-500'
      case 'media': return 'bg-yellow-500'
      case 'baja': return 'bg-green-500'
      default: return 'bg-gray-500'
    }
  }

  const getIntensidadText = (intensidad) => {
    switch (intensidad) {
      case 'alta': return 'text-red-700'
      case 'media': return 'text-yellow-700'
      case 'baja': return 'text-green-700'
      default: return 'text-gray-700'
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Mapa de Calor de Delitos
          </h1>
          <p className="text-lg text-gray-600">
            Visualización geográfica de la distribución de delitos por zona
          </p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Panel de controles */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="lg:col-span-1"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="h-5 w-5" />
                <span>Configuración</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Selección de partido */}
              <div className="space-y-2">
                <Label>Partido</Label>
                <Select value={selectedPartido} onValueChange={setSelectedPartido}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {partidos.map(partido => (
                      <SelectItem key={partido} value={partido}>
                        <div className="flex items-center space-x-2">
                          <MapPin className="h-4 w-4" />
                          <span>{partido}</span>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Tipo de delito */}
              <div className="space-y-2">
                <Label>Tipo de Delito</Label>
                <Select value={selectedDelito} onValueChange={setSelectedDelito}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {tiposDelito.map(tipo => (
                      <SelectItem key={tipo.value} value={tipo.value}>
                        {tipo.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Tipo de visualización */}
              <div className="space-y-2">
                <Label>Visualización</Label>
                <div className="space-y-2">
                  {tiposVisualizacion.map(tipo => (
                    <Button
                      key={tipo.value}
                      variant={tipoVisualizacion === tipo.value ? "default" : "outline"}
                      onClick={() => setTipoVisualizacion(tipo.value)}
                      className="w-full justify-start"
                      size="sm"
                    >
                      <span className="mr-2">{tipo.icon}</span>
                      {tipo.label}
                    </Button>
                  ))}
                </div>
              </div>

              {/* Intensidad */}
              <div className="space-y-2">
                <Label>Intensidad: {intensidad[0]}%</Label>
                <Slider
                  value={intensidad}
                  onValueChange={setIntensidad}
                  max={100}
                  min={10}
                  step={10}
                  className="w-full"
                />
              </div>

              {/* Opciones */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label htmlFor="etiquetas">Mostrar etiquetas</Label>
                  <Switch
                    id="etiquetas"
                    checked={mostrarEtiquetas}
                    onCheckedChange={setMostrarEtiquetas}
                  />
                </div>
              </div>

              {/* Botones de acción */}
              <div className="space-y-2">
                <Button 
                  onClick={cargarDatosMapa} 
                  disabled={loading}
                  className="w-full"
                  variant="outline"
                >
                  <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                  Actualizar
                </Button>
                
                <Button 
                  onClick={descargarMapa}
                  className="w-full bg-gradient-to-r from-green-500 to-green-600"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Descargar Imagen
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Área del mapa */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-3"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Map className="h-5 w-5" />
                  <span>Mapa de Calor - {selectedPartido}</span>
                </div>
                <Badge variant="outline">
                  {datosDelitos.length} zonas
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {/* Simulación del mapa */}
              <div className="relative bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg h-96 overflow-hidden">
                {loading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2 text-blue-600" />
                      <p className="text-gray-600">Cargando datos del mapa...</p>
                    </div>
                  </div>
                ) : (
                  <div className="relative w-full h-full">
                    {/* Fondo del mapa */}
                    <div className="absolute inset-0 bg-gradient-to-br from-slate-100 to-slate-200">
                      <div className="absolute top-4 left-4 text-xs text-gray-500">
                        {selectedPartido} - Mapa de Calor
                      </div>
                    </div>

                    {/* Puntos de calor */}
                    {datosDelitos.map((zona, index) => {
                      const x = 10 + (index * 15) + Math.random() * 60
                      const y = 20 + Math.random() * 60
                      const size = Math.max(zona.delitos / 2, 20)
                      
                      return (
                        <motion.div
                          key={zona.id}
                          initial={{ scale: 0, opacity: 0 }}
                          animate={{ scale: 1, opacity: 0.7 }}
                          transition={{ duration: 0.5, delay: index * 0.1 }}
                          className={`absolute rounded-full ${getIntensidadColor(zona.intensidad)} cursor-pointer hover:opacity-90 transition-all`}
                          style={{
                            left: `${x}%`,
                            top: `${y}%`,
                            width: `${size}px`,
                            height: `${size}px`,
                            transform: 'translate(-50%, -50%)'
                          }}
                          title={`${zona.nombre}: ${zona.delitos} delitos`}
                        >
                          {mostrarEtiquetas && (
                            <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs font-medium text-gray-700 whitespace-nowrap">
                              {zona.nombre}
                            </div>
                          )}
                        </motion.div>
                      )
                    })}

                    {/* Leyenda */}
                    <div className="absolute bottom-4 right-4 bg-white p-3 rounded-lg shadow-md">
                      <div className="text-xs font-medium mb-2">Intensidad</div>
                      <div className="space-y-1">
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                          <span className="text-xs">Alta (30+)</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                          <span className="text-xs">Media (15-29)</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                          <span className="text-xs">Baja (1-14)</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Estadísticas por zona */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Estadísticas por Zona</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {datosDelitos.map(zona => (
                  <motion.div
                    key={zona.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium">{zona.nombre}</h3>
                      <Badge className={`${getIntensidadColor(zona.intensidad)} text-white`}>
                        {zona.intensidad}
                      </Badge>
                    </div>
                    <div className="text-2xl font-bold text-gray-900 mb-2">
                      {zona.delitos}
                    </div>
                    <div className="text-sm text-gray-500 space-y-1">
                      <div>Robos: {zona.tipos.robos}</div>
                      <div>Lesiones: {zona.tipos.lesiones}</div>
                      <div>Otros: {zona.tipos.otros}</div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

export default HeatMap

