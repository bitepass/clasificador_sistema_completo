import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate, useLocation } from 'react-router-dom'
import { 
  Upload, 
  Settings, 
  BarChart3, 
  FileText, 
  Map, 
  History, 
  Home,
  X
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const Sidebar = ({ open, setOpen, currentStep, onStepChange }) => {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: Home,
      path: '/',
      description: 'Vista general del sistema'
    },
    {
      id: 'upload',
      name: 'Cargar Archivo',
      icon: Upload,
      path: '/upload',
      description: 'Subir planilla Excel'
    },
    {
      id: 'process',
      name: 'Procesar',
      icon: Settings,
      path: '/process',
      description: 'Clasificar datos'
    },
    {
      id: 'results',
      name: 'Resultados',
      icon: BarChart3,
      path: '/results',
      description: 'Ver clasificaciones'
    },
    {
      id: 'reports',
      name: 'Informes',
      icon: FileText,
      path: '/reports',
      description: 'Generar informes situacionales'
    },
    {
      id: 'heatmap',
      name: 'Mapa de Calor',
      icon: Map,
      path: '/heatmap',
      description: 'Visualizar delitos por zona'
    },
    {
      id: 'history',
      name: 'Historial',
      icon: History,
      path: '/history',
      description: 'Planillas procesadas'
    }
  ]

  const handleNavigation = (item) => {
    navigate(item.path)
    if (item.id !== 'dashboard') {
      onStepChange(item.id)
    }
    setOpen(false)
  }

  const isActive = (path) => {
    return location.pathname === path
  }

  return (
    <>
      {/* Overlay para móvil */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={() => setOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -280 }}
        animate={{ x: open ? 0 : -280 }}
        transition={{ type: "spring", damping: 25, stiffness: 200 }}
        className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-white border-r border-gray-200 shadow-lg z-50 lg:translate-x-0 lg:static lg:z-auto"
      >
        <div className="flex flex-col h-full">
          {/* Header del sidebar */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">
                Navegación
              </h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setOpen(false)}
                className="lg:hidden"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Menú de navegación */}
          <nav className="flex-1 p-4 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon
              const active = isActive(item.path)
              
              return (
                <motion.button
                  key={item.id}
                  onClick={() => handleNavigation(item)}
                  className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200 ${
                    active
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Icon className={`h-5 w-5 ${active ? 'text-white' : 'text-gray-500'}`} />
                  <div className="flex-1">
                    <div className={`font-medium ${active ? 'text-white' : 'text-gray-900'}`}>
                      {item.name}
                    </div>
                    <div className={`text-xs ${active ? 'text-blue-100' : 'text-gray-500'}`}>
                      {item.description}
                    </div>
                  </div>
                  {active && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="w-2 h-2 bg-white rounded-full"
                    />
                  )}
                </motion.button>
              )
            })}
          </nav>

          {/* Footer del sidebar */}
          <div className="p-4 border-t border-gray-200">
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-3 rounded-lg">
              <div className="flex items-center space-x-2">
                <Badge variant="outline" className="bg-white text-blue-700">
                  v2.0
                </Badge>
                <span className="text-sm text-gray-600">Sistema Mejorado</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Clasificación automática con IA
              </p>
            </div>
          </div>
        </div>
      </motion.aside>
    </>
  )
}

export default Sidebar

