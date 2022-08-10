#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import os
import time
import boto3
from stepfunctions import steps
from stepfunctions.workflow import Workflow
from stepfunctions.inputs import ExecutionInput
import sagemaker
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.processing import ScriptProcessor
from smexperiments.experiment import Experiment


def processing_output_path(purpose, timestamp=True, local=False):
    """ setup a result path within container.
    arg:
        purpose: a purpose under a project
        timestamp: whether a timestamp in file name is needed
        local: if set the path to local for test
    return:
        path: a csv path for later usage
    """
    if timestamp:
        job = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        job = '_{}'.format(job)
    else:
        job = ''
    path = '/opt/ml/processing/{}/{}{}.csv'.format(purpose, purpose, job)
    if local:
        path = '{}{}.csv'.format(purpose, job)
    return path



def setup_workflow(project='[project]',
                   purpose='[purpose]',
                   workflow_execution_role='arn:aws-cn:iam::[account-id]:role/[role-name]'):
    """ to setup all needed for a step function with sagemaker.
    arg: 
        project: project name under sagemaker
        purpose: subproject
        workflow_execution_role: arn to execute step functions
        script_dir: processing file name, like a .py file
        ecr_repository: ecr repository name
    return:
        workflow: a stepfunctions.workflow.Workflow instance  
    example: 
        PROJECT = '[dpt-proj-2022]'
        PURPOSE = '[processing]'
        WORKFLOW_EXECUTION_ROLE = "arn:aws-cn:iam::[account-id]:role/[role-name]"
        SCRIPT_DIR = "[processing].py"
        ECR_REPOSITORY = '[ecr-2022]'
    """

    # SageMaker Session setup
    # ========================================================================================
    # SageMaker Session
    # ====================================
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    role = sagemaker.get_execution_role()
    
    # Storage
    # ====================================
    session = sagemaker.Session()
    region = session.boto_region_name
    s3_output = session.default_bucket()

    # Code storage
    # ==================
    s3_prefix = '{}/{}'.format(project, purpose)
    s3_prefix_code = '{}/code'.format(s3_prefix)
    s3CodePath = 's3://{}/{}/code'.format(s3_output, s3_prefix)   

    ## preprocess & prediction
    script_dir = '{}.py'.format(purpose)
    script_list = [script_dir]

    for script in script_list:
        session.upload_data(script,
                            bucket=session.default_bucket(),
                            key_prefix=s3_prefix_code)

    # ECR environment
    # ====================================
    ecr_repository = project
    uri_suffix = 'amazonaws.com.cn'
    tag = ':latest'
    ecr_repository_uri = '{}.dkr.ecr.{}.{}/{}'.format(account_id, region, uri_suffix, ecr_repository + tag)

    # SageMaker Experiments setup
    # ========================================================================================
    experiment = Experiment.create(experiment_name="{}-{}".format(project, int(time.time())), 
                                   description="machine learning project", 
                                   sagemaker_boto_client=boto3.client('sagemaker'))
    print(experiment)

    execution_input = ExecutionInput(
        schema={
            "ProcessingJobName": str,
            "ResultPath": str,
        }
    )

    # setup script processor
    script_processor = ScriptProcessor(command=['python3'],
                                       image_uri=ecr_repository_uri,
                                       role=role,
                                       instance_count=1,
                                       instance_type='ml.m5.4xlarge')

    # Step
    # ========================================================================================
    
    optimizing_step = steps.ProcessingStep(
        "Processing Step",
        processor=script_processor,
        job_name=execution_input["ProcessingJobName"],
        inputs=[ProcessingInput(
                            source=s3CodePath,
                            destination='/opt/ml/processing/input/code',
                            input_name='code')],
        outputs=[ProcessingOutput(output_name=purpose,
                        destination = execution_input["ResultPath"],
                        source='/opt/ml/processing/{}'.format(purpose))],
        container_entrypoint=["python3", "/opt/ml/processing/input/code/"+script_dir],
    )


    # Fail Sate
    # ========================================================================================
    failed_state = steps.states.Fail(
        "Processing Workflow failed", 
        cause="SageMakerProcessingJobFailed"
    )

    catch_state_processing = steps.states.Catch(
        error_equals=["States.TaskFailed"],
        next_step=failed_state
    )

    # Create Workflow
    # ========================================================================================
    optimizing_step.add_catch(catch_state_processing)

    workflow_name = "workflow-{}-{}".format(project, purpose).upper()
    workflow_graph = steps.Chain([optimizing_step])

    workflow = Workflow(
        name=workflow_name,
        definition=workflow_graph,
        role=workflow_execution_role
    )

    workflow.create()
    return workflow


