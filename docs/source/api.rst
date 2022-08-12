BatCat API
==========

Data Science Environment Setup
------------------------------

.. autofunction:: batcat.FileSys

.. autofunction:: batcat.get_logger


Simple Storage Service (S3) 
---------------------------

.. autofunction:: batcat.read_csv_from_bucket

.. autofunction:: batcat.read_excel_from_bucket

.. autofunction:: batcat.save_to_bucket

.. autofunction:: batcat.list_bucket_files

.. autofunction:: batcat.copy_bucket_files

.. autofunction:: batcat.SuccessSignal


Redshift 
--------

.. autofunction:: batcat.get_date_with_delta

.. autofunction:: batcat.read_data_from_redshift

.. autofunction:: batcat.save_df_to_redshift

.. autofunction:: batcat.read_data_from_redshift_by_secret

.. autofunction:: batcat.get_secret


Athena 
------

.. autofunction:: batcat.read_data_from_athena


Lambda
------

.. autofunction:: batcat.print_event

.. autofunction:: batcat.get_bucket_key


Step Functions
--------------

.. autofunction:: batcat.processing_output_path

.. autofunction:: batcat.setup_workflow

.. autofunction:: batcat.test_workflow

.. autofunction:: batcat.template_docker

.. autofunction:: batcat.template_stepfunctions

.. autofunction:: batcat.template_lambda





















