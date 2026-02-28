# 🔄 Workflow: CI - Testing y Linting

## Descripción

Workflow de Integración Continua que ejecuta tests y linting automáticamente en cada push o pull request.

## Archivo

\`\`\`
.github/workflows/ci.yml
\`\`\`

## Triggers

- **Push** a branches: \`main\`, \`develop\`
- **Pull Request** a branches: \`main\`, \`develop\`

## Matriz de Python

Ejecuta tests en múltiples versiones de Python:
- Python 3.9
- Python 3.10
- Python 3.11

## Jobs y Steps

### 1. Checkout Code
Descarga el código del repositorio

### 2. Setup Python
Configura la versión de Python según la matriz

### 3. Cache Dependencies
Cachea dependencias de pip para acelerar builds

### 4. Install Dependencies
Instala paquetes desde \`requirements.txt\`

### 5. Lint with flake8
\`\`\`bash
# Errores críticos (build falla)
flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source

# Warnings (no falla el build)
flake8 src/ tests/ --count --max-line-length=100 --exit-zero
\`\`\`

### 6. Run Tests
\`\`\`bash
pytest tests/ -v --cov=src --cov-report=xml --cov-report=term
\`\`\`

### 7. Upload Coverage
Sube reporte de cobertura a Codecov

### 8. Generate HTML Report
Genera reporte HTML de cobertura (solo Python 3.10)

### 9. Upload Artifact
Sube reporte HTML como artifact

## Visualización del Flujo

\`\`\`mermaid
graph TD
    A[Push/PR] --> B[Checkout]
    B --> C[Setup Python 3.9]
    B --> D[Setup Python 3.10]
    B --> E[Setup Python 3.11]
    
    C --> F1[Lint 3.9]
    D --> F2[Lint 3.10]
    E --> F3[Lint 3.11]
    
    F1 --> G1[Test 3.9]
    F2 --> G2[Test 3.10]
    F3 --> G3[Test 3.11]
    
    G1 --> H1[Coverage 3.9]
    G2 --> H2[Coverage 3.10]
    G3 --> H3[Coverage 3.11]
    
    H2 --> I[Upload HTML]
\`\`\`

## Ver Resultados

En GitHub:
1. Ve a la tab "Actions"
2. Selecciona el workflow "CI - Testing and Linting"
3. Ver resultados de cada job

## Solución de Problemas

### Lint Falla
\`\`\`bash
# Ejecutar localmente
flake8 src/ tests/ --max-line-length=100
\`\`\`

### Tests Fallan
\`\`\`bash
# Ejecutar localmente
pytest tests/ -v
\`\`\`
