# 🎓 Módulo: Train

## Descripción General

El módulo `train.py` implementa el proceso completo de entrenamiento de modelos con validación cruzada y métricas detalladas.

## Función Principal: `train_model()`

\`\`\`python
def train_model(
    model_type='random_forest',
    val_split=0.2,
    cv_folds=5
) -> dict
\`\`\`

**Parámetros**:
- \`model_type\`: Tipo de modelo ('random_forest', 'logistic_regression', 'gradient_boosting')
- \`val_split\`: Proporción de validación (default: 0.2 = 20%)
- \`cv_folds\`: Número de folds para cross-validation (default: 5)

**Retorna**:
Dict con métricas de entrenamiento

## Proceso de Entrenamiento

\`\`\`mermaid
graph TD
    A[Cargar Datos] --> B[Preprocesar]
    B --> C[Crear Modelo]
    C --> D[Cross-Validation]
    D --> E[Entrenar en Set Completo]
    E --> F[Evaluar en Train]
    F --> G[Evaluar en Validación]
    G --> H[Feature Importance]
    H --> I[Guardar Modelo]
    I --> J[Guardar Métricas]
\`\`\`

## Uso desde Terminal

\`\`\`bash
# Entrenamiento básico
python src/train.py

# Especificar modelo
python src/train.py --model gradient_boosting

# Personalizar validación
python src/train.py --model random_forest --val-split 0.3 --cv-folds 10
\`\`\`

## Uso Programático

\`\`\`python
from src.train import train_model

# Entrenar modelo
metrics = train_model(
    model_type='random_forest',
    val_split=0.2,
    cv_folds=5
)

print(f"Train Accuracy: {metrics['train_accuracy']:.4f}")
print(f"Val Accuracy: {metrics['val_accuracy']:.4f}")
print(f"CV Accuracy: {metrics['cv_accuracy_mean']:.4f} ± {metrics['cv_accuracy_std']:.4f}")
\`\`\`

## Salidas Generadas

### Modelo Entrenado

Guardado en: \`models/titanic_model_{model_type}.pkl\`

### Métricas

Guardado en: \`reports/training_metrics.json\`

**Estructura**:
\`\`\`json
{
  "model_type": "random_forest",
  "train_accuracy": 0.9775,
  "val_accuracy": 0.8268,
  "cv_accuracy_mean": 0.8203,
  "cv_accuracy_std": 0.0234,
  "cv_scores": [0.82, 0.85, 0.80, 0.83, 0.81],
  "n_features": 14,
  "n_train_samples": 712,
  "n_val_samples": 179,
  "feature_importance": {
    "Sex": 0.254,
    "Title": 0.187,
    ...
  }
}
\`\`\`

## Validación Cruzada

El script utiliza **k-fold stratified cross-validation**:

- Divide datos en k folds
- Entrena k modelos (cada uno excluyendo un fold)
- Calcula accuracy en cada fold
- Reporta media y desviación estándar

**Beneficios**:
- Estimación robusta del rendimiento
- Reduce varianza
- Detecta overfitting

## Feature Importance

Para modelos basados en árboles (Random Forest, Gradient Boosting), se calcula y muestra la importancia de cada feature.

**Ejemplo de salida**:
\`\`\`
Top 10 feature importances:
   1. Sex: 0.2540
   2. Title: 0.1870
   3. Fare: 0.1530
   4. Age: 0.1280
   5. Pclass: 0.1120
   ...
\`\`\`

## Ver También

- [📄 model.py](MODEL.md)
- [📄 evaluate.py](EVALUATE.md)
- [📄 preprocessing.py](PREPROCESSING.md)
