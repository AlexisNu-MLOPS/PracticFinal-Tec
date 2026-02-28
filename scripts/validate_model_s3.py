"""
Script para validar un modelo guardado en S3.
Descarga temporalmente el modelo y los datos de prueba desde S3, 
calcula las métricas y falla (exit 1) si la precisión (precision) es menor o igual a 0.6.

Uso:
    python scripts/validate_model_s3.py \
        --model-s3 s3://bucket/path/to/model/model.tar.gz \
        --data-s3 s3://bucket/path/to/processed/test.csv \
        --threshold 0.6
"""
import argparse
import sys
import logging
import pandas as pd
import boto3
import tarfile
import tempfile
import joblib
from pathlib import Path
from urllib.parse import urlparse
from sklearn.metrics import precision_score, accuracy_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def parse_s3_uri(uri):
    """Parsea un URI de S3 y devuelve bucket y key."""
    parsed = urlparse(uri)
    if parsed.scheme != "s3":
        raise ValueError(f"El URI debe empezar con s3://, recibido: {uri}")
    return parsed.netloc, parsed.path.lstrip('/')

def download_from_s3(s3_client, uri, local_path):
    """Descarga un archivo de S3 a la ruta local."""
    bucket, key = parse_s3_uri(uri)
    log.info(f"Descargando de S3: s3://{bucket}/{key}")
    s3_client.download_file(bucket, key, str(local_path))
    log.info(f"Guardado temporalmente en: {local_path}")
    return local_path

def parse_args():
    p = argparse.ArgumentParser(description="Validar precisión de modelo desde S3")
    p.add_argument("--model-s3", required=True, help="URI S3 del modelo entrenado (.pkl o .tar.gz)")
    p.add_argument("--data-s3", required=True, help="URI S3 del CSV de evaluación (ej. test.csv o val.csv)")
    p.add_argument("--threshold", type=float, default=0.6, help="Umbral mínimo de Precision")
    return p.parse_args()

def main():
    args = parse_args()
    s3 = boto3.client("s3")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # 1. Descargar Datos de Test
        log.info("1. Preparando Datos de Test...")
        test_csv_path = temp_dir_path / "test.csv"
        download_from_s3(s3, args.data_s3, test_csv_path)
        
        df_test = pd.read_csv(test_csv_path)
        if "Survived" not in df_test.columns:
            log.error("La columna 'Survived' no se encuentra en el set de datos.")
            sys.exit(1)
            
        y_test = df_test.pop("Survived")
        X_test = df_test
        log.info(f"   ✓ Test data loaded: {X_test.shape} features")

        # 2. Descargar y Cargar el Modelo
        log.info("2. Preparando el Modelo...")
        model_local_path = temp_dir_path / "model_downloaded"
        download_from_s3(s3, args.model_s3, model_local_path)
        
        # SageMaker guarda los modelos como model.tar.gz por defecto si no son pasados como raw
        model_file = model_local_path
        if str(args.model_s3).endswith('.tar.gz'):
            with tarfile.open(model_local_path, "r:gz") as tar:
                tar.extractall(path=temp_dir_path)
            # Buscar el archivo .pkl desempaquetado
            pkl_files = list(temp_dir_path.glob("*.pkl"))
            if not pkl_files:
                log.error("No se encontró ningún archivo .pkl dentro del model.tar.gz")
                sys.exit(1)
            model_file = pkl_files[0]
            log.info(f"   ✓ Modelo extraído: {model_file.name}")
            
        model = joblib.load(model_file)
        log.info("   ✓ Modelo cargado en memoria exitosamente")

        # 3. Predicción y Validación
        log.info("3. Evaluando Métricas...")
        y_pred = model.predict(X_test)
        
        precision = precision_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        
        log.info(f"   - Accuracy:  {accuracy:.4f}")
        log.info(f"   - Precision: {precision:.4f}")
        
        log.info("="*50)
        if precision > args.threshold:
            log.info(f"✅ VALIDACIÓN EXITOSA: La precisión ({precision:.4f}) es mayor al umbral ({args.threshold})")
            sys.exit(0)
        else:
            log.error(f"❌ VALIDACIÓN FALLIDA: La precisión ({precision:.4f}) NO supera el umbral ({args.threshold})")
            sys.exit(1)

if __name__ == "__main__":
    main()
