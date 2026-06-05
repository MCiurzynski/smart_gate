/**
 * Centralised runtime configuration. Keep all `import.meta.env` reads here so
 * the rest of the app depends on a typed object instead of raw env access.
 */
export const env = {
  // Defaults to the Vite dev proxy path (see vite.config.ts).
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? '/api',
} as const;
