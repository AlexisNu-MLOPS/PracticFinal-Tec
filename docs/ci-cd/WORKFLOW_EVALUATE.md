# 📈 Workflow: Evaluate Model

## Descripción

Workflow para evaluar modelos automáticamente después del entrenamiento o de forma manual.

## Archivo

\`\`\`
.github/workflows/evaluate-model.yml
\`\`\`

## Triggers

### 1. Después de Train Model (workflow_run)
Se ejecuta automáticamente cuando:
- El workflow "Train Model" completa exitosamente

### 2. Manual (workflow_dispatch)
Con parámetro:
- \`model_filename\`: Nombre del modelo a evaluar
  - Default: \`titanic_model_random_forest.pkl\`

## Jobs y Steps

### 1. Checkout Code

### 2. Setup Python 3.10

### 3. Cache Dependencies

### 4. Install Dependencies

### 5. Download Dataset
\`\`\`bash
python scripts/download_data.py
\`\`\`

### 6. Download Trained Model
(Solo si triggered by workflow_run)
Descarga artifact del workflow de training

### 7. Evaluate Model
\`\`\`bash
MODEL_FILE="${{ github.event.inputs.model_filename || 'titanic_model_random_forest.pkl' }}"
python src/evaluate.py --model $MODEL_FILE --use-test
\`\`\`

### 8. Upload Results Artifact
Guarda resultados (30 días):
- \`reports/evaluation_results.json\`
- \`reports/*.png\` (visualizaciones)

### 9. Display Results
Muestra métricas en logs

### 10. Create Summary
JSON con métricas en GitHub UI

### 11. Comment on PR
Si es PR, comenta resultados automáticamente:

\`\`\`markdown
## Model Evaluation Results 📊

- **Accuracy**: 0.8268
- **Precision**: 0.8023
- **Recall**: 0.7692
- **F1 Score**: 0.7854
- **ROC-AUC**: 0.8745
\`\`\`

## Integración con Train Workflow

\`\`\`mermaid
graph LR
    A[Train Workflow] -->|Completa| B[Guarda Artifact]
    B -->|Trigger| C[Evaluate Workflow]
    C -->|Descarga| B
    C --> D[Evalúa Modelo]
    D --> E[Publica Resultados]
\`\`\`

## Artifacts Generados

- \`evaluation-results\`
  - \`evaluation_results.json\`
  - \`confusion_matrix.png\`
  - \`roc_curve.png\`
  - \`feature_importance.png\`

## Ver Resultados

### En GitHub Actions:
- Summary muestra JSON con métricas
- Download artifacts para visualizaciones

### En Pull Request:
- Comentario automático con métricas clave
