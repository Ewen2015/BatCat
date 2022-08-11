.. BatCat documentation master file, created by
   sphinx-quickstart on Wed Aug 10 14:12:47 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BatCat's documentation!
==================================
**BatCat** is designed to help data scientists to practice **machine learning operations (MLOps)** on **Amazon Web Services (AWS)**.

Services of AWS covered:

- **AWS Lambda**: a serverless, event-driven compute service
- **AWS S3 (Simple Storage Service)**: provides object storage service
- **Amazon Athena**: a serverless, interactive query service on S3
- **Amazon Redshift**: a data warehouse product
- **AWS Step Functions**: a low-code, visual workflow service that developers use to build distributed applications, automate IT and business processes, and build data and machine learning pipelines using AWS services.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Installation Guide
==================

BatCat can be installed from `PyPI <https://pypi.org/project/batcat/>`_ .

.. code-block:: bash
  
  pip install batcat


BatCat Tutorials
================

File Structure
--------------

BatCat provides one-line command to setup a well-organized file structure for data science projects.

.. code-block:: bash

    python -m batcat.FileSys

The interactive and immersive command-line interfaces as following. Just type down your project name, like :code:`battery` in this tutorial. Then it will generate a file structure for your data science project and print out a file tree of it. 

::

    hi, there! please write down your machine learning project's name.
    project's name: battery
    project_battery/
        README.md
        .gitignore
        doc/
            READM.md
        log/
        model/
        test/
        data/
            tmp/
            train/
            test/
            result/
            raw/
        notebook/
        report/
        script/
            config.json
        deploy/
            deploy.sh


Storage: Data Loading and Saving 
--------------------------------

BatCat supports importing data from S3 bucket (directly by Athena or Redshift) and saving back to S3.

Read data directly from S3 and save the df to S3.

.. code-block:: Python

    import batcat as bc
    
    bucket = '2022-RnD-battery'
    key = 'usage'

    df = bc.read_csv_from_bucket(bucket, key)
    
    bc.save_to_bucket(df, bucket, key)


.. code-block:: Python

    query = """
    SELECT 
        vin,
        usage,
        time
    FROM 
        cdc.dw_bms.battery_usage
    WHERE
        time >= '{}' and time <= '{}'
    """
    date_start = '2022-01-01'
    date_end = '2022-08-01'

    # from Athena
    region = 'cn-northwest-1'
    s3_staging_dir = "s3://apac-athena-queryresult/ATHENA_QUERY"
    
    bc.read_data_from_athena(query=query, 
                             region=region,
                             s3_staging_dir=s3_staging_dir,
                             date_start=date_start, 
                             date_end=date_end)
    
    # from RedShift
    # with host/password
    host = '0.1.1.1'
    password = 'this_is_a_password'
    
    bc.read_data_from_redshift(query=query, 
                               host=host,
                               password=password,
                               port=5439,
                               database='dev',
                               user='awsuser',
                               date_start=date_start, 
                               date_end=date_end)
    
    # with secret manager
    secret_name = 'secret/manager'
    
    bc.read_data_from_redshift_by_secret(secret_name=secret_name, 
                                         region=region, 
                                         query=query)


Compute: Docker, Step Functions, and Lambda Setup
-------------------------------------------------

BatCat provides templetes for docker, Step Functions, and Lambda setup. 

.. code-block:: Python

    project = '2022-RnD-battery'
    purpose = 'usage-analysis'

    result_s3_bucket = '2022-RnD-battery'

    workflow_execution_role = 'arn:aws-cn:iam::[account-id]:role/[role-name]'

    # setup Docker environment
    bc.template_docker(project=project, 
                       uri_suffix='amazonaws.com.cn', 
                       pip_image=True, 
                       python_version='3.7-slim-buster')
    
    # setup Step Functions workflow
    bc.template_stepfunctions(project=project,
                              purpose=purpose,
                              result_s3_bucket=s3-bucket,
                              workflow_execution_role=workflow_execution_role)
    
    # setup lambda to trigger workflow
    bc.template_lambda(project=project, 
                       purpose=purpose, 
                       result_s3_bucket=s3-bucket,
                       partition='aws-cn')


BatCat API
==========

File Structure
--------------

.. autofunction:: batcat.FileSys


Storage: Data Loading and Saving 
--------------------------------

.. autofunction:: batcat.read_csv_from_bucket

.. autofunction:: batcat.save_to_bucket

.. autofunction:: batcat.read_data_from_athena

.. autofunction:: batcat.read_data_from_redshift

.. autofunction:: batcat.read_data_from_redshift_by_secret


Compute: Docker, Step Functions, and Lambda Setup
-------------------------------------------------

.. autofunction:: batcat.template_docker

.. autofunction:: batcat.template_stepfunctions

.. autofunction:: batcat.template_lambda


Indices and tables
==================

* :ref:`genindex`