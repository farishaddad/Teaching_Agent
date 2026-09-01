import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'https://65nvz27oze.execute-api.eu-west-2.amazonaws.com/prod',
        changeOrigin: true,
        secure: true,
      },
    },
  },
});
