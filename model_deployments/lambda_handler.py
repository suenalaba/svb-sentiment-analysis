import os
import boto3
import json

SAGEMAKER_ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    data = json.dumps(event)
    response = runtime.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT_NAME,
        ContentType='application/json',
        Accept='application/json',
        Body=data
    )
    response_json = json.loads(response['Body'].read().decode())
    predicted_label = response_json[0]['label'].upper()
    return {
        "predicted_label" :predicted_label
    }