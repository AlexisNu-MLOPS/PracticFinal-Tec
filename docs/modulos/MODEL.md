# 🤖 Módulo: Model

## Descripción General

El módulo `model.py` gestiona la creación, configuración, guardado y carga de modelos de Machine Learning.

## Modelos Soportados

| Modelo | Tipo | Ventajas | Tiempo |
|--------|------|----------|---------|
| **random_forest** | Random Forest Classifier | Alta precisión, interpretable | ~10s |
| **logistic_regression** | Logistic Regression | Rápido, baseline | ~1s |
| **gradient_boosting** | Gradient Boosting | Máxima precisión | ~30s |

## Funciones Principales

### `create_model(model_type, **kwargs)`

Factory para crear modelos con hiperparámetros.

\`\`\`python
from src.model import create_model

# Random Forest con parámetros por defecto
model = create_model('random_forest')

# Con parámetros custom
model = create_model('random_forest', n_estimators=200, max_depth=15)
\`\`\`

**Parámetros por defecto**:

**Random Forest**:
\`\`\`python
{
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42,
    'n_jobs': -1
}
\`\`\`

### `save_model(model, filename)`

Serializa modelo con joblib.

\`\`\`python
from src.model import save_model

save_model(model, 'mi_modelo.pkl')
# Guarda en: models/mi_modelo.pkl
\`\`\`

### `load_model(filename)`

Carga modelo desde archivo.

\`\`\`python
from src.model import load_model

model = load_model('mi_modelo.pkl')
predictions = model.predict(X_test)
\`\`\`

## Ejemplo Completo

\`\`\`python
from src.model import create_model, save_model, load_model
from src.data_loader import load_titanic_data
from src.preprocessing import preprocess_data

# Cargar y preprocesar
train_df, _ = load_titanic_data()
processed = preprocess_data(train_df)
X_train, y_train = processed['X_train'], processed['y_train']

# Crear y entrenar modelo
model = create_model('random_forest', n_estimators=200)
model.fit(X_train, y_train)

# Guardar
save_model(model, 'titanic_model_rf.pkl')

# Cargar en otro momento
loaded_model = load_model('titanic_model_rf.pkl')
score = loaded_model.score(X_train, y_train)
print(f"Accuracy: {score:.4f}")
\`\`\`

## Ver También

- [📄 train.py](TRAIN.md)
- [📄 evaluate.py](EVALUATE.md)
