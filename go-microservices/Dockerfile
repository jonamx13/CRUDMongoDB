# Etapa de construcción
FROM golang:1.21-alpine AS builder

# Instalar dependencias necesarias
RUN apk add --no-cache git ca-certificates tzdata

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de módulos Go
COPY go.mod go.sum ./

# Descargar dependencias
RUN go mod download

# Copiar código fuente
COPY . .

# Construir aplicación
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/main.go

# Etapa de producción
FROM alpine:latest

# Instalar certificados CA para HTTPS
RUN apk --no-cache add ca-certificates tzdata

# Crear usuario no root
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

WORKDIR /root/

# Copiar binario desde etapa de construcción
COPY --from=builder /app/main .

# Cambiar propiedad del archivo
RUN chown appuser:appgroup main && chmod +x main

# Cambiar a usuario no root
USER appuser

# Exponer puerto
EXPOSE 8080

# Variables de entorno por defecto
ENV GIN_MODE=release
ENV PORT=8080
ENV MONGO_URI=mongodb://mongodb:27017
ENV MONGO_DB=empresa_db
ENV MONGO_COLLECTION=rh

# Comando por defecto
CMD ["./main"]