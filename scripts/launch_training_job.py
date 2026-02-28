"""
Script para lanzar un SageMaker Training Job.
Lee datos desde un canal de S3 (input) y guarda el modelo resultante en S3.

Uso:
    python scripts/launch_training_job.py \
        --image <ecr-uri>:train-latest \
        --role <sagemaker-execution-role-arn> \
        --input-s3 s3://bucket/path/to/train/ \
        --output-s3 s3://bucket/path/to/model/
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
    p = argparse.ArgumentParser(description="Launch SageMaker Training Job")
    p.add_argument("--image", required=True, help="ECR image URI (train stage)")
    p.add_argument("--role", required=True, help="SageMaker execution IAM role ARN")
    p.add_argument(
        "--input-s3", required=True,
        help="S3 URI prefix where training data is located"
    )
    p.add_argument(
        "--output-s3", required=True,
        help="S3 URI prefix where the model will be saved"
    )
    p.add_argument(
        "--instance-type", default="ml.m5.large",
        help="SageMaker instance type (default: ml.m5.large)"
    )
    p.add_argument(
        "--wait", action="store_true", default=True,
        help="Wait for job to complete (default: True)"
    )
    return p.parse_args()


def launch_training_job(args):
    sm = boto3.client("sagemaker", region_name=REGION)

    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    job_name = f"titanic-training-{ts}"

    log.info("Launching SageMaker Training Job: %s", job_name)
    log.info("  Image      : %s", args.image)
    log.info("  Role       : %s", args.role)
    log.info("  Input  (S3): %s", args.input_s3)
    log.info("  Output (S3): %s", args.output_s3)
    log.info("  Instance   : %s", args.instance_type)

    sm.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            "TrainingImage": args.image,
            "TrainingInputMode": "File",
        },
        RoleArn=args.role,
        InputDataConfig=[
            {
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": args.input_s3,
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
                # SageMaker maps this to /opt/ml/input/data/train inside the container
            }
        ],
        OutputDataConfig={
            # SageMaker will upload /opt/ml/model to this S3 path as a model.tar.gz
            "S3OutputPath": args.output_s3,
        },
        ResourceConfig={
            "InstanceType": args.instance_type,
            "InstanceCount": 1,
            "VolumeSizeInGB": 10,
        },
        StoppingCondition={
            "MaxRuntimeInSeconds": 3600,
        },
    )

    log.info("Job submitted: %s", job_name)
    print(f"::set-output name=job_name::{job_name}")   # GitHub Actions output

    if not args.wait:
        return job_name

    # Esperar a que termine
    log.info("Waiting for job to complete …")
    while True:
        response = sm.describe_training_job(TrainingJobName=job_name)
        status = response["TrainingJobStatus"]
        log.info("  Status: %s", status)

        if status == "Completed":
            log.info("✅ Training Job completed successfully.")
            return job_name
        elif status in ("Failed", "Stopped"):
            reason = response.get("FailureReason", "unknown")
            log.error("❌ Training Job %s: %s", status, reason)
            sys.exit(1)

        time.sleep(30)


if __name__ == "__main__":
    args = parse_args()
    launch_training_job(args)
