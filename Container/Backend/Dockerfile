# ============================================
# Stage 1: Build
# ============================================
FROM python:3.12.3-slim AS builder

# Configurar el modo no interactivo
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bogota

# Instalar dependencias de build
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo requirements.txt primero (para aprovechar cache de Docker)
COPY Backend/requirements.txt .

# Instalar dependencias en un directorio específico
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.12.3-slim

# Configurar el modo no interactivo
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bogota

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar las dependencias instaladas desde el stage builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar el código de la aplicación
COPY Backend/ ./

# Cambiar ownership de los archivos al usuario appuser
RUN chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

# Agregar el directorio de binarios de Python al PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Exponer el puerto que usa FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
