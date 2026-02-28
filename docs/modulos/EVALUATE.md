# 📊 Módulo: Evaluate

## Descripción General

El módulo `evaluate.py` implementa la evaluación completa de modelos entrenados, generando métricas y visualizaciones.

## Función Principal: `evaluate_model()`

\`\`\`python
def evaluate_model(
    model_filename='titanic_model_random_forest.pkl',
    use_test=True
) -> dict
\`\`\`

**Parámetros**:
- \`model_filename\`: Nombre del archivo del modelo a evaluar
- \`use_test\`: Si True usa conjunto de test, si False usa validación

## Métricas Calculadas

| Métrica | Descripción | Rango |
|---------|-------------|--------|
| **Accuracy** | Proporción de predicciones correctas | 0-1 |
| **Precision** | Precisión de predicciones positivas | 0-1 |
| **Recall** | Sensibilidad, tasa de verdaderos positivos | 0-1 |
| **F1-Score** | Media armónica de precisión y recall | 0-1 |
| **ROC-AUC** | Área bajo la curva ROC | 0-1 |

## Visualizaciones Generadas

### 1. Confusion Matrix
\`reports/confusion_matrix.png\`

Muestra:
- True Positives (TP)
- True Negatives (TN)
- False Positives (FP)
- False Negatives (FN)

### 2. ROC Curve
\`reports/roc_curve.png\`

Curva de Característica Operativa del Receptor mostrando trade-off entre sensibilidad y especificidad.

### 3. Feature Importance
\`reports/feature_importance.png\`

Top 15 features más importantes según el modelo.

## Uso desde Terminal

\`\`\`bash
# Evaluar en validación
python src/evaluate.py

# Evaluar en test
python src/evaluate.py --use-test

# Evaluar modelo específico
python src/evaluate.py --model titanic_model_gradient_boosting.pkl --use-test
\`\`\`

## Uso Programático

\`\`\`python
from src.evaluate import evaluate_model

# Evaluar modelo
results = evaluate_model(
    model_filename='titanic_model_random_forest.pkl',
    use_test=True
)

print(f"Accuracy: {results['metrics']['accuracy']:.4f}")
print(f"F1-Score: {results['metrics']['f1_score']:.4f}")
print(f"ROC-AUC: {results['metrics']['roc_auc']:.4f}")
\`\`\`

## Salidas Generadas

### Resultados JSON
\`reports/evaluation_results.json\`

\`\`\`json
{
  "model_filename": "titanic_model_random_forest.pkl",
  "evaluation_set": "Test",
  "n_samples": 179,
  "n_features": 14,
  "metrics": {
    "accuracy": 0.8268,
    "precision": 0.8023,
    "recall": 0.7692,
    "f1_score": 0.7854,
    "roc_auc": 0.8745
  },
  "confusion_matrix": [[95, 15], [20, 49]],
  "classification_report": {...}
}
\`\`\`

## Classification Report

Reporte detallado por clase:

\`\`\`
              precision    recall  f1-score   support

Not Survived       0.83      0.86      0.85       110
    Survived       0.77      0.73      0.75        69

    accuracy                           0.81       179
   macro avg       0.80      0.80      0.80       179
weighted avg       0.81      0.81      0.81       179
\`\`\`

## Interpretar Resultados

### Accuracy
- **> 80%**: Excelente
- **70-80%**: Bueno
- **< 70%**: Mejorable

### Precision vs Recall
- **Alta Precision**: Pocas falsas alarmas
- **Alto Recall**: Pocas predicciones perdidas
- **F1-Score**: Balance entre ambos

### ROC-AUC
- **> 0.9**: Excelente
- **0.8-0.9**: Muy bueno
- **0.7-0.8**: Aceptable
- **< 0.7**: Pobre

## Ver También

- [📄 train.py](TRAIN.md)
- [📄 model.py](MODEL.md)
