// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ mode }) => {
  const isDev = mode === 'development';

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    server: {
      proxy: isDev
        ? {
            '/api': {
              target: 'http://127.0.0.1:8000',
              changeOrigin: true,
              // The rewrite function can adjust the URL path if needed:
              // e.g., if your backend expects /api/ instead of /api
              rewrite: (path) => path.replace(/^\/api/, '/api'),
            },
            '/docs': {
              target: 'http://127.0.0.1:8000',
              changeOrigin: true,
            },
            '/openapi.json': {
              target: 'http://127.0.0.1:8000',
              changeOrigin: true,
            },
          }
        : undefined,
    },
  };
});