def test_workflow(workflow, project='[project]', purpose='[purpose]', result_s3_bucket='[s3-bucket]'):
    """ to test a step function workflow.
    arg:
        workflow: a stepfunctions.workflow.Workflow instance
        project: project name under sagemaker
        purpose: subproject
        result_s3_bucket: S3 bucket for saving results
    return:
        None
    """
    job = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    job_name = "{}-{}-{}".format(project, purpose, job)
    result_path="s3://{}/{}".format(result_s3_bucket, purpose)
    
    # Execute workflow
    execution = workflow.execute(
        inputs={
            "ProcessingJobName": job_name,
            "ResultPath": result_path, 
        }
    )
    execution_output = execution.get_output(wait=True)
    return None



def template_stepfunctions(project='[project]',
                           purpose='[purpose]',
                           result_s3_bucket='[s3-bucket]',
                           workflow_execution_role='arn:[partition]:iam::[account-id]:role/[role-name]'):
    """ A template for setting up Step Functions.
    arg:
        project: project name under sagemaker
        purpose: subproject
        result_s3_bucket: S3 bucket for saving results
        workflow_execution_role: execution role arn
    return:
        None
    """

    template = \
"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from batcat.Stepfunctions import setup_workflow
from batcat.Stepfunctions import test_workflow

if __name__ == '__main__':

    WORKFLOW_EXECUTION_ROLE = '{}'

    PROJECT = '{}'
    PURPOSE = '{}'

    RESULT_S3_BUCKET = '{}'
    
    workflow = setup_workflow(project=PROJECT, 
                              purpose=PURPOSE, 
                              workflow_execution_role=WORKFLOW_EXECUTION_ROLE)

    test_workflow(workflow, project=PROJECT, purpose=PURPOSE, result_s3_bucket=RESULT_S3_BUCKET)

    # workflow.delete()
""".format(workflow_execution_role, project, purpose, result_s3_bucket)
    
    with open('setup_stepfuncions_{}.py'.format(purpose), 'w') as writer:
        writer.write(template)

    return None


def template_lambda(project='[project]', 
                    purpose='[purpose]', 
                    result_s3_bucket='[s3-bucket]',
                    partition='aws-cn'):
    """ A template for setting up Lambda.
    arg:
        project: project name under sagemaker
        purpose: subproject
        result_s3_bucket: S3 bucket for saving results
        partition: The partition in which the resource is located. A partition is a group of Amazon Regions. Default as 'aws-cn'.
    return:
        None
    """
    file_name = '{}-{}-trigger/lambda_function.py'.format(project, purpose)
    
    region = boto3.session.Session().region_name
    account = boto3.client('sts').get_caller_identity().get('Account')

    stateMachineName = "workflow-{}-{}".format(project, purpose).upper()
    workflowarn = 'arn:{}:states:{}:{}:stateMachine:{}'.format(partition, region, account, stateMachineName)

    result_path="s3://{}/{}".format(result_s3_bucket, purpose)

    template1 = \
"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
import uuid
import time

WORKFLOWARN = '{}'
PROJECT = '{}'
PURPOSE = '{}'
RESULT_PATH = '{}'

client = boto3.client('stepfunctions')
""".format(workflowarn, project, purpose, result_path)
    template2 = \
"""
def lambda_handler(event, context):  
    transactionId = str(uuid.uuid1())

    job = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    job_name = "{}-{}-{}".format(PROJECT, PURPOSE, job)

    inputs={
        "ProcessingJobName": job_name,
        "ResultPath": RESULT_PATH, 
    }
    
    response = client.start_execution(
            stateMachineArn = WORKFLOWARN,
            name = transactionId,
            input = json.dumps(inputs)
        )

    return {
       'statusCode': 200,
       'body': json.dumps('succeeded!')
   }
"""
    template = template1 + template2
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as writer:
        writer.write(template)

    return None

if __name__ == '__main__':
    main()