"""
Script para lanzar un SageMaker Processing Job.
Lee datos crudos de S3 y guarda los datos procesados en S3.

Uso:
    python scripts/launch_processing_job.py \
        --image <ecr-uri>:processing-latest \
        --role <sagemaker-execution-role-arn> \
        --input-s3 s3://bucket/path/to/raw/ \
        --output-s3 s3://bucket/path/to/processed/
"""
import argparse
import datetime
import logging
import sys
import time

import boto3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

REGION = "us-east-1"


def parse_args():
    p = argparse.ArgumentParser(description="Launch SageMaker Processing Job")
    p.add_argument("--image", required=True, help="ECR image URI (processing stage)")
    p.add_argument("--role", required=True, help="SageMaker execution IAM role ARN")
    p.add_argument(
        "--input-s3", required=True,
        help="S3 URI of the raw dataset (file or prefix)"
    )
    p.add_argument(
        "--output-s3", required=True,
        help="S3 URI prefix where processed CSVs will be saved"
    )
    p.add_argument(
        "--instance-type", default="ml.t3.medium",
        help="SageMaker instance type (default: ml.t3.medium)"
    )
    p.add_argument(
        "--wait", action="store_true", default=True,
        help="Wait for job to complete (default: True)"
    )
    return p.parse_args()


def launch_processing_job(args):
    sm = boto3.client("sagemaker", region_name=REGION)

    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    job_name = f"titanic-processing-{ts}"

    log.info("Launching SageMaker Processing Job: %s", job_name)
    log.info("  Image      : %s", args.image)
    log.info("  Role       : %s", args.role)
    log.info("  Input  (S3): %s", args.input_s3)
    log.info("  Output (S3): %s", args.output_s3)
    log.info("  Instance   : %s", args.instance_type)

    sm.create_processing_job(
        ProcessingJobName=job_name,
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": args.instance_type,
                "VolumeSizeInGB": 10,
            }
        },
        AppSpecification={
            "ImageUri": args.image,
            # process.py es el ENTRYPOINT de la imagen; no se necesita ContainerEntrypoint
        },
        RoleArn=args.role,
        ProcessingInputs=[
            {
                "InputName": "raw",
                "S3Input": {
                    "S3Uri": args.input_s3,
                    # Si el URI apunta a un archivo, SageMaker lo descarga como archivo
                    "LocalPath": "/opt/ml/processing/input/raw",
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                },
            }
        ],
        ProcessingOutputConfig={
            "Outputs": [
                {
                    "OutputName": "processed",
                    "S3Output": {
                        "S3Uri": args.output_s3,
                        "LocalPath": "/opt/ml/processing/output",
                        "S3UploadMode": "EndOfJob",
                    },
                }
            ]
        },
    )

    log.info("Job submitted: %s", job_name)
    print(f"::set-output name=job_name::{job_name}")   # GitHub Actions output

    if not args.wait:
        return job_name

    # Esperar a que termine
    log.info("Waiting for job to complete …")
    while True:
        response = sm.describe_processing_job(ProcessingJobName=job_name)
        status = response["ProcessingJobStatus"]
        log.info("  Status: %s", status)

        if status == "Completed":
            log.info("✅ Processing Job completed successfully.")
            return job_name
        elif status in ("Failed", "Stopped"):
            reason = response.get("FailureReason", "unknown")
            log.error("❌ Processing Job %s: %s", status, reason)
            sys.exit(1)

        time.sleep(30)


if __name__ == "__main__":
    args = parse_args()
    launch_processing_job(args)
