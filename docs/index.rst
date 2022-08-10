BatCat Introduction
===================


**BatCat** is designed to help data scientists to practice **machine learning operations (MLOps)** on **Amazon Web Services (AWS)**.

Services of AWS covered:

- **AWS Lambda**: a serverless, event-driven compute service
- **AWS S3 (Simple Storage Service)**: provides object storage service
- **Amazon Athena**: a serverless, interactive query service on S3
- **Amazon Redshift**: a data warehouse product
- **AWS Step Functions**: a low-code, visual workflow service that developers use to build distributed applications, automate IT and business processes, and build data and machine learning pipelines using AWS services.


Install
-------

BatCat can be installed from `PyPI <https://pypi.org/project/batcat/>`_ .

.. code-block:: bash

  pip install batcat



File Structure
--------------

BatCat provides one-line command to setup a well-organized file structure for data science projects.

.. autofunction:: batcat.FileSys


Storage: Data Loading and Saving 
--------------------------------

BatCat supports importing data from S3 bucket (directly by Athena or Redshift) and saving back to S3.

.. code-block:: Python
    
    bc.read_csv_from_bucket(bucket, key)
    bc.save_to_bucket(df, bucket, key)
    
    bc.read_data_from_athena(query, 
                             region,
                             s3_staging_dir,
                             date_start=None, 
                             date_end=None)

    bc.read_data_from_redshift(query, 
                               host,
                               password,
                               port=5439,
                               database='dev',
                               user='awsuser',
                               date_start=None, 
                               date_end=None)

    bc.read_data_from_redshift_by_secret(secret_name=None, 
                                         region=None, 
                                         query=None)

Compute: Docker, Step Functions, and Lambda Setup
-------------------------------------------------

BatCat provides templetes for docker, Step Functions, and Lambda setup. 


.. code-block:: Python

    bc.template_docker(project='[project]', 
                       uri_suffix='amazonaws.com.cn', 
                       pip_image=True, 
                       python_version='3.7-slim-buster')

    bc.template_stepfunctions(project='[project]',
                              purpose='[purpose]',
                              result_s3_bucket='[s3-bucket]',
                              workflow_execution_role='arn:[partition]:iam::[account-id]:role/[role-name]')

    bc.template_lambda(project='[project]', 
                       purpose='[purpose]', 
                       result_s3_bucket='[s3-bucket]',
                       partition='aws-cn')







