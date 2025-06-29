import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

const resources = {
  es: {
    translation: {
      'Clasificador AI de Documentos': 'Clasificador AI de Documentos',
      'Sistema inteligente para la clasificación automática de documentos criminales': 'Sistema inteligente para la clasificación automática de documentos criminales',
      'Cargar Archivo Excel': 'Cargar Archivo Excel',
      'Selecciona un archivo Excel (.xlsx, .xls) que contenga los relatos a clasificar': 'Selecciona un archivo Excel (.xlsx, .xls) que contenga los relatos a clasificar',
      'Procesar': 'Procesar',
      'Procesando...': 'Procesando...',
      'Archivo seleccionado:': 'Archivo seleccionado:',
      'Progreso:': 'Progreso:',
      '¡Archivo procesado correctamente!': '¡Archivo procesado correctamente!',
      'Solo se permiten archivos Excel (.xlsx, .xls)': 'Solo se permiten archivos Excel (.xlsx, .xls)',
      'El archivo es demasiado grande (máx. 5MB)': 'El archivo es demasiado grande (máx. 5MB)',
      'Resultados de la Clasificación': 'Resultados de la Clasificación',
      'Se procesaron {{count}} registros exitosamente': 'Se procesaron {{count}} registros exitosamente',
      'Filtrar por categoría:': 'Filtrar por categoría:',
      'Buscar texto:': 'Buscar texto:',
      'Total de documentos clasificados:': 'Total de documentos clasificados:',
      'Descargar Excel': 'Descargar Excel',
      'Vista previa de resultados:': 'Vista previa de resultados:',
      'No se encontraron resultados.': 'No se encontraron resultados.',
      'Ayuda y Documentación': 'Ayuda y Documentación',
      'Para soporte, visita el': 'Para soporte, visita el',
      'Formatos soportados: Excel (.xlsx, .xls) con columnas: relato, descripcion, hechos, narracion.': 'Formatos soportados: Excel (.xlsx, .xls) con columnas: relato, descripcion, hechos, narracion.',
      'Cantidad de Delitos por Categoría': 'Cantidad de Delitos por Categoría',
      'Inicio': 'Inicio',
      'Ayuda': 'Ayuda',
      'Resultados': 'Resultados',
      'Cargar Archivo': 'Cargar Archivo',
    }
  },
  en: {
    translation: {
      'Clasificador AI de Documentos': 'AI Document Classifier',
      'Sistema inteligente para la clasificación automática de documentos criminales': 'Intelligent system for automatic classification of criminal documents',
      'Cargar Archivo Excel': 'Upload Excel File',
      'Selecciona un archivo Excel (.xlsx, .xls) que contenga los relatos a clasificar': 'Select an Excel file (.xlsx, .xls) containing the reports to classify',
      'Procesar': 'Process',
      'Procesando...': 'Processing...',
      'Archivo seleccionado:': 'Selected file:',
      'Progreso:': 'Progress:',
      '¡Archivo procesado correctamente!': 'File processed successfully!',
      'Solo se permiten archivos Excel (.xlsx, .xls)': 'Only Excel files (.xlsx, .xls) are allowed',
      'El archivo es demasiado grande (máx. 5MB)': 'The file is too large (max 5MB)',
      'Resultados de la Clasificación': 'Classification Results',
      'Se procesaron {{count}} registros exitosamente': '{{count}} records processed successfully',
      'Filtrar por categoría:': 'Filter by category:',
      'Buscar texto:': 'Search text:',
      'Total de documentos clasificados:': 'Total classified documents:',
      'Descargar Excel': 'Download Excel',
      'Vista previa de resultados:': 'Results preview:',
      'No se encontraron resultados.': 'No results found.',
      'Ayuda y Documentación': 'Help & Documentation',
      'Para soporte, visita el': 'For support, visit the',
      'Formatos soportados: Excel (.xlsx, .xls) con columnas: relato, descripcion, hechos, narracion.': 'Supported formats: Excel (.xlsx, .xls) with columns: relato, descripcion, hechos, narracion.',
      'Cantidad de Delitos por Categoría': 'Number of Crimes by Category',
      'Inicio': 'Home',
      'Ayuda': 'Help',
      'Resultados': 'Results',
      'Cargar Archivo': 'Upload File',
    }
  }
}

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'es',
    fallbackLng: 'es',
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n 