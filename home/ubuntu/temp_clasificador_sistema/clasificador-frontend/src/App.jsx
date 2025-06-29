import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Upload, Download, FileText, Brain, CheckCircle, AlertCircle } from 'lucide-react'
import { Menubar, MenubarMenu, MenubarTrigger, MenubarContent, MenubarItem } from '@/components/ui/menubar.jsx'
import { ChartContainer } from '@/components/ui/chart.jsx'
import './App.css'
import { Routes, Route, useNavigate } from 'react-router-dom'
import { useAppContext } from './AppContext.jsx'
import Spinner from './components/ui/spinner.jsx'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { useTranslation } from 'react-i18next'

function CargaArchivo({ handleFileChange, handleUpload, t }) {
  const { file, loading, error, progress } = useAppContext()
  const [success, setSuccess] = useState(false)
  const [fileError, setFileError] = useState(null)

  // Validación de archivo
  const validateFile = (event) => {
    setFileError(null)
    setSuccess(false)
    const selectedFile = event.target.files[0]
    if (!selectedFile) return handleFileChange(event)
    const validTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
    const maxSize = 5 * 1024 * 1024 // 5MB
    if (!validTypes.includes(selectedFile.type)) {
      setFileError('Solo se permiten archivos Excel (.xlsx, .xls)')
      return
    }
    if (selectedFile.size > maxSize) {
      setFileError('El archivo es demasiado grande (máx. 5MB)')
      return
    }
    handleFileChange(event)
  }

  React.useEffect(() => {
    if (progress === 100 && !loading && !error && file) {
      setSuccess(true)
    }
  }, [progress, loading, error, file])

  return (
    <div className="grid gap-6">
      {/* Card de carga de archivo */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            {t('Cargar Archivo Excel')}
          </CardTitle>
          <CardDescription>
            {t('Selecciona un archivo Excel (.xlsx, .xls) que contenga los relatos a clasificar')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={validateFile}
              className="flex-1 text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            <Button 
              onClick={handleUpload} 
              disabled={!file || loading || !!fileError}
              className="min-w-[120px]"
            >
              {loading ? <Spinner size={20} /> : t('Procesar')}
            </Button>
          </div>
          {file && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <FileText className="h-4 w-4" />
              {t('Archivo seleccionado:')} {file.name}
            </div>
          )}
          {/* Mostrar progreso general aunque no esté cargando */}
          <div className="mb-4">
            <Progress value={progress} className="w-full" />
            <p className="text-sm text-gray-600 text-center">
              {t('Progreso:')} {progress}%
            </p>
          </div>
          {fileError && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{fileError}</AlertDescription>
            </Alert>
          )}
          {success && (
            <Alert variant="success">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription>{t('¡Archivo procesado correctamente!')}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
      {/* Mostrar errores */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}

function Resultados({ handleDownload, t }) {
  const { results } = useAppContext()
  const [categoriaFiltro, setCategoriaFiltro] = React.useState('')
  const [busqueda, setBusqueda] = React.useState('')
  if (!results) return null
  // Obtener todas las categorías únicas
  const categorias = Array.from(new Set(results.resultados.map(r => r.clasificacion.CALIFICACION_LEGAL || 'OTROS')))
  // Filtrar resultados
  const resultadosFiltrados = results.resultados.filter(r => {
    const coincideCategoria = categoriaFiltro ? r.clasificacion.CALIFICACION_LEGAL === categoriaFiltro : true
    const coincideBusqueda = busqueda ? (r.texto_original.toLowerCase().includes(busqueda.toLowerCase())) : true
    return coincideCategoria && coincideBusqueda
  })
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CheckCircle className="h-5 w-5 text-green-600" aria-hidden="true" />
          <span id="resultados-title">{t('Resultados de la Clasificación')}</span>
        </CardTitle>
        <CardDescription id="resultados-desc">
          {t('Se procesaron')} {results.total_filas} {t('registros exitosamente')}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-wrap gap-4 items-center mb-2">
          <div>
            <label htmlFor="categoriaFiltro" className="text-sm font-medium mr-2">{t('Filtrar por categoría:')}</label>
            <select
              id="categoriaFiltro"
              value={categoriaFiltro}
              onChange={e => setCategoriaFiltro(e.target.value)}
              className="border rounded px-2 py-1 text-sm focus:outline-blue-500"
              aria-label={t('Filtrar por categoría')}
            >
              <option value="">{t('Todas')}</option>
              {categorias.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="busqueda" className="text-sm font-medium mr-2">{t('Buscar texto:')}</label>
            <input
              id="busqueda"
              type="text"
              value={busqueda}
              onChange={e => setBusqueda(e.target.value)}
              placeholder={t('Buscar...')}
              className="border rounded px-2 py-1 text-sm focus:outline-blue-500"
              aria-label={t('Buscar texto en resultados')}
            />
          </div>
        </div>
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-600">
            {t('Total de documentos clasificados:')} <span className="font-semibold">{resultadosFiltrados.length}</span>
          </div>
          <Button onClick={handleDownload} className="flex items-center gap-2" aria-label={t('Descargar resultados en Excel')}>
            <Download className="h-4 w-4" aria-hidden="true" />
            {t('Descargar Excel')}
          </Button>
        </div>
        {/* Vista previa de algunos resultados */}
        <div className="border rounded-lg p-4 bg-gray-50 max-h-96 overflow-y-auto" role="region" aria-labelledby="resultados-title" aria-describedby="resultados-desc">
          <h4 className="font-semibold mb-3">{t('Vista previa de resultados:')}</h4>
          <div className="space-y-3">
            {resultadosFiltrados.slice(0, 3).map((resultado, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4 py-2 bg-white rounded" tabIndex={0} aria-label={t('Resultado fila')} aria-describedby={`Resultado fila ${resultado.fila}`}>
                <div className="text-sm">
                  <p className="font-medium">{t('Fila')} {resultado.fila}:</p>
                  <p className="text-gray-600 truncate">{resultado.texto_original.substring(0, 100)}...</p>
                  <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                    <span><strong>{t('Calificación:')}</strong> {resultado.clasificacion.CALIFICACION_LEGAL}</span>
                    <span><strong>{t('Modalidad:')}</strong> {resultado.clasificacion.MODALIDAD}</span>
                    <span><strong>{t('Arma:')}</strong> {resultado.clasificacion.ARMA}</span>
                    <span><strong>{t('Jurisdicción:')}</strong> {resultado.clasificacion.JURISDICCION}</span>
                  </div>
                </div>
              </div>
            ))}
            {resultadosFiltrados.length > 3 && (
              <p className="text-sm text-gray-500 text-center">
                {t('... y')} {resultadosFiltrados.length - 3} {t('registros más')}
              </p>
            )}
            {resultadosFiltrados.length === 0 && (
              <p className="text-sm text-gray-500 text-center">{t('No se encontraron resultados.')}</p>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function Ayuda({ t }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">{t('Ayuda y Documentación')}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-gray-700">
          <p>{t('Para soporte, visita el')} <a href="https://github.com/bitepass/clasificador_sistema_completo" className="text-blue-600 underline" target="_blank" rel="noopener noreferrer">{t('repositorio en GitHub')}</a>.</p>
          <p>{t('Formatos soportados: Excel (.xlsx, .xls) con columnas: relato, descripcion, hechos, narracion.')}</p>
        </div>
      </CardContent>
    </Card>
  )
}

function GraficoClasificacion({ t }) {
  const { results } = useAppContext()
  if (!results || !results.resultados) return null
  // Contar cantidad por categoría
  const counts = {}
  results.resultados.forEach(r => {
    const cat = r.clasificacion.CALIFICACION_LEGAL || 'OTROS'
    counts[cat] = (counts[cat] || 0) + 1
  })
  const data = Object.entries(counts).map(([categoria, cantidad]) => ({ categoria, cantidad }))
  if (data.length === 0) return null
  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle className="text-lg">{t('Cantidad de Delitos por Categoría')}</CardTitle>
      </CardHeader>
      <CardContent>
        <div style={{ width: '100%', height: 350 }}>
          <ResponsiveContainer>
            <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 40 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="categoria" angle={-30} textAnchor="end" interval={0} height={80} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="cantidad" fill="#2563eb" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}

function App() {
  const { file, setFile, loading, setLoading, results, setResults, error, setError, progress, setProgress } = useAppContext()
  const navigate = useNavigate()
  const { t, i18n } = useTranslation()
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')

  useEffect(() => {
    const root = window.document.documentElement
    if (theme === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    localStorage.setItem('theme', theme)
  }, [theme])

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError(null)
      setResults(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Por favor selecciona un archivo Excel')
      return
    }
    setLoading(true)
    setError(null)
    setProgress(0)
    const formData = new FormData()
    formData.append('file', file)
    try {
      // Simular progreso
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90))
      }, 500)
      const response = await fetch('http://localhost:5000/api/clasificador/upload', {
        method: 'POST',
        body: formData,
      })
      clearInterval(progressInterval)
      setProgress(100)
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Error al procesar el archivo')
      }
      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!results) return
    try {
      const response = await fetch("http://localhost:5000/api/clasificador/generate-excel", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resultados: results.resultados,
          original_columns: results.original_columns,
          original_data: results.original_data,
        }),
      })
      if (!response.ok) {
        throw new Error("Error al generar el archivo Excel")
      }
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.style.display = "none"
      a.href = url
      a.download = "clasificacion_resultados.xlsx"
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4 transition-colors duration-300">
      {/* Menú principal siempre visible */}
      <div className="max-w-4xl mx-auto mb-4">
        <Menubar>
          <MenubarMenu>
            <MenubarTrigger onClick={() => navigate('/')}>{t('Inicio')}</MenubarTrigger>
            <MenubarContent>
              <MenubarItem onClick={() => navigate('/')}>{t('Cargar Archivo')}</MenubarItem>
              <MenubarItem onClick={() => navigate('/resultados')}>{t('Resultados')}</MenubarItem>
              <MenubarItem onClick={() => navigate('/ayuda')}>{t('Ayuda')}</MenubarItem>
            </MenubarContent>
          </MenubarMenu>
          <MenubarMenu>
            <MenubarTrigger>🌐</MenubarTrigger>
            <MenubarContent>
              <MenubarItem onClick={() => i18n.changeLanguage('es')}>Español</MenubarItem>
              <MenubarItem onClick={() => i18n.changeLanguage('en')}>English</MenubarItem>
            </MenubarContent>
          </MenubarMenu>
          <MenubarMenu>
            <MenubarTrigger>{theme === 'dark' ? '🌙' : '☀️'}</MenubarTrigger>
            <MenubarContent>
              <MenubarItem onClick={() => setTheme('light')}>☀️ Claro</MenubarItem>
              <MenubarItem onClick={() => setTheme('dark')}>🌙 Oscuro</MenubarItem>
            </MenubarContent>
          </MenubarMenu>
        </Menubar>
      </div>
      <div className="max-w-4xl mx-auto">
        <Routes>
          <Route path="/" element={
            <>
              <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
                  <Brain className="h-10 w-10 text-blue-600" />
                  {t('Clasificador AI de Documentos')}
                </h1>
                <p className="text-lg text-gray-600">
                  {t('Sistema inteligente para la clasificación automática de documentos criminales')}
                </p>
              </div>
              <CargaArchivo handleFileChange={handleFileChange} handleUpload={handleUpload} t={t} />
            </>
          } />
          <Route path="/resultados" element={<Resultados handleDownload={handleDownload} t={t} />} />
          <Route path="/ayuda" element={<Ayuda t={t} />} />
        </Routes>
        <GraficoClasificacion t={t} />
      </div>
    </div>
  )
}

export default App
