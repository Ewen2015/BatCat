#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import os
import json
import time
from time import gmtime, strftime
import pickle
import boto3
import joblib
import tarfile
import sagemaker
from sagemaker.estimator import Estimator
import subprocess


def save_model(model, model_name='model', model_suffix='.joblib'):
    model_path = model_name + model_suffix
    with open(model_path, 'wb') as f:
        joblib.dump(model, f)
    return None

def template_inference():
    """Generate a template Python script for inference. This helps SageMaker understand how your input and output for your model serving will be configured.

    Args:
        None
    Yields:
        A template AWS SageMaker inference file to the current directory. 
    """

    template = \
"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import joblib
import os
import json


def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        request_body = json.loads(request_body)
        inpVar = request_body['Input']
        return inpVar
    else:
        raise ValueError("This model only supports application/json input")

        
def predict_fn(input_data, model):
    return model.predict(input_data)


def output_fn(prediction, content_type):
    res = prediction[0]
    respJSON = {'Output': res}
    return respJSON
"""
    
    with open('inference.py', 'w') as writer:
        writer.write(template)

    return None

def upload_model_to_s3(model_name='model', model_suffix='.joblib', bucket='[project]'):
    boto_session = boto3.session.Session()
    s3 = boto_session.resource('s3')
    
    model_path = model_name + model_suffix
    
    # Build tar file with model data + inference code
    bashCommand = f"tar -cvpzf {model_name}.tar.gz {model_path} inference.py"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Upload tar.gz to bucket
    key_model = f"model/{model_name}.tar.gz"
    model_artifacts = f"s3://{bucket}/{key_model}"
    
    response = s3.meta.client.upload_file(f'{model_name}.tar.gz', bucket, key_model)
    return model_artifacts


def deploy_model(model, 
                 model_name='model',
                 project='[project]',
                 role='arn:aws-cn:iam::[account-id]:role/[role-name]'):
    """ Deploy a SKLearn model to SageMaker Endpoint.
    
    Args:
        model: An SKLearn model.
        model_name (str): The model name.
        project (str): The project name, which is also the S3 bucket name in BatCat convention.
        role (str): The Execution Role ARN, which should include S3 Full Access, SageMaker Full Access, and ECR Full Access.
    Return:
        None
    """
    
    ## Model Setup    
    save_model(model=model)
    template_inference()
    model_artifacts = upload_model_to_s3(bucket=project)
    
    ## SKLearn Image Setup
    client = boto3.client(service_name="sagemaker")
    runtime = boto3.client(service_name="sagemaker-runtime")
    boto_session = boto3.session.Session()
    region = boto_session.region_name
    sagemaker_session = sagemaker.Session()
    
    # retrieve sklearn image
    image_uri = sagemaker.image_uris.retrieve(
        framework="sklearn",
        region=region,
        version="0.23-1",
        py_version="py3",
        instance_type="ml.m5.xlarge",
    )

    ## Deploy Endpoint
    #Step 1: Model Creation
    model_name = model_name.upper() + strftime("-%Y%m%d-%H%M%S", gmtime())
    print("Model name: " + model_name)
    create_model_response = client.create_model(
        ModelName=model_name,
        Containers=[
            {
                "Image": image_uri,
                "Mode": "SingleModel",
                "ModelDataUrl": model_artifacts,
                "Environment": {'SAGEMAKER_SUBMIT_DIRECTORY': model_artifacts,
                               'SAGEMAKER_PROGRAM': 'inference.py'} 
            }
        ],
        ExecutionRoleArn=role,
    )
    print("Model Arn: " + create_model_response["ModelArn"])
    
    #Step 2: EPC Creation
    epc_name = "EPC-" + model_name 
    endpoint_config_response = client.create_endpoint_config(
        EndpointConfigName=epc_name,
        ProductionVariants=[
            {
                "VariantName": "sklearnvariant",
                "ModelName": model_name,
                "InstanceType": "ml.c5.large",
                "InitialInstanceCount": 1
            },
        ],
    )
    print("Endpoint Configuration Arn: " + endpoint_config_response["EndpointConfigArn"])
    
    #Step 3: EP Creation
    endpoint_name = "EP-" + model_name
    create_endpoint_response = client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=epc_name,
    )
    print("Endpoint Arn: " + create_endpoint_response["EndpointArn"])


    #Monitor creation
    describe_endpoint_response = client.describe_endpoint(EndpointName=endpoint_name)
    while describe_endpoint_response["EndpointStatus"] == "Creating":
        describe_endpoint_response = client.describe_endpoint(EndpointName=endpoint_name)
        print(describe_endpoint_response["EndpointStatus"])
        time.sleep(15)
    print(describe_endpoint_response)
    return endpoint_name

if __name__ == '__main__':
    main()