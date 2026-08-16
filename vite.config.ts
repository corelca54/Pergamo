import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true
      },
      manifest: {
        name: 'Pérgamo - Gestión Documental',
        short_name: 'Pérgamo',
        description: 'Auditoría de TRD y CCD para unidades operativas',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        icons: []
      }
    })
  ],
  resolve: {
    alias: {
      '@domain': path.resolve(__dirname, './src/domain'),
      '@application': path.resolve(__dirname, './src/application'),
      '@infrastructure': path.resolve(__dirname, './src/infrastructure'),
      '@presentation': path.resolve(__dirname, './src/presentation')
    }
  }
});