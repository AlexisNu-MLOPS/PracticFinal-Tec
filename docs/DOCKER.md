# 🐳 Guía de Docker

Esta guía explica cómo usar Docker para ejecutar el proyecto Titanic ML en contenedores.

## 📋 Tabla de Contenidos

- [Prerequisitos](#prerequisitos)
- [Estructura de Docker](#estructura-de-docker)
- [Construcción de Imágenes](#construcción-de-imágenes)
- [Uso con Docker](#uso-con-docker)
- [Uso con Docker Compose](#uso-con-docker-compose)
- [Comandos Útiles](#comandos-útiles)
- [Troubleshooting](#troubleshooting)

---

## Prerequisitos

- **Docker**: Versión 20.10+ ([Descargar Docker](https://www.docker.com/get-started))
- **Docker Compose**: Versión 2.0+ (incluido con Docker Desktop)

Verificar instalación:

```bash
docker --version
docker-compose --version
```

---

## Estructura de Docker

El proyecto utiliza un **Dockerfile multi-stage** con 4 etapas:

### 1. `base`

Imagen base con Python 3.10 y dependencias del sistema.

### 2. `development`

Imagen para desarrollo con todo el código fuente y herramientas.

### 3. `train`

Imagen especializada para entrenar modelos.

### 4. `production`

Imagen ligera optimizada para producción/evaluación.

---

## Construcción de Imágenes

### Opción 1: Construcción manual con Docker

#### Imagen de desarrollo

```bash
docker build --target development -t titanic-ml:dev .
```

#### Imagen de entrenamiento

```bash
docker build --target train -t titanic-ml:train .
```

#### Imagen de producción

```bash
docker build --target production -t titanic-ml:prod .
```

### Opción 2: Construcción con Docker Compose

```bash
# Construir todos los servicios
docker-compose build

# Construir un servicio específico
docker-compose build dev
docker-compose build train
docker-compose build evaluate
```

---

## Uso con Docker

### 1. Desarrollo Interactivo

```bash
# Iniciar contenedor de desarrollo
docker run -it --rm \
  -v $(pwd):/app \
  titanic-ml:dev bash

# Dentro del contenedor, puedes ejecutar:
python scripts/download_data.py
python src/train.py
python src/evaluate.py --model models/titanic_model_random_forest.pkl --use-test
pytest tests/ -v
```

### 2. Entrenar Modelo

```bash
# Entrenar y guardar modelo
docker run --rm \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/reports:/app/reports \
  titanic-ml:train
```

### 3. Evaluar Modelo

```bash
# Evaluar modelo existente
docker run --rm \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/reports:/app/reports \
  titanic-ml:prod
```

### 4. Ejecutar Tests

```bash
docker run --rm \
  -v $(pwd):/app \
  titanic-ml:dev \
  pytest tests/ -v --cov=src
```

---

## Uso con Docker Compose

Docker Compose simplifica la orquestación de múltiples contenedores.

### Comandos Principales

#### Desarrollo

```bash
# Iniciar entorno de desarrollo
docker-compose up dev

# Ejecutar comandos en el contenedor de desarrollo
docker-compose run --rm dev python src/train.py
docker-compose run --rm dev bash
```

#### Entrenamiento

```bash
# Entrenar modelo
docker-compose up train

# O ejecutar en background
docker-compose up -d train

# Ver logs
docker-compose logs -f train
```

#### Evaluación

```bash
# Evaluar modelo (requiere que train haya completado)
docker-compose up evaluate
```

#### Testing

```bash
# Ejecutar todos los tests
docker-compose up test

# Ver resultados
docker-compose run --rm test pytest tests/ -v
```

#### Pipeline Completo

```bash
# Ejecutar entrenamiento y evaluación en secuencia
docker-compose up train evaluate
```

### Gestión de Volúmenes

Los datos persisten en volúmenes Docker:

```bash
# Listar volúmenes
docker volume ls | grep titanic

# Inspeccionar volumen
docker volume inspect titanic_ml_models

# Limpiar volúmenes
docker-compose down -v
```

---

## Comandos Útiles

### Ver Imágenes

```bash
docker images | grep titanic-ml
```

### Ver Contenedores Activos

```bash
docker ps
docker-compose ps
```

### Logs

```bash
# Docker
docker logs <container_id>

# Docker Compose
docker-compose logs -f train
```

### Limpiar Recursos

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar también volúmenes
docker-compose down -v

# Eliminar imágenes
docker rmi titanic-ml:dev titanic-ml:train titanic-ml:prod

# Limpiar todo (usar con cuidado)
docker system prune -a
```

### Acceso a Shell

```bash
# Docker
docker exec -it <container_id> bash

# Docker Compose
docker-compose exec dev bash
```

---

## Troubleshooting

### Problema: Error de permisos

**Síntoma:** No se pueden escribir archivos en volúmenes.

**Solución:**

```bash
# Opción 1: Ejecutar con tu usuario
docker run --rm --user $(id -u):$(id -g) -v $(pwd):/app titanic-ml:dev

# Opción 2: Cambiar permisos después
sudo chown -R $USER:$USER models/ reports/ data/
```

### Problema: Imagen muy grande

**Síntoma:** La imagen de Docker es muy pesada.

**Solución:**

```bash
# Usar multi-stage builds (ya implementado)
# Limpiar cache de pip
docker build --no-cache -t titanic-ml:prod .

# Ver tamaño de capas
docker history titanic-ml:prod
```

### Problema: Cambios en código no se reflejan

**Síntoma:** Modificaciones al código no aparecen en el contenedor.

**Solución:**

```bash
# Asegúrate de usar volúmenes para desarrollo
docker-compose run --rm dev bash

# O reconstruir la imagen
docker-compose build dev
```

### Problema: Puerto ocupado

**Síntoma:** Error al iniciar contenedor por puerto en uso.

**Solución:**

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # host:container

# O detener el proceso que usa el puerto
lsof -ti:8000 | xargs kill -9
```

---

## Mejores Prácticas

### 1. **Desarrollo Local**

- Usa volúmenes para montar el código fuente
- El servicio `dev` incluye todas las herramientas

### 2. **CI/CD**

- Usa la imagen `production` optimizada
- Monta solo volúmenes necesarios (models, reports)

### 3. **Caché de Construcción**

- Las dependencias se instalan primero para aprovechar caché
- Cambios en código no invalidan caché de pip

### 4. **Seguridad**

- La imagen de producción usa un usuario no-root (`mluser`)
- Minimiza la superficie de ataque con imágenes slim

### 5. **Tamaño de Imagen**

- Base: `python:3.10-slim` (~150MB)
- Development: ~800MB (con todas las dependencias)
- Production: ~600MB (optimizada)

---

## Integración con GitHub Actions

Puedes crear un workflow para publicar imágenes:

```yaml
# .github/workflows/docker-publish.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t titanic-ml:latest .
      
      - name: Push to Docker Hub
        # Configurar credenciales y push
```

---

## Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
