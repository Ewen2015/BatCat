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

.. autofunction:: batcat.FileSys


Storage: Data Loading and Saving 
--------------------------------

BatCat supports importing data from S3 bucket (directly by Athena or Redshift) and saving back to S3.


.. autofunction:: batcat.read_csv_from_bucket

.. autofunction:: batcat.save_to_bucket

.. autofunction:: batcat.read_data_from_athena

.. autofunction:: batcat.read_data_from_redshift

.. autofunction:: batcat.read_data_from_redshift_by_secret


Compute: Docker, Step Functions, and Lambda Setup
-------------------------------------------------

BatCat provides templetes for docker, Step Functions, and Lambda setup. 

.. autofunction:: batcat.template_docker

.. autofunction:: batcat.template_stepfunctions

.. autofunction:: batcat.template_lambda

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
