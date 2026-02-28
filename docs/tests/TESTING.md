# 🧪 Testing

## Descripción General

El proyecto incluye tests unitarios completos para garantizar la calidad y corrección del código.

## Estructura de Tests

\`\`\`
tests/
├── __init__.py
├── test_preprocessing.py  # Tests del preprocessor
└── test_model.py          # Tests de modelos
\`\`\`

## Ejecutar Tests

### Todos los tests
\`\`\`bash
pytest tests/ -v
\`\`\`

### Con cobertura
\`\`\`bash
pytest tests/ -v --cov=src --cov-report=html
\`\`\`

### Ver reporte HTML
\`\`\`bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
\`\`\`

### Test específico
\`\`\`bash
pytest tests/test_preprocessing.py::test_fill_missing_values -v
\`\`\`

## Tests de Preprocessing

Archivo: \`tests/test_preprocessing.py\`

**Tests incluidos**:
- \`test_extract_title\` - Extracción de títulos
- \`test_create_features\` - Feature engineering
- \`test_fill_missing_values\` - Imputación
- \`test_encode_categorical\` - Codificación
- \`test_fit_transform\` - Pipeline completo
- \`test_transform\` - Transformación de datos nuevos

## Tests de Modelo

Archivo: \`tests/test_model.py\`

**Tests incluidos**:
- \`test_create_random_forest\` - Creación de RF
- \`test_create_logistic_regression\` - Creación de LR
- \`test_create_gradient_boosting\` - Creación de GB
- \`test_save_and_load_model\` - Serialización

## Cobertura de Código

Objetivo: > 80% de cobertura

**Verificar cobertura**:
\`\`\`bash
pytest tests/ --cov=src --cov-report=term
\`\`\`

## Linting

### Verificar estilo
\`\`\`bash
flake8 src/ tests/ --max-line-length=100
\`\`\`

### Solo errores críticos
\`\`\`bash
flake8 src/ tests/ --select=E9,F63,F7,F82
\`\`\`

## Añadir Nuevos Tests

### Template de test
\`\`\`python
import pytest
from src.mi_modulo import mi_funcion

def test_mi_funcion():
    """Test de mi_funcion."""
    # Arrange
    input_data = ...
    expected = ...
    
    # Act
    result = mi_funcion(input_data)
    
    # Assert
    assert result == expected
\`\`\`

## CI/CD Integration

Los tests se ejecutan automáticamente en GitHub Actions en cada push/PR.

Ver: [Workflow CI](../ci-cd/WORKFLOW_CI.md)
