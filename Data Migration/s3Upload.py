#code to upload a file from the computer to the S3 bucket

import logging
import boto3
from botocore.exceptions import ClientError
import os

def upload_file(file_path):

    bucket_name = "staging-ride-life-path-info"
    access_key = "REDACTED"
    secret_key = "REDACTED"

    s3 = boto3.client(service_name="s3", 
            aws_access_key_id=access_key, 
            aws_secret_access_key=secret_key
    )
    response = s3.upload_file(file_path, bucket_name, file_path)
    print(f"upload_log_to_aws response: {response}")
    if response is None:
        print("Success")
    else:
        print("Error")