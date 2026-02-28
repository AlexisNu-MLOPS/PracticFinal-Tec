# 📜 Script: download_data.py

## Descripción

Script para descargar automáticamente el dataset del Titanic desde fuentes confiables.

## Ubicación

\`\`\`
scripts/download_data.py
\`\`\`

## Funcionalidad

### Fuentes de Datos

1. **Fuente principal**: Seaborn datasets (vía \`sns.load_dataset('titanic')\`)
2. **Fallback**: GitHub (datasciencedojo/datasets)

### Proceso de Descarga

\`\`\`mermaid
graph TD
    A[Inicio] --> B{¿Archivo existe?}
    B -->|Sí| C[Skip - Ya descargado]
    B -->|No| D[Intentar seaborn]
    D --> E{¿Éxito?}
    E -->|Sí| F[Datos descargados]
    E -->|No| G[Intentar GitHub]
    G --> H{¿Éxito?}
    H -->|Sí| F
    H -->|No| I[Error - Manual download]
    F --> J[Split train/test 80/20]
    J --> K[Guardar CSV]
\`\`\`

## Uso

\`\`\`bash
# Ejecutar script
python scripts/download_data.py
\`\`\`

## Salida

- \`data/raw/train.csv\` - Datos de entrenamiento (80%)
- \`data/raw/test.csv\` - Datos de test (20%)

## Manejo de Errores

Si falla la descarga automática, se puede descargar manualmente desde:
[Kaggle - Titanic Dataset](https://www.kaggle.com/c/titanic/data)

\`\`\`bash
# Colocar archivo descargado en:
mkdir -p data/raw
mv ~/Downloads/train.csv data/raw/
\`\`\`
