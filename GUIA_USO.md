# 📚 Guía de Uso Detallada - Proyecto Titanic ML

## Índice

- [Requisitos Previos](#requisitos-previos)
- [Instalación Paso a Paso](#instalación-paso-a-paso)
- [Configuración del Entorno](#configuración-del-entorno)
- [Uso Básico](#uso-básico)
- [Uso Avanzado](#uso-avanzado)
- [Personalización](#personalización)
- [Solución de Problemas](#solución-de-problemas)

## Requisitos Previos

### Software Necesario

| Software | Versión Mínima | Propósito |
|----------|----------------|-----------|
| Python | 3.9+ | Lenguaje de programación principal |
| pip | 20.0+ | Gestor de paquetes Python |
| Git | 2.0+ | Control de versiones |

### Conocimientos Recomendados

- ✅ Fundamentos de Python
- ✅ Conceptos básicos de Machine Learning
- ✅ Uso de terminal/línea de comandos
- 📖 Git básico (opcional pero recomendado)

### Sistema Operativo

Compatible con:

- 🐧 Linux (Ubuntu, Debian, Fedora, etc.)
- 🍎 macOS
- 🪟 Windows 10/11 (con Git Bash o WSL recomendado)

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
# Opción A: HTTPS
git clone https://github.com/ivhuco/practica_ci_cd.git
cd practica_ci_cd

# Opción B: SSH (si tienes configurada tu clave SSH)
git clone git@github.com:ivhuco/practica_ci_cd.git
cd practica_ci_cd
```

### 2. Verificar Python

```bash
# Verificar versión de Python
python --version
# o
python3 --version

# Debe mostrar Python 3.9 o superior
```

> [!TIP]
> Si tienes múltiples versiones de Python, asegúrate de usar la versión 3.9+ en todos los comandos.

### 3. Crear Entorno Virtual

**En Linux/macOS:**

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verificar que estás en el entorno virtual
# (debe aparecer (venv) al inicio de tu prompt)
which python
```

**En Windows (CMD):**

```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate.bat
```

**En Windows (PowerShell):**

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**En Windows (Git Bash):**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/Scripts/activate
```

### 4. Instalar Dependencias

```bash
# Actualizar pip a la última versión
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

**Dependencias instaladas:**

- `pandas` - Manipulación de datos
- `numpy` - Operaciones numéricas
- `scikit-learn` - Algoritmos de ML
- `matplotlib` - Visualizaciones
- `seaborn` - Visualizaciones estadísticas
- `pytest` - Framework de testing
- `pytest-cov` - Cobertura de tests
- `flake8` - Linting
- `joblib` - Serialización de modelos

## Configuración del Entorno

### Estructura de Directorios

El proyecto creará automáticamente estos directorios al ejecutarse:

```
practica_ci_cd/
├── data/
│   ├── raw/          # Se crea al descargar datos
│   └── processed/    # Se crea al preprocesar
├── models/           # Se crea al entrenar
└── reports/          # Se crea al evaluar
```

> [!NOTE]
> No necesitas crear estos directorios manualmente, se crean automáticamente.

### Variables de Entorno (Opcional)

Si deseas personalizar rutas, puedes crear un archivo `.env`:

```bash
# .env (opcional)
DATA_PATH=/ruta/personalizada/data
MODEL_PATH=/ruta/personalizada/models
REPORTS_PATH=/ruta/personalizada/reports
```

## Uso Básico

### Opción 1: Pipeline Completo (Recomendado para Comenzar)

Esta es la forma más sencilla de ejecutar todo el proyecto:

```bash
# 1. Descargar datos
python scripts/download_data.py

# 2. Ejecutar pipeline completo (entrena y evalúa)
python scripts/run_pipeline.py
```

**Salida esperada:**

```
============================================================
               TITANIC ML PIPELINE
============================================================

STEP 1: TRAINING MODEL
------------------------------------------------------------
==================================================
TITANIC SURVIVAL PREDICTION - TRAINING
==================================================

1. Loading data...
   ✓ Loaded 891 training samples
   
2. Preprocessing data...
   ✓ Training set: (712, 14)
   ✓ Validation set: (179, 14)
   
3. Creating model (random_forest)...
   ✓ Model created
   
...

STEP 2: EVALUATING MODEL
------------------------------------------------------------
...
```

### Opción 2: Ejecución Paso a Paso

Para mayor control, ejecuta cada paso individualmente:

#### Paso 1: Descargar Datos

```bash
python scripts/download_data.py
```

**Qué hace:**

- Descarga el dataset del Titanic desde seaborn
- Si falla, intenta fuente alternativa (GitHub)
- Crea split train/test (80/20)
- Guarda en `data/raw/`

**Verificar descarga:**

```bash
ls -lh data/raw/
# Debe mostrar:
# train.csv
# test.csv
```

#### Paso 2: Entrenar Modelo

```bash
# Entrenar con configuración por defecto (Random Forest)
python src/train.py

# O especificar parámetros
python src/train.py --model random_forest --val-split 0.2 --cv-folds 5
```

**Parámetros disponibles:**

- `--model`: Tipo de modelo (`random_forest`, `logistic_regression`, `gradient_boosting`)
- `--val-split`: Proporción de validación (default: 0.2)
- `--cv-folds`: Número de folds para validación cruzada (default: 5)

**Salida:**

- Modelo entrenado: `models/titanic_model_random_forest.pkl`
- Métricas: `reports/training_metrics.json`

**Ejemplo de métricas:**

```json
{
  "model_type": "random_forest",
  "train_accuracy": 0.9775,
  "val_accuracy": 0.8268,
  "cv_accuracy_mean": 0.8203,
  "cv_accuracy_std": 0.0234
}
```

#### Paso 3: Evaluar Modelo

```bash
# Evaluar en conjunto de validación
python src/evaluate.py

# Evaluar en conjunto de test
python src/evaluate.py --use-test

# Evaluar modelo específico
python src/evaluate.py --model titanic_model_random_forest.pkl --use-test
```

**Salida:**

- Resultados: `reports/evaluation_results.json`
- Matriz de confusión: `reports/confusion_matrix.png`
- Curva ROC: `reports/roc_curve.png`
- Importancia de features: `reports/feature_importance.png`

**Ver resultados:**

```bash
# Ver métricas en terminal
cat reports/evaluation_results.json | python -m json.tool

# Abrir visualizaciones
open reports/confusion_matrix.png      # macOS
xdg-open reports/confusion_matrix.png  # Linux
start reports/confusion_matrix.png     # Windows
```

## Uso Avanzado

### Experimentación con Diferentes Modelos

#### Random Forest (Default)

```bash
python src/train.py --model random_forest --cv-folds 5
python src/evaluate.py --model titanic_model_random_forest.pkl --use-test
```

**Ventajas:**

- Alta precisión
- Maneja bien no-linealidades
- Feature importance interpretable

**Hiperparámetros (en `src/model.py`):**

- `n_estimators`: 100
- `max_depth`: 10
- `min_samples_split`: 5

#### Logistic Regression

```bash
python src/train.py --model logistic_regression --cv-folds 5
python src/evaluate.py --model titanic_model_logistic_regression.pkl --use-test
```

**Ventajas:**

- Rápido de entrenar
- Interpretable
- Buen baseline

#### Gradient Boosting

```bash
python src/train.py --model gradient_boosting --cv-folds 5
python src/evaluate.py --model titanic_model_gradient_boosting.pkl --use-test
```

**Ventajas:**

- Muy alta precisión
- Robusto
- Maneja bien features complejas

### Comparar Modelos

Script para comparar todos los modelos:

```bash
# Entrenar todos los modelos
for model in random_forest logistic_regression gradient_boosting; do
    echo "Entrenando $model..."
    python src/train.py --model $model
done

# Evaluar todos los modelos
for model in random_forest logistic_regression gradient_boosting; do
    echo "Evaluando titanic_model_$model.pkl..."
    python src/evaluate.py --model titanic_model_$model.pkl --use-test
done

# Ver comparación de métricas
echo "=== COMPARACIÓN DE MODELOS ==="
for model in random_forest logistic_regression gradient_boosting; do
    echo "\n$model:"
    python -c "import json; data=json.load(open('reports/evaluation_results.json')); print(f\"Accuracy: {data['metrics']['accuracy']:.4f}\")"
done
```

### Personalizar Hiperparámetros

Edita `src/model.py` para cambiar hiperparámetros:

```python
# En src/model.py, función create_model()

# Para Random Forest:
default_params = {
    'n_estimators': 200,      # Cambia de 100 a 200
    'max_depth': 15,          # Cambia de 10 a 15
    'min_samples_split': 3,   # Cambia de 5 a 3
    'min_samples_leaf': 1,    # Añade nuevo parámetro
    'random_state': 42,
    'n_jobs': -1
}
```

### Validación Cruzada Detallada

```bash
# Más folds para validación más robusta
python src/train.py --cv-folds 10

# Menos folds para entrenamiento más rápido
python src/train.py --cv-folds 3
```

### Usar Datos Propios

```python
# En un script personalizado
from src.data_loader import load_titanic_data
from src.preprocessing import preprocess_data
from src.model import create_model, save_model

# Cargar tus datos
# Asegúrate que tengan las mismas columnas que el dataset del Titanic
import pandas as pd
custom_train = pd.read_csv('mi_dataset_train.csv')
custom_test = pd.read_csv('mi_dataset_test.csv')

# Preprocesar
processed = preprocess_data(custom_train, custom_test)

# Entrenar
model = create_model('random_forest')
model.fit(processed['X_train'], processed['y_train'])

# Guardar
save_model(model, 'mi_modelo_custom.pkl')
```

## Personalización

### Añadir Nuevas Features

Edita `src/preprocessing.py`, método `create_features()`:

```python
def create_features(self, df):
    """Create engineered features."""
    df = df.copy()
    
    # Features existentes
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    
    # TU NUEVA FEATURE
    df['FarePerPerson'] = df['Fare'] / df['FamilySize']
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 60, 100], 
                            labels=['Child', 'Teen', 'Adult', 'Senior'])
    
    return df
```

### Cambiar Estrategia de Imputación

Edita `src/preprocessing.py`, método `fill_missing_values()`:

```python
def fill_missing_values(self, df):
    """Fill missing values with appropriate strategies."""
    df = df.copy()
    
    # Cambiar de mediana a media para Age
    df['Age'].fillna(df['Age'].mean(), inplace=True)  # Era mediana
    
    # Usar un valor específico para Fare
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    
    return df
```

### Añadir Nuevos Modelos

Edita `src/model.py`, función `create_model()`:

```python
from sklearn.svm import SVC  # Importar nuevo modelo

def create_model(model_type='random_forest', **kwargs):
    # ... código existente ...
    
    elif model_type == 'svm':  # Nuevo modelo
        default_params = {
            'C': 1.0,
            'kernel': 'rbf',
            'random_state': 42
        }
        default_params.update(kwargs)
        return SVC(**default_params)
```

Luego úsalo:

```bash
python src/train.py --model svm
```

## Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests con cobertura
pytest tests/ -v --cov=src --cov-report=html

# Ver reporte de cobertura
open htmlcov/index.html  # macOS
```

### Ejecutar Tests Específicos

```bash
# Solo tests de preprocessing
pytest tests/test_preprocessing.py -v

# Solo tests de modelo
pytest tests/test_model.py -v

# Test específico
pytest tests/test_preprocessing.py::test_fill_missing_values -v
```

### Linting

```bash
# Verificar estilo de código
flake8 src/ tests/ --max-line-length=100

# Errores críticos solamente
flake8 src/ tests/ --select=E9,F63,F7,F82
```

## Solución de Problemas

### Problema: "Module not found"

**Síntoma:**

```
ModuleNotFoundError: No module named 'pandas'
```

**Solución:**

```bash
# Verificar que el entorno virtual está activado
which python  # Debe mostrar ruta con 'venv'

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "File not found: train.csv"

**Síntoma:**

```
FileNotFoundError: Training data not found at data/raw/train.csv
```

**Solución:**

```bash
# Descargar datos primero
python scripts/download_data.py

# Verificar que se descargaron
ls data/raw/
```

### Problema: Error al descargar datos

**Síntoma:**

```
⚠ Could not download dataset automatically
```

**Solución:**

1. Descargar manualmente desde [Kaggle](https://www.kaggle.com/c/titanic/data)
2. Colocar `train.csv` en `data/raw/`
3. Continuar con el entrenamiento

### Problema: Baja precisión del modelo

**Posibles causas y soluciones:**

1. **Falta de datos:**

   ```bash
   # Verificar cantidad de datos
   python -c "import pandas as pd; print(pd.read_csv('data/raw/train.csv').shape)"
   ```

2. **Hiperparámetros subóptimos:**
   - Ajusta hiperparámetros en `src/model.py`
   - Aumenta `n_estimators` o `max_depth`

3. **Overfitting:**

   ```bash
   # Verificar con más validación cruzada
   python src/train.py --cv-folds 10
   
   # Reducir complejidad del modelo
   # Edita src/model.py y reduce max_depth
   ```

### Problema: Tests fallan

**Síntoma:**

```
FAILED tests/test_preprocessing.py::test_something
```

**Solución:**

```bash
# Ver detalles del error
pytest tests/test_preprocessing.py::test_something -v -s

# Verificar que los datos de test están disponibles
ls data/raw/
```

### Problema: GitHub Actions falla

**Verificar:**

1. Logs en GitHub Actions tab
2. Verificar que `requirements.txt` está actualizado
3. Verificar compatibilidad de versiones de Python

```bash
# Probar localmente lo que hace CI
flake8 src/ tests/ --max-line-length=100
pytest tests/ -v
```

### Problema: Error de memoria

**Síntoma:**

```
MemoryError: Unable to allocate array
```

**Solución:**

```bash
# Reducir complejidad del modelo
# En src/model.py, reduce n_estimators

# O procesar en batches más pequeños
python src/train.py --val-split 0.3  # Usa menos datos para training
```

## Comandos de Referencia Rápida

```bash
# Setup inicial
git clone https://github.com/ivhuco/practica_ci_cd.git
cd practica_ci_cd
python -m venv venv
source venv/bin/activate  # O venv\Scripts\activate en Windows
pip install -r requirements.txt

# Pipeline completo
python scripts/download_data.py
python scripts/run_pipeline.py

# Pasos individuales
python scripts/download_data.py
python src/train.py --model random_forest
python src/evaluate.py --use-test

# Testing
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
flake8 src/ tests/ --max-line-length=100

# Comparar modelos
for m in random_forest logistic_regression gradient_boosting; do
    python src/train.py --model $m
    python src/evaluate.py --model titanic_model_$m.pkl --use-test
done

# Limpiar archivos generados
rm -rf data/raw/* data/processed/* models/* reports/*.png
```

## Siguientes Pasos

Una vez que domines el uso básico:

1. 📖 Lee [ARQUITECTURA.md](ARQUITECTURA.md) para entender el diseño
2. 🔍 Explora [docs/modulos/](docs/modulos/) para detalles de cada módulo
3. 🚀 Revisa [docs/ci-cd/](docs/ci-cd/) para automatización
4. 🧪 Añade tus propios tests en `tests/`
5. 🎨 Personaliza features y modelos según tus necesidades

## Recursos Adicionales

- [Documentación de scikit-learn](https://scikit-learn.org/)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Titanic Kaggle Competition](https://www.kaggle.com/c/titanic)
