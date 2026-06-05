import { defineConfig } from "vite";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import babel from "@rolldown/plugin-babel";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), babel({ presets: [reactCompilerPreset()] })],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  root: ".",
  publicDir: "public",
  server: {
    // Match the backend's FRONTEND_HOST / CORS origin (docker-compose.yml).
    port: 5175,
    // Proxy API calls to the FastAPI backend so the browser stays same-origin
    // (no CORS needed in dev). Override the target with VITE_API_PROXY_TARGET.
    proxy: {
      "/api": {
        target: process.env.VITE_API_PROXY_TARGET ?? "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist/client",
    emptyOutDir: true,
  },
});
