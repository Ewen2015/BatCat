#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""

def docker(ecr_repository, uri_suffix='amazonaws.com.cn', pip_image=True, python_version='3.7-slim-buster'):
    if pip_image:
        pip_image = "-i https://pypi.douban.com/simple/"
    templete_docker=\
"""#!/bin/bash

account_id=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)
uri_suffix="{}"

# INSTALL PYTHON PACKAGES
# ========================================================================================================
python3 -m pip install -r requirements.txt {}

# DOCKER
# ========================================================================================================
# WRITE DOCKER FILE
mkdir -p docker
cp requirements_docker.txt docker/requirements.txt
cd docker
rm Dockerfile
cat <<EOF >> Dockerfile
FROM python:{}
RUN apt -y update && apt install -y --no-install-recommends \
    libgomp1 build-essential \
    && apt clean    
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip3 install -r requirements.txt {}
COPY . /opt/app 
ENV PYTHONUNBUFFERED=TRUE
EOF
cd ..

# CREATE ECR REPOSITORY AND PUSH DOCKER IMAGE
# ========================================================================================================
ecr_repository="{}"
tag=":latest"
repository_uri="$account_id.dkr.ecr.$region.$uri_suffix/$ecr_repository$tag"

docker build -t $ecr_repository docker
$(aws ecr get-login --region $region --registry-ids $account_id --no-include-email)
aws ecr create-repository --repository-name $ecr_repository
docker tag $ecr_repository$tag $repository_uri
docker push $repository_uri
""".format(uri_suffix, pip_image, python_version, pip_image, ecr_repository)
    with open('setup_docker.sh', 'w') as writer:
        writer.write(templete_docker)

    templete_req_docker=\
"""numpy==1.21.1 
pandas==1.3.4
matplotlib==3.3.2
scikit-learn==0.24.2
ipython==7.26.0 
ipywidgets==7.6.3  
traitlets==5.0.5
numba==0.52.0
sagemaker-training==3.9.2 
boto3==1.18.57
pyathena==2.3.0
redshift_connector==2.0.888
sqlalchemy==1.3.23
psycopg2==2.7.7
psycopg2-binary==2.9.1
catboost==1.0.5
shap==0.40.0
mlxtend==0.19.0
gossipcat==0.3.2
batcat==0.1.6
"""
    with open('requirements_docker.txt', 'w') as writer:
        writer.write(templete_req_docker)
    
    templete_req=\
"""awscli==1.20.57
boto3==1.18.57
requests==2.26.0
sagemaker==2.59.8
stepfunctions==2.2.0
sagemaker-experiments==0.1.35
sagemaker-training==3.9.2 
boto3==1.18.57
pyathena==2.3.0
redshift_connector==2.0.888
sqlalchemy==1.3.23
psycopg2==2.7.7
psycopg2-binary==2.9.1
batcat==0.1.6
"""
    with open('requirements.txt', 'w') as writer:
        writer.write(templete_req)
    return None