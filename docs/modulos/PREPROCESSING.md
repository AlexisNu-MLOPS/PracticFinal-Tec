# 🔧 Módulo: Preprocessing

## Descripción General

El módulo `preprocessing.py` implementa el pipeline completo de preprocesamiento para el dataset del Titanic. Transforma datos raw en features listos para Machine Learning mediante feature engineering, imputación,codificación y escalado.

## Ubicación

\`\`\`
src/preprocessing.py
\`\`\`

## Clase Principal: `TitanicPreprocessor`

Implementa el patrón **fit-transform** similar a transformers de scikit-learn, garantizando consistencia entre datos de entrenamiento y test.

### Atributos

\`\`\`python
self.label_encoders = {}      # Encoders para variables categóricas
self.scaler = StandardScaler()  # Scaler para variables numéricas
self.feature_columns = None     # Nombres de columnas finales
\`\`\`

## Pipeline de Preprocesamiento

\`\`\`mermaid
graph LR
    A[Datos Raw] --> B[Feature Engineering]
    B --> C[Imputación]
    C --> D[Codificación]
    D --> E[Selección Features]
    E --> F[Escalado]
    F --> G[Datos ML-Ready]
    
    style A fill:#ffcdd2
    style G fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#fff9c4
\`\`\`

## Métodos Principales

### `extract_title(name)`

Extrae el título del nombre del pasajero.

**Ejemplos de títulos**: Mr, Mrs, Miss, Master, Dr, Rev, etc.

\`\`\`python
title = preprocessor.extract_title("Smith, Mr. John")
# Retorna: 'Mr'
\`\`\`

### `create_features(df)`

Crea nuevas features a partir de las existentes.

**Features creados**:
- \`FamilySize\`: SibSp + Parch + 1
- \`IsAlone\`: 1 si familia size = 1, else 0
- \`Title\`: Título extraído del nombre

\`\`\`python
df_with_features = preprocessor.create_features(df)
\`\`\`

### `fill_missing_values(df)`

Imputa valores faltantes con estrategias específicas.

**Estrategias**:
- **Age**: Mediana por grupo de título
- **Fare**: Mediana general
- **Embarked**: Moda

### `encode_categorical(df, fit=True)`

Codifica variables categóricas.

**Variables codificadas**:
- Sex: Label Encoding (M=1, F=0)
- Embarked: Label Encoding
- Title: One-Hot Encoding

### `fit_transform(df, target_col='Survived')`

Pipeline completo para datos de entrenamiento.

\`\`\`python
X, y = preprocessor.fit_transform(train_df)
\`\`\`

### `transform(df, target_col=None)`

Aplica transformaciones  a datos nuevos.

\`\`\`python
X_test, y_test = preprocessor.transform(test_df, 'Survived')
\`\`\`

## Función de Conveniencia

### `preprocess_data()`

Función all-in-one para preprocesar datasets.

\`\`\`python
from src.preprocessing import preprocess_data

result = preprocess_data(
    train_df,
    test_df=test_df,
    val_split=0.2,
    random_state=42
)

X_train = result['X_train']
y_train = result['y_train']
X_val = result['X_val']
y_val = result['y_val']
\`\`\`

## Ver También

- [📄 data_loader.py](DATA_LOADER.md)
- [📄 train.py](TRAIN.md)
