import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './styles.css'
import App from './App'
import { ThemeProvider } from './contexts/ThemeContext'

const root = createRoot(document.getElementById('root')!)
root.render(
  <BrowserRouter>
    <ThemeProvider>
    <App />
    </ThemeProvider>
  </BrowserRouter>
)


