import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

const BACKEND_URL = 'http://localhost:8000'
const BACKEND_PREFIXES = ['/auth', '/robots', '/devis', '/coming-soon', '/imports']

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: Object.fromEntries(
      BACKEND_PREFIXES.map((prefix) => [prefix, { target: BACKEND_URL, changeOrigin: true }])
    )
  }
})