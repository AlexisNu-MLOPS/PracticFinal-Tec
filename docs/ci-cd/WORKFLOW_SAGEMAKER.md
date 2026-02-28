# 🔬 SageMaker Processing Pipeline

## ¿Qué hace este workflow?

Lanza automáticamente un **SageMaker Processing Job** en AWS después de que las imágenes Docker se publiquen en ECR. El job toma los datos crudos de S3, los procesa y guarda los resultados listos para entrenar.

## Trigger

Se dispara automáticamente via `workflow_run` cuando:

- El workflow **"Docker Build and Publish to ECR"** completa exitosamente en `main`

También puede ejecutarse manualmente con `workflow_dispatch`.

## Flujo Completo

```
docker-publish.yml completa en main
        ↓
sagemaker-pipeline.yml se dispara
        ↓
1. Configure AWS Credentials    (usa secretos de GitHub)
2. Login to Amazon ECR          (obtiene endpoint del registry)
3. Install boto3
4. Launch SageMaker Processing Job
        ↓
   SageMaker toma la imagen:
   421041021233.dkr.ecr.us-east-1.amazonaws.com/practica-ci-cd:processing-latest
        ↓
   Lee datos crudos de:
   s3://practica.mlops.2026/ejemplo.studio/
        ↓
   Ejecuta src/process.py dentro del contenedor
        ↓
   Guarda datos procesados en:
   s3://practica.mlops.2026/ejemplo.studio/processed/
        │
        ├── train.csv       (80% del dataset, listo para entrenar)
        ├── validation.csv  (20% del dataset, para validar)
        └── test.csv        (si hay CSV de test en el input)
5. Espera a que el job termine  (polling cada 30s)
```

## Configuración

### Variables de entorno (en el workflow)

| Variable | Valor | Descripción |
|---|---|---|
| `AWS_REGION` | `us-east-1` | Región de AWS |
| `ECR_REPOSITORY` | `practica-ci-cd` | Nombre del repo en ECR |
| `S3_INPUT` | `s3://practica.mlops.2026/ejemplo.studio/` | Datos crudos de entrada |
| `S3_OUTPUT` | `s3://practica.mlops.2026/ejemplo.studio/processed/` | Datos procesados de salida |
| `SAGEMAKER_ROLE_ARN` | `arn:aws:iam::421041021233:role/sagemaker-execution-practica-ci-cd` | Rol IAM que asume SageMaker |

### Secretos de GitHub requeridos

| Secreto | Cómo obtenerlo |
|---|---|
| `AWS_ACCESS_KEY_ID` | `terraform output aws_access_key_id` |
| `AWS_SECRET_ACCESS_KEY` | `terraform output -raw aws_secret_access_key` |

## Infraestructura relacionada (Terraform)

El workflow depende de recursos creados por Terraform:

| Recurso Terraform | Usado por |
|---|---|
| `aws_ecr_repository.ml_repo` | Fuente de la imagen de processing |
| `aws_iam_role.sagemaker_execution` | Rol que SageMaker asume (ARN hardcodeado en el workflow) |
| `aws_iam_role_policy.sagemaker_s3` | Permite al job leer/escribir en S3 |
| `aws_iam_role_policy.sagemaker_ecr` | Permite al job hacer pull de la imagen |
| `aws_iam_user.github_actions` | Se autentifica con los secretos de GitHub |
| `aws_iam_user_policy.github_sagemaker` | Le da permisos al usuario para lanzar Processing Jobs |

## Script de lanzamiento

El workflow ejecuta [`scripts/launch_processing_job.py`](../../scripts/launch_processing_job.py), que:

1. Llama a `sagemaker.create_processing_job()` via boto3
2. Configura el canal de input (S3 → `/opt/ml/processing/input/raw/`)
3. Configura el canal de output (`/opt/ml/processing/output/` → S3)
4. Espera con polling cada 30s hasta que el job termine
5. Sale con código de error si el job falla

## 🚧 Ejercicio para alumnos: Training Job

El siguiente paso del pipeline (Training Job) está **pendiente**. Ver la sección [🎓 Ejercicio para Alumnos](../../README.md#-ejercicio-para-alumnos) en el README.
