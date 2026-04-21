import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const BACKEND_URL = process.env.VITE_BACKEND_URL || 'http://localhost:8023'
const WS_BACKEND_URL = BACKEND_URL.replace(/^http/, 'ws')

export default defineConfig({
  plugins: [react()],
  server: {
    host: process.env.VITE_HOST || 'localhost',
    port: parseInt(process.env.VITE_PORT || '5173'),
    proxy: {
      '/api': BACKEND_URL,
      '/ws': { target: WS_BACKEND_URL, ws: true },
    },
  },
})
