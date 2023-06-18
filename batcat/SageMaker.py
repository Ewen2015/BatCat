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
import subprocess


def save_model(model, model_name='model', model_suffix='.joblib'):
    """Saves a machine learning model using Joblib.

    Args:
        model (object): The trained machine learning model.
        model_name (str, optional): The name to save the model under. Defaults to 'model'.
        model_suffix (str, optional): The file extension to save the model with. Defaults to '.joblib'.

    Returns:
        None
    """
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
    res = prediction.tolist()
    respJSON = {'Output': res}
    return respJSON
"""
    
    with open('inference.py', 'w') as writer:
        writer.write(template)

    return None

def upload_model_to_s3(model_name='model', model_suffix='.joblib', bucket='[bucket]'):
    """Uploads a machine learning model to an S3 bucket.

    Args:
        model_name (str, optional): The name to save the model under. Defaults to 'model'.
        model_suffix (str, optional): The file extension to save the model with. Defaults to '.joblib'.
        bucket (str): The S3 bucket to upload the model to.

    Returns: 
        model_artifacts (str): The S3 path where the model is uploaded.
    """
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
                 bucket='[bucket]'):
    """ Deploy an scikit-learn model to SageMaker Endpoint.
    
    Args:
        model: An scikit-learn model.
        model_name (str): The model name.
        bucket (str): The bucket to store model, which is also the project name in BatCat convention.

    Return:
        reponse (dict): The model, endpoint configuration, endpoint information. 
    """
    response = dict()
    response["ModelName"] = model_name
    print("Model Name: " + response["ModelName"])

    ## Model Setup    
    save_model(model=model)
    template_inference()
    model_artifacts = upload_model_to_s3(bucket=bucket)
    response["ModelArtifacts"] = model_artifacts
    print("Model Artifacts: " + response["ModelArtifacts"])
    
    ## SKLearn Image Setup
    client = boto3.client(service_name="sagemaker")
    runtime = boto3.client(service_name="sagemaker-runtime")
    boto_session = boto3.session.Session()
    region = boto_session.region_name
    sagemaker_session = sagemaker.Session()
    role = sagemaker.get_execution_role()
    
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
    response["ModelVersion"] = model_name
    print("Model Name (Version): " + response["ModelVersion"])

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
    response["ModelArn"] = create_model_response["ModelArn"]
    print("Model Arn: " + response["ModelArn"])
    
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
    response["EndpointConfigName"] = epc_name
    response["EndpointConfigArn"] = endpoint_config_response["EndpointConfigArn"]
    print("Endpoint Configuration Name: " + response["EndpointConfigName"])
    print("Endpoint Configuration Arn: " + response["EndpointConfigArn"])
    
    #Step 3: EP Creation
    endpoint_name = "EP-" + model_name
    create_endpoint_response = client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=epc_name,
    )
    response["EndpointName"] = endpoint_name
    response["EndpointArn"] = create_endpoint_response["EndpointArn"]
    print("Endpoint Name: " + response["EndpointName"])
    print("Endpoint Arn: " + response["EndpointArn"])

    #Monitor creation
    describe_endpoint_response = client.describe_endpoint(EndpointName=endpoint_name)
    while describe_endpoint_response["EndpointStatus"] == "Creating":
        describe_endpoint_response = client.describe_endpoint(EndpointName=endpoint_name)
        print(describe_endpoint_response["EndpointStatus"])
        time.sleep(15)
    print(describe_endpoint_response)

    return response


def invoke(endpoint_name, input_data):
    """Invokes a SageMaker endpoint with input data.

    Args:
        endpoint_name (str): The name of the SageMaker endpoint.
        input_data (list): The input data to send to the endpoint.

    Returns:
        result (list): The response from the SageMaker endpoint. 
    """
    runtime_client = boto3.client('sagemaker-runtime')
    content_type = "application/json"
    
    request_body = {"Input": input_data}
    data = json.loads(json.dumps(request_body))
    payload = json.dumps(data)

    response = runtime_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType=content_type,
        Body=payload)
    result = json.loads(response['Body'].read().decode())['Output']
    return result

if __name__ == '__main__':
    main()