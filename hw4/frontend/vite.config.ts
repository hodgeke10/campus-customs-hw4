import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The FastAPI backend serves the API and the product images from port 8000.
const backend = 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': backend,
      '/media': backend,
    },
  },
})
