import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { 
  Upload, 
  File, 
  CheckCircle, 
  AlertCircle, 
  X,
  FileSpreadsheet,
  Info
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { useToast } from '@/hooks/use-toast'

const FileUpload = ({ onFileUploaded, currentPlanilla }) => {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [error, setError] = useState(null)
  const { toast } = useToast()

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    // Validar tipo de archivo
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
      setError('Solo se permiten archivos Excel (.xlsx, .xls)')
      return
    }

    // Validar tamaño (máximo 16MB)
    if (file.size > 16 * 1024 * 1024) {
      setError('El archivo es demasiado grande. Máximo 16MB.')
      return
    }

    setError(null)
    setUploading(true)
    setUploadProgress(0)

    try {
      const formData = new FormData()
      formData.append('file', file)

      // Simular progreso de subida
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return prev
          }
          return prev + 10
        })
      }, 200)

      const response = await fetch(`${import.meta.env.VITE_API_URL}/clasificador/upload`, {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (response.ok) {
        const result = await response.json()
        setUploadedFile({
          name: file.name,
          size: file.size,
          totalFilas: result.total_filas,
          planillaId: result.planilla_id
        })
        
        toast({
          title: "Archivo subido exitosamente",
          description: `Se procesarán ${result.total_filas} registros`,
        })

        onFileUploaded(result)
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Error subiendo archivo')
      }
    } catch (err) {
      setError(err.message)
      toast({
        title: "Error al subir archivo",
        description: err.message,
        variant: "destructive"
      })
    } finally {
      setUploading(false)
    }
  }, [onFileUploaded, toast])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    multiple: false,
    disabled: uploading
  })

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const resetUpload = () => {
    setUploadedFile(null)
    setError(null)
    setUploadProgress(0)
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
            Cargar Planilla Excel
          </h1>
          <p className="text-lg text-gray-600">
            Sube tu archivo Excel con los hechos delictivos para procesar
          </p>
        </div>
      </motion.div>

      {/* Información del formato */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Alert className="bg-blue-50 border-blue-200">
          <Info className="h-4 w-4 text-blue-600" />
          <AlertDescription className="text-blue-800">
            <strong>Formato esperado:</strong> El archivo debe contener columnas como id_hecho, nro_registro, ipp, 
            fecha_hecho, relato, etc. Se procesarán todas las filas automáticamente.
          </AlertDescription>
        </Alert>
      </motion.div>

      {/* Zona de subida */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card className="border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors">
          <CardContent className="p-8">
            <div
              {...getRootProps()}
              className={`text-center cursor-pointer transition-all duration-200 ${
                isDragActive ? 'scale-105' : ''
              } ${uploading ? 'pointer-events-none opacity-50' : ''}`}
            >
              <input {...getInputProps()} />
              
              <motion.div
                animate={isDragActive ? { scale: 1.1 } : { scale: 1 }}
                transition={{ duration: 0.2 }}
                className="mb-6"
              >
                <div className="w-20 h-20 mx-auto bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-4">
                  <FileSpreadsheet className="h-10 w-10 text-blue-600" />
                </div>
              </motion.div>

              {uploading ? (
                <div className="space-y-4">
                  <div className="text-lg font-medium text-gray-900">
                    Subiendo archivo...
                  </div>
                  <Progress value={uploadProgress} className="w-full max-w-md mx-auto" />
                  <div className="text-sm text-gray-500">
                    {uploadProgress}% completado
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-lg font-medium text-gray-900">
                    {isDragActive
                      ? 'Suelta el archivo aquí'
                      : 'Arrastra tu archivo Excel aquí o haz clic para seleccionar'
                    }
                  </div>
                  <div className="text-sm text-gray-500">
                    Formatos soportados: .xlsx, .xls (máximo 16MB)
                  </div>
                  <Button variant="outline" className="mt-4">
                    <Upload className="h-4 w-4 mr-2" />
                    Seleccionar Archivo
                  </Button>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>

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

      {/* Archivo subido */}
      <AnimatePresence>
        {uploadedFile && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="bg-green-50 border-green-200">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-green-800">
                  <CheckCircle className="h-5 w-5" />
                  <span>Archivo Subido Exitosamente</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                      <FileSpreadsheet className="h-6 w-6 text-green-600" />
                    </div>
                    <div>
                      <div className="font-medium text-green-900">{uploadedFile.name}</div>
                      <div className="text-sm text-green-700">
                        {formatFileSize(uploadedFile.size)} • {uploadedFile.totalFilas} registros
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge className="bg-green-100 text-green-800">
                      Listo para procesar
                    </Badge>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={resetUpload}
                      className="text-green-700 hover:text-green-900"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Planilla actual */}
      <AnimatePresence>
        {currentPlanilla && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="bg-blue-50 border-blue-200">
              <CardHeader>
                <CardTitle className="text-blue-800">Planilla Actual</CardTitle>
                <CardDescription className="text-blue-600">
                  Archivo cargado y listo para procesar
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-blue-900">{currentPlanilla.filename}</div>
                    <div className="text-sm text-blue-700">
                      {currentPlanilla.total_filas} registros para procesar
                    </div>
                  </div>
                  <Badge className="bg-blue-100 text-blue-800">
                    ID: {currentPlanilla.planilla_id}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default FileUpload

