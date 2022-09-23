BatCat Tutorials
****************

Data Science Projects Basics
============================

Environment Setup
-----------------

The first step to start a data science project should always be setup a development file system, no matter on cloud or in your laptop. **BatCat** provides a one-line command to setup a well-organized file system for data science projects.

.. code-block:: bash

    python -m batcat.FileSys

The interactive and immersive command-line interfaces as following. Just type down your project name, like :code:`battery` in this tutorial. Then it will generate a file structure for your data science project and print out a file tree of it. 

::

    hi, there! please write down your machine learning project's name.
    project's name: battery
    project_battery/
        requirements.txt
        README.md
        .gitignore
        docs/
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

.. note::

    1. :file:`requirements.txt` includes all packages you need in your project. We recommend you to list not only package names but thier versions in the file. Besides, this serves your well if you develop your project on SageMaker, for you have to install all required packages every time restarting the Jupyter Notebook instance.
    2. :file:`.gitignore` includes :file:`data/*` by default, which is our best practice in data science projects with **git**. Generally, you don't want to git your data. 
    3. :file:`docs/READM.md` is inspired by `How to ML Paper - A brief Guide <https://docs.google.com/document/d/16R1E2ExKUCP5SlXWHr-KzbVDx9DBUclra-EbU8IB-iE/edit?usp=sharing>`_. We highly recommend you to document your data science project in an organized way so that anyone, including youself, can catch up your thoughts in the future.


Logging
-------

Most data scientists spend little time on logging and may just print out along the experiement in Jupyter Notebook. However, this can make annoying troubles when it comes to production environment or when the data science experiements require a long period to generate experiement records. Therefore, logging is critical to a data science project. 

Python Module **Logging** is one of the most underrated features. Two things (5&3) to take away from **Logging**: 

1. **5 levels** of importance that logs can contain(debug, info, warning, error, critical);  
2. **3 components** to configure a logger in Python (a logger, a formatter, and at least one handler).

**BatCat** provides a function :code:`get_logger` to make life easier.

.. code-block:: Python

    import batcat as bc
    
    log_name = 'battery'
    log_file = '../log/batter.log'

    logger = bc.get_logger(logName=log_name, logFile=log_file)
    
    logger.debug('this is a debug')
    logger.info('this is a test')
    logger.warning('this is a warning')
    
    logger.error('this is an error!')
    logger.critial('this is critical!')


IO Tools
========

**Services on AWS**: S3, Redshift, Athena. 

**BatCat** supports reading data from S3 bucket (directly or by Athena or Redshift) and saving back to S3.

S3 Bucket
---------

Read CSV data directly from S3 and save a DataFrame to S3.

.. code-block:: Python
    
    bucket = '2022-RnD-battery'
    key = 'usage'

    df = bc.read_csv_from_bucket(bucket, key)
    
    bc.save_to_bucket(df, bucket, key)

SQL: Redshift, Athena
---------------------

The above approach is fine with a given S3 object but can be tricky when it comes to scenarios you need write SQLs to query data. This can be handled with Athena and Redshift. 

1. **Athena**: Service Glue is required before you query with Athena.
2. **Redshift**: 
    - With host/password.
    - With Secret Manager.

.. note::
    
    Athena is recommended as Redshift approach may raise timeout error or be blocked by VPC if the Redshift is located in it. 

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


Deployment on Cloud
===================

**Services on AWS**: ECR, SageMaker Processing, Step Functions, and Lambda. 

Background
----------

Before we dive in the topic, let's align on the meaning of "deployment on cloud". This basicly involves **microservice** like container and **serverless**. In the AWS context, it related services:

- ECR
- SageMaker Processing
- Step Functions
- Lambda
- IAM

Amazon SageMaker lets developers and data scientists train and deploy machine learning models. With Amazon SageMaker Processing, you can run processing jobs for data processing steps in your machine learning pipeline. 

However, the most annoying part of SageMaker is that it offers many modules *to faciliate* model development and deployment but looks like a white elephant. What a data scientist need is something with shallow learning curve and the knowledge can be transfered to other cloud services, **NOT** something only works on AWS, which betrays the intend to use Docker! 

So here's BatCat. It provides templates to setup docker images, workflows of Step Functions, and triggers generated by Lambda functions -- to slim down the setup work on AWS. 

.. image:: images/process.svg
  :align: center

**BatCat** takes all steps in a machine learning product as processing jobs -- data cleaning, preprocessing, feature engineering, predicting. Note that the training step is not in production stage but development stage so not inlcuded here.

Setup
-----

1. Create related roles and attach policies to it. 
    Like any other AWS services, roles and policies setup is one of the most disappointing parts when using it. Refer to :ref:`Identity and Access Management <appendix:Identity and Access Management (IAM)>` for more information.
2. Setup templates:
    1. Docker setup Bash script and requirements text file. Add more required Python packages to :file:`requirements.txt` as needed. 
    2. Step Functions setup Python script.
    3. Lambda function setup Python script.
3. Add the data science core script.
    Add your data science Python script to the current directory, whose name should aligned with :code:`purpose`. In the example below, it is :code:`usage-analysis.py`.
4. Run the scripts to deploy.
    That's it!

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


.. note::

    1. :code:`project`: your data science project name. We suggest a format as :code:`[year]-[department]-[topic]`.
    2. :code:`purpose`: or subproject under a project. 
    3. :code:`result_s3_bucket`: the S3 bucket to store data science results. 
    4. :code:`workflow_execution_role`: the role ARN you created in step 1. 