import os
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

SAGEMAKER_ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT_NAME']
SAGEMAKER_ROLE_NAME = os.environ['SAGEMAKER_ROLE_NAME']

role_name = SAGEMAKER_ROLE_NAME
iam = boto3.client('iam')
response = iam.get_role(RoleName=role_name)
role = response['Role']['Arn']

hub = {
    'HF_MODEL_ID':'mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis',
    'HF_TASK':'text-classification'
}

huggingface_model = HuggingFaceModel(
    transformers_version='4.37.0',
    pytorch_version='2.1.0',
    py_version='py310',
    env=hub,
#     model_data="s3://sagemaker-model-self/model.tar.gz",
    role=role, 
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name=SAGEMAKER_ENDPOINT_NAME, # endpoint name for lambda function
)