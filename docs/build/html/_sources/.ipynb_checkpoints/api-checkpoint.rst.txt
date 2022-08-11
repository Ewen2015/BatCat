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