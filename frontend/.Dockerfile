# --- Build stage: compile the Vite app with Bun ---
FROM oven/bun:1 AS build

WORKDIR /app

# Install dependencies first for better layer caching.
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

# Build the static assets (tsc -b && vite build -> dist/client).
COPY . .
RUN bun run build

# --- Runtime stage: serve static assets and proxy /api via nginx ---
FROM nginx:1.27-alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/client /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
