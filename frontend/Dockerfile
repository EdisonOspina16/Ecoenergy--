FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

ARG NEXT_PUBLIC_API_URL=http://backend-service:5000
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN echo "API_URL INYECTADA: $NEXT_PUBLIC_API_URL"

RUN npm run build

# ---------- RUNTIME ----------
FROM node:18-alpine
WORKDIR /app

# Copiar lo esencial
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules

# Copiar archivos opcionales SIN FALLAR si no existen
RUN mkdir -p public && \
    cp -r /app/public/* public/ 2>/dev/null || echo "Carpeta public no existe → omitida"

RUN cp /app/next.config.js . 2>/dev/null || echo "next.config.js no existe → omitido"
RUN cp /app/tsconfig.json . 2>/dev/null || echo "tsconfig.json no existe → omitido"

EXPOSE 3000

CMD ["npm", "start"]