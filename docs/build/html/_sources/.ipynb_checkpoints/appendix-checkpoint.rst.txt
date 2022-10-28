Appendix
********


Machine Learning Operations (MLOps)
===================================

The paper `Hidden Technical Debt in Machine Learning Systems <https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf>`_ gave birth to the field **MLOps** which aims to address concerns of technical debt in machine learning systems.

Machine learning offers a fantastically powerful toolkit for building useful complex prediction systems quickly. This paper argues **it is dangerous to think of these quick wins as coming for free**. Using the software engineering framework of **technical debt**, we find it is common to incur massive ongoing maintenance costs in real-world ML systems. We explore several ML-specific risk factors to account for in system design. These include **boundary erosion, entanglement, hidden feedback loops, undeclared consumers, data dependencies, configuration issues, changes in the external world, and a variety of system-level anti-patterns**. (`Hidden Technical Debt in Machine Learning Systems <https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf>`_)

    
    You can’t be an AI expert these days and not have some grounding in software engineering. 
    
    – Grady Booch


.. image:: images/mlops.png
  :align: center

Only a small fraction of real-world ML systems is composed of the ML code, as shown by the small black box in the middle. The required surrounding infrastructure is vast and complex.



Identity and Access Management (IAM)
====================================


- An IAM **role** is an identity you can create that has specific permissions with credentials that are valid for short durations.
- A **policy** is an object in Amazon Web Services that defines permissions.

Our best practice is to create a **role** for data science, which attached **policies** listed in **step 4** below. 

1. Go to the `IAM console <https://console.aws.amazon.com/iam/>`_.
2. Select **Roles** and then **Create role**.
3. Under **Choose the service that will use this role** select **SageMaker**. And Choose **Next**
4. Choose Attach **policies** and search for 

- :code:`AmazonS3FullAccess`
- :code:`AWSGlueServiceRole`
- :code:`AmazonAthenaFullAccess`
- :code:`AmazonRedshiftFullAccess`
- :code:`AmazonSageMakerFullAccess`
- :code:`AmazonEC2ContainerRegistryFullAccess`
- :code:`AWSStepFunctionsFullAccess`
- :code:`AWSLambda_FullAccess`
- :code:`CloudWatchEventsFullAccess`
- :code:`CloudWatchFullAccess`
- :code:`SecretsManagerReadWrite`

5. Choose **Next** until you can enter a **Role name**.
6. Enter a name such as :code:`datalake-comsumer-datascience` and then select **Create role**.

If you are running this notebook outside of SageMaker, the SDK will use your configured AWS CLI configuration. For more information, see `Configuring the AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>`_.