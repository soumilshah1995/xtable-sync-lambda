import os
import boto3
import yaml
from pathlib import Path
import jpype
import jpype.imports

s3_client = boto3.client('s3')

def download_config(s3_path, local_path):
    bucket, key = parse_s3_path(s3_path)
    s3_client.download_file(bucket, key, local_path)

def parse_s3_path(s3_path):
    parts = s3_path.replace("s3://", "").split("/", 1)
    return parts[0], parts[1]

# Initialize JVM outside the handler
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[str(Path('/var/task/jars/*'))])

def lambda_handler(event, context):
    try:
        print(f"Received event: {event}")  # Debug print

        # Get S3 path from event
        s3_path = event.get('path')
        if not s3_path:
            raise ValueError("No 'path' provided in the event")

        # Download config file from S3
        local_config_path = '/tmp/config.yaml'
        download_config(s3_path, local_config_path)

        print(f"Config downloaded to: {local_config_path}")  # Debug print

        # Read and parse config
        with open(local_config_path, 'r') as file:
            config = yaml.safe_load(file)

        print(f"Config loaded: {config}")  # Debug print

        # Import Java classes
        RunSync = jpype.JClass("org.apache.xtable.utilities.RunSync")

        print("Running sync...")  # Debug print

        # Run sync
        RunSync.main([
            "--datasetConfig",
            local_config_path
        ])

        return {"status": "Sync completed successfully"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"status": "Error", "message": str(e)}

# Ensure JVM is shut down properly
def lambda_cleanup(event, context):
    if jpype.isJVMStarted():
        jpype.shutdownJVM()