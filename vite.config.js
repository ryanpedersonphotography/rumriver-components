import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  histoire: {
    setupFile: './src/histoire-setup.js'
  }
})