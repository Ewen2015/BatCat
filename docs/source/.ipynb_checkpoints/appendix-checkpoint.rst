Appendix
********

Identity and Access Management (IAM)
====================================

1. Add permissions to your notebook role in IAM
-----------------------------------------------

The IAM role assumed by your notebook requires permission to create and run workflows in AWS Step Functions. If this notebook is running on a SageMaker notebook instance, do the following to provide IAM permissions to the notebook:

1. Go to the `IAM console <https://console.aws.amazon.com/iam/>`_.
2. Select **Roles** and then **Create role**.
3. Under **Choose the service that will use this role** select **SageMaker**. And Choose **Next**
4. Choose Attach policies and search for :code:`AWSStepFunctionsFullAccess`, :code:`AmazonS3FullAccess`, :code:`AmazonEC2ContainerRegistryFullAccess`, :code:`AmazonSageMakerFullAccess`, :code:`AmazonAthenaFullAccess`, :code:`AmazonRedshiftFullAccess`, :code:`SecretsManagerReadWrite`.
5. Choose **Next** until you can enter a **Role name**.
6. Enter a name such as :code:`apacdlcm-dev-role-AmazonSageMakerAccessRole` and then select **Create role**.

If you are running this notebook outside of SageMaker, the SDK will use your configured AWS CLI configuration. For more information, see `Configuring the AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>`_.

Next, let's create an execution role in IAM for Step Functions. 

2. Create an Execution Role for Step Functions
----------------------------------------------

Your Step Functions workflow requires an IAM role to interact with other services in your AWS environment. 

1. Go to the `IAM console <https://console.aws.amazon.com/iam/>`_.
2. Select **Roles** and then **Create role**.
3. Under **Choose the service that will use this role** select **Step Functions**.
4. Choose **Next** until you can enter a **Role name**.
5. Enter a name such as :code:`apacdlcm-dev-role-sgmkersfnworkflow` and then select **Create role**.

Next, attach a AWS Managed IAM policy to the role you created as per below steps.

1. Go to the `IAM console <https://console.aws.amazon.com/iam/>`_.
2. Select **Roles**
3. Search for :code:`apacdlcm-dev-role-sgmkersfnworkflow` IAM Role
4. Under the **Permissions** tab, click **Attach policies** and then search for :code:`CloudWatchEventsFullAccess` IAM Policy managed by AWS.
5. Click on **Attach Policy**.


Next, create and attach another new policy to the role you created. As a best practice, the following steps will attach a policy that only provides access to the specific resources and actions needed for this solution.

1. Under the **Permissions** tab, click **Attach policies** and then **Create policy**.
2. Enter the following in the **JSON** tab:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "events:PutTargets",
                    "events:DescribeRule",
                    "events:PutRule"
                ],
                "Resource": [
                    "arn:aws-cn:events:*:*:rule/StepFunctionsGetEventsForSageMakerTrainingJobsRule",
                    "arn:aws-cn:events:*:*:rule/StepFunctionsGetEventsForSageMakerTransformJobsRule",
                    "arn:aws-cn:events:*:*:rule/StepFunctionsGetEventsForSageMakerTuningJobsRule",
                    "arn:aws-cn:events:*:*:rule/StepFunctionsGetEventsForECSTaskRule",
                    "arn:aws-cn:events:*:*:rule/StepFunctionsGetEventsForBatchJobsRule"
                ]
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": "NOTEBOOK_ROLE_ARN",
                "Condition": {
                    "StringEquals": {
                        "iam:PassedToService": "sagemaker.amazonaws.com"
                    }
                }
            },
            {
                "Sid": "VisualEditor2",
                "Effect": "Allow",
                "Action": [
                    "batch:DescribeJobs",
                    "batch:SubmitJob",
                    "batch:TerminateJob",
                    "dynamodb:DeleteItem",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "ecs:DescribeTasks",
                    "ecs:RunTask",
                    "ecs:StopTask",
                    "glue:BatchStopJobRun",
                    "glue:GetJobRun",
                    "glue:GetJobRuns",
                    "glue:StartJobRun",
                    "lambda:InvokeFunction",
                    "sagemaker:CreateEndpoint",
                    "sagemaker:CreateEndpointConfig",
                    "sagemaker:CreateHyperParameterTuningJob",
                    "sagemaker:CreateModel",
                    "sagemaker:CreateProcessingJob",
                    "sagemaker:CreateTrainingJob",
                    "sagemaker:CreateTransformJob",
                    "sagemaker:DeleteEndpoint",
                    "sagemaker:DeleteEndpointConfig",
                    "sagemaker:DescribeHyperParameterTuningJob",
                    "sagemaker:DescribeProcessingJob",
                    "sagemaker:DescribeTrainingJob",
                    "sagemaker:DescribeTransformJob",
                    "sagemaker:ListProcessingJobs",
                    "sagemaker:ListTags",
                    "sagemaker:StopHyperParameterTuningJob",
                    "sagemaker:StopProcessingJob",
                    "sagemaker:StopTrainingJob",
                    "sagemaker:StopTransformJob",
                    "sagemaker:UpdateEndpoint",
                    "sns:Publish",
                    "sqs:SendMessage"
                ],
                "Resource": "*"
            }
        ]
    }


3. Replace **NOTEBOOK_ROLE_ARN** with the ARN for your notebook that you created in the previous step in the above Policy.
4. Choose **Review policy** and give the policy a name such as :code:`AmazonSageMaker-StepFunctionsWorkflowExecutionPolicy`.
5. Choose **Create policy**.
6. Select **Roles** and search for your :code:`AmazonSageMaker-StepFunctionsWorkflowExecutionRole` role.
7. Under the **Permissions** tab, click **Attach policies**.
8. Search for your newly created :code:`AmazonSageMaker-StepFunctionsWorkflowExecutionPolicy` policy and select the check box next to it.
9. Choose **Attach policy**. You will then be redirected to the details page for the role.
10. Copy the :code:`AmazonSageMaker-StepFunctionsWorkflowExecutionRole` **Role ARN** at the top of the Summary.


3. Create an Lambda Trigger Role for Step Functions
---------------------------------------------------

Your lambda requires an IAM role to trigger Step Functions workflow. 

1. Go to the `IAM console <https://console.aws.amazon.com/iam/>`_.
2. Select **Roles** and then **Create role**.
3. Under **Choose the service that will use this role** select **Lambda**. And Choose **Next**
4. Choose Attach policies and search for :code:`AWSStepFunctionsFullAccess`, :code:`AWSLambdaFullAccess`, :code:`CloudWatchFullAccess`, :code:`AmazonS3FullAccess`, :code:`SecretsManagerReadWrite`
5. Choose **Next** until you can enter a **Role name**.
6. Enter a name such as :code:`apacdlcm-dev-role-lambdatriggersfn` and then select **Create role**.


Next, create and attach another new policy to the role you created. 

1. Under the **Permissions** tab, click **Attach policies** and then **Create policy**.
2. Enter the following in the **JSON** tab:

.. code-block:: json

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ec2:DescribeNetworkInterfaces",
            "ec2:CreateNetworkInterface",
            "ec2:DeleteNetworkInterface",
            "ec2:DescribeInstances",
            "ec2:AttachNetworkInterface"
          ],
          "Resource": "*"
        }
      ]
    }

4. Choose **Review policy** and give the policy a name such as :code:`LambdaTriggerStepFuncRole`.
5. Choose **Create policy**.
6. Select **Roles** and search for your :code:`LambdaTriggerStepFuncRole` role.
7. Under the **Permissions** tab, click **Attach policies**.
8. Search for your newly created :code:`LambdaTriggerStepFuncRole` policy and select the check box next to it.
9. Choose **Attach policy**. You will then be redirected to the details page for the role.
10. Copy the :code:`apacdlcm-dev-role-lambdatriggersfn` **Role ARN** at the top of the Summary.
