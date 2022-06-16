####################
BatCat Documentation
####################


**BatCat** is designed to help data scientists to practice **machine learning operations (MLOps)** on **Amazon Web Services (AWS)**.

Services of AWS covered:

- **AWS Lambda**: a serverless, event-driven compute service
- **AWS S3 (Simple Storage Service)**: provides object storage service
- **Amazon Athena**: a serverless, interactive query service on S3
- **Amazon Redshift**: a data warehouse product
- **AWS Step Functions**: a low-code, visual workflow service that developers use to build distributed applications, automate IT and business processes, and build data and machine learning pipelines using AWS services.


Install
=======

BatCat can be installed from `PyPI <https://pypi.org/project/batcat/>`_ .

.. code-block:: bash

  pip install batcat



File Structure
==============

BatCat provides one-line command to setup a well-organized file structure for data science projects.

.. code-block:: Python

    import batcat as bc

    bc.FileSys()


Import Data
===========

BatCat supports importing data from S3, Redshift, and Athena.

.. code-block:: Python
    
    bc.read_csv_from_bucket(bucket, key)
    
    bc.read_data_from_athena(query, 
                             region,
                             s3_staging_dir)

    bc.read_data_from_redshift(query, 
                               host,
                               password,
                               port,
                               database,
                               user)

