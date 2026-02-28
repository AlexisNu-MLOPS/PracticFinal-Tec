# 🚂 Workflow: Train Model

## Descripción

Workflow para entrenar modelos automáticamente de forma manual o programada.

## Archivo

\`\`\`
.github/workflows/train-model.yml
\`\`\`

## Triggers

### 1. Manual (workflow_dispatch)
Con parámetro de entrada:
- \`model_type\`: Tipo de modelo a entrenar
  - Opciones: random_forest, logistic_regression, gradient_boosting
  - Default: random_forest

### 2. Programado (schedule)
Ejecución automática semanal:
- Domingos a las 00:00 UTC
- Cron: \`'0 0 * * 0'\`

## Jobs y Steps

### 1. Checkout Code
Descarga código del repositorio

### 2. Setup Python 3.10
Configura Python

### 3. Cache Dependencies
Cachea dependencias pip

### 4. Install Dependencies
Instala paquetes

### 5. Download Dataset
\`\`\`bash
python scripts/download_data.py
\`\`\`

### 6. Train Model
\`\`\`bash
MODEL_TYPE="${{ github.event.inputs.model_type || 'random_forest' }}"
python src/train.py --model $MODEL_TYPE --val-split 0.2 --cv-folds 5
\`\`\`

### 7. Upload Model Artifact
Guarda modelo como artifact (30 días):
- \`models/*.pkl\`
- \`reports/training_metrics.json\`

### 8. Display Results
Muestra métricas en logs

### 9. Create Summary
Crea summary en GitHub Actions UI

## Ejecutar Manualmente

En GitHub:
1. Ve a "Actions"
2. Selecciona "Train Model"
3. Click "Run workflow"
4. Selecciona modelo y branch
5. Click "Run workflow"

## Artifacts Generados

Descargables desde la página del workflow run:
- \`trained-model\` - Modelo + métricas
- \`training-metrics\` - Solo métricas JSON

## Usar Modelo Entrenado

\`\`\`bash
# Descargar artifact desde GitHub UI
# Extraer archivo
unzip trained-model.zip
mv models/titanic_model_random_forest.pkl ./

# Usar modelo
python src/evaluate.py --model titanic_model_random_forest.pkl
\`\`\`
