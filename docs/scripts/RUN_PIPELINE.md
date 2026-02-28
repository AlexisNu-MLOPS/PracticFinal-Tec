# 📜 Script: run_pipeline.py

## Descripción

Script orquestador que ejecuta el pipeline completo end-to-end: entrenamiento y evaluación.

## Ubicación

\`\`\`
scripts/run_pipeline.py
\`\`\`

## Funcionalidad

Ejecuta en secuencia:
1. Entrenamiento del modelo (train.py)
2. Evaluación del modelo (evaluate.py)

## Uso

\`\`\`bash
python scripts/run_pipeline.py
\`\`\`

## Flujo de Ejecución

\`\`\`mermaid
sequenceDiagram
    participant Script
    participant Train
    participant Evaluate
    participant Filesystem
    
    Script->>Train: train_model()
    Train->>Filesystem: Guardar modelo
    Train->>Filesystem: Guardar métricas train
    Train-->>Script: Métricas
    
    Script->>Evaluate: evaluate_model()
    Evaluate->>Filesystem: Cargar modelo
    Evaluate->>Filesystem: Guardar resultados
    Evaluate->>Filesystem: Guardar visualizaciones
    Evaluate-->>Script: Resultados
    
    Script-->>Script: Pipeline completo!
\`\`\`

## Salida Esperada

\`\`\`
============================================================
               TITANIC ML PIPELINE
============================================================

STEP 1: TRAINING MODEL
------------------------------------------------------------
[Training output...]
✓ Model saved: models/titanic_model_random_forest.pkl

STEP 2: EVALUATING MODEL
------------------------------------------------------------
[Evaluation output...]
✓ Results saved: reports/evaluation_results.json

============================================================
                    PIPELINE COMPLETE!
============================================================

📊 Check the 'reports/' directory for detailed results
🤖 Trained model saved in 'models/' directory
\`\`\`

## Personalización

Puedes modificar el script para:
- Entrenar múltiples modelos
- Usar diferentes configuraciones
- Añadir pasos adicionales

\`\`\`python
# Ejemplo de personalización
def main():
    # Entrenar múltiples modelos
    for model_type in ['random_forest', 'logistic_regression', 'gradient_boosting']:
        print(f"\\nTraining {model_type}...")
        train_model(model_type=model_type)
        evaluate_model(model_filename=f'titanic_model_{model_type}.pkl')
\`\`\`
