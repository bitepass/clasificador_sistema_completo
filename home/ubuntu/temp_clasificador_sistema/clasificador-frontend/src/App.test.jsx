import { render, screen } from '@testing-library/react'
import { AppProvider } from './AppContext'
import { BrowserRouter } from 'react-router-dom'
import App from './App'

describe('App', () => {
  it('muestra el título principal', () => {
    render(
      <BrowserRouter>
        <AppProvider>
          <App />
        </AppProvider>
      </BrowserRouter>
    )
    expect(screen.getByText(/Clasificador AI de Documentos/i)).toBeInTheDocument()
  })
}) 