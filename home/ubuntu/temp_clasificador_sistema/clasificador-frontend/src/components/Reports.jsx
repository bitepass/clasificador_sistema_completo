import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Download, 
  Calendar, 
  MapPin, 
  BarChart3, 
  PieChart,
  TrendingUp,
  Users,
  Shield,
  Clock
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { useToast } from '@/hooks/use-toast'

const Reports = () => {
  const [selectedPartido, setSelectedPartido] = useState('')
  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [tipoReporte, setTipoReporte] = useState('situacional')
  const [formato, setFormato] = useState('pdf')
  const [generando, setGenerando] = useState(false)
  const { toast } = useToast()

  const partidos = [
    'San Martín',
    'José C. Paz',
    'Malvinas Argentinas',
    'San Miguel',
    'Tres de Febrero',
    'Hurlingham',
    'Ituzaingó',
    'Morón'
  ]

  const tiposReporte = [
    { value: 'situacional', label: 'Informe Situacional', description: 'Análisis completo de delitos por período' },
    { value: 'estadistico', label: 'Reporte Estadístico', description: 'Datos numéricos y tendencias' },
    { value: 'comparativo', label: 'Análisis Comparativo', description: 'Comparación entre períodos' },
    { value: 'ejecutivo', label: 'Resumen Ejecutivo', description: 'Síntesis para autoridades' }
  ]

  const formatos = [
    { value: 'pdf', label: 'PDF', icon: '📄' },
    { value: 'word', label: 'Word', icon: '📝' },
    { value: 'excel', label: 'Excel', icon: '📊' }
  ]

  const ejemplosInformes = [
    {
      titulo: 'Informe Situacional - San Martín',
      periodo: 'Mayo 2025',
      descripcion: 'Análisis completo de hechos delictivos en San Martín durante mayo 2025',
      estadisticas: {
        totalHechos: 245,
        homicidios: 3,
        robos: 156,
        lesiones: 42
      }
    },
    {
      titulo: 'Informe Situacional - José C. Paz',
      periodo: 'Mayo 2025',
      descripcion: 'Análisis completo de hechos delictivos en José C. Paz durante mayo 2025',
      estadisticas: {
        totalHechos: 189,
        homicidios: 2,
        robos: 134,
        lesiones: 28
      }
    }
  ]

  const generarInforme = async () => {
    if (!selectedPartido) {
      toast({
        title: "Error",
        description: "Por favor selecciona un partido",
        variant: "destructive"
      })
      return
    }

    if (!fechaInicio || !fechaFin) {
      toast({
        title: "Error",
        description: "Por favor selecciona el rango de fechas",
        variant: "destructive"
      })
      return
    }

    setGenerando(true)

    try {
      // Simular generación de informe
      await new Promise(resolve => setTimeout(resolve, 3000))

      // En implementación real, esto sería una llamada a la API
      const response = await fetch('/api/clasificador/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          partido: selectedPartido,
          fechaInicio,
          fechaFin,
          tipoReporte,
          formato
        })
      })

      if (response.ok) {
        // Simular descarga
        const blob = new Blob(['Contenido del informe simulado'], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `informe_${selectedPartido}_${fechaInicio}_${fechaFin}.${formato}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)

        toast({
          title: "Informe generado",
          description: `El informe de ${selectedPartido} se ha generado exitosamente`,
        })
      } else {
        throw new Error('Error generando el informe')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo generar el informe",
        variant: "destructive"
      })
    } finally {
      setGenerando(false)
    }
  }

  const usarUltimaPlanilla = () => {
    const hoy = new Date()
    const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
    setFechaInicio(inicioMes.toISOString().split('T')[0])
    setFechaFin(hoy.toISOString().split('T')[0])
    
    toast({
      title: "Fechas configuradas",
      description: "Se configuró el rango para el mes actual",
    })
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Generación de Informes Situacionales
          </h1>
          <p className="text-lg text-gray-600">
            Crea informes detallados basados en los datos clasificados
          </p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Panel de configuración */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <FileText className="h-5 w-5" />
                <span>Configuración del Informe</span>
              </CardTitle>
              <CardDescription>
                Configura los parámetros para generar tu informe situacional
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Selección de partido */}
              <div className="space-y-2">
                <Label htmlFor="partido">Partido</Label>
                <Select value={selectedPartido} onValueChange={setSelectedPartido}>
                  <SelectTrigger>
                    <SelectValue placeholder="Seleccionar partido" />
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

              {/* Rango de fechas */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="fechaInicio">Fecha de inicio</Label>
                  <Input
                    id="fechaInicio"
                    type="date"
                    value={fechaInicio}
                    onChange={(e) => setFechaInicio(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="fechaFin">Fecha de fin</Label>
                  <Input
                    id="fechaFin"
                    type="date"
                    value={fechaFin}
                    onChange={(e) => setFechaFin(e.target.value)}
                  />
                </div>
              </div>

              <div className="flex justify-center">
                <Button variant="outline" onClick={usarUltimaPlanilla}>
                  <Calendar className="h-4 w-4 mr-2" />
                  Usar última planilla cargada
                </Button>
              </div>

              <Separator />

              {/* Tipo de reporte */}
              <div className="space-y-2">
                <Label>Tipo de Reporte</Label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {tiposReporte.map(tipo => (
                    <div
                      key={tipo.value}
                      className={`p-3 border rounded-lg cursor-pointer transition-all ${
                        tipoReporte === tipo.value
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setTipoReporte(tipo.value)}
                    >
                      <div className="font-medium">{tipo.label}</div>
                      <div className="text-sm text-gray-500">{tipo.description}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Formato de salida */}
              <div className="space-y-2">
                <Label>Formato de Salida</Label>
                <div className="flex space-x-3">
                  {formatos.map(fmt => (
                    <Button
                      key={fmt.value}
                      variant={formato === fmt.value ? "default" : "outline"}
                      onClick={() => setFormato(fmt.value)}
                      className="flex items-center space-x-2"
                    >
                      <span>{fmt.icon}</span>
                      <span>{fmt.label}</span>
                    </Button>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Botón de generación */}
              <Button
                onClick={generarInforme}
                disabled={generando}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
                size="lg"
              >
                {generando ? (
                  <>
                    <Clock className="h-4 w-4 mr-2 animate-spin" />
                    Generando Informe...
                  </>
                ) : (
                  <>
                    <Download className="h-4 w-4 mr-2" />
                    Generar Informe Situacional
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </motion.div>

        {/* Panel de información */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="space-y-6"
        >
          {/* Información del informe */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Contenido del Informe</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-3">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <div>
                  <div className="font-medium">Estadísticas Generales</div>
                  <div className="text-sm text-gray-500">Totales por tipo de delito</div>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <PieChart className="h-5 w-5 text-green-600" />
                <div>
                  <div className="font-medium">Análisis por Modalidad</div>
                  <div className="text-sm text-gray-500">Distribución y tendencias</div>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                <div>
                  <div className="font-medium">Gráficos y Visualizaciones</div>
                  <div className="text-sm text-gray-500">Representación visual de datos</div>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Users className="h-5 w-5 text-orange-600" />
                <div>
                  <div className="font-medium">Análisis de Víctimas</div>
                  <div className="text-sm text-gray-500">Demografía y características</div>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Shield className="h-5 w-5 text-red-600" />
                <div>
                  <div className="font-medium">Recomendaciones</div>
                  <div className="text-sm text-gray-500">Sugerencias operativas</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Ejemplos de informes */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Informes Recientes</CardTitle>
              <CardDescription>Ejemplos de informes generados</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {ejemplosInformes.map((informe, index) => (
                <div key={index} className="p-3 border rounded-lg">
                  <div className="font-medium text-sm">{informe.titulo}</div>
                  <div className="text-xs text-gray-500 mb-2">{informe.periodo}</div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-gray-500">Total:</span>
                      <span className="font-medium ml-1">{informe.estadisticas.totalHechos}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Robos:</span>
                      <span className="font-medium ml-1">{informe.estadisticas.robos}</span>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm" className="w-full mt-2 text-xs">
                    <Download className="h-3 w-3 mr-1" />
                    Descargar
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Información adicional */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <CardHeader>
            <CardTitle className="text-blue-800">Información Importante</CardTitle>
          </CardHeader>
          <CardContent className="text-blue-700">
            <ul className="space-y-2 text-sm">
              <li>• Los informes se generan basándose en los datos clasificados automáticamente</li>
              <li>• Se incluyen gráficos, tablas y análisis estadísticos detallados</li>
              <li>• El formato PDF es recomendado para presentaciones oficiales</li>
              <li>• Los informes siguen el formato estándar utilizado por las fuerzas de seguridad</li>
              <li>• Se pueden generar informes comparativos entre diferentes períodos</li>
            </ul>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

export default Reports

