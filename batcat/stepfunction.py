#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import time
import boto3
from stepfunctions import steps
from stepfunctions.workflow import Workflow
from stepfunctions.inputs import ExecutionInput
import sagemaker
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.processing import ScriptProcessor
from smexperiments.experiment import Experiment


def StepFunction(project,
                 purpose,
                 workflow_execution_role, 
                 script_dir,
                 ecr_repository,
                 workflow_name):
    """ 
    arg: 
        project: project name under sagemaker
        purpose: subproject
        workflow_execution_role: arn to execute step functions
        script_dir: processing file name, like a .py file
        ecr_repository: ecr repository name
        workflow_name: workflow name to register in step functions
    return:
        workflow: a stepfunctions.workflow.Workflow instance  
    example: 
        PROJECT = '[dpt-proj-2022]'
        PURPOSE = '[processing]'
        WORKFLOW_EXECUTION_ROLE = "arn:aws-cn:iam::[*********]:role/[**************]"
        SCRIPT_DIR = "[processing].py"
        ECR_REPOSITORY = '[ecr-2022]'
        WORKFLOW_NAME='[DEPTMT-PROJECT-SUBPROJECT-WORKFLOW]'
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
    script_list = [script_dir]

    for script in script_list:
        session.upload_data(script,
                            bucket=session.default_bucket(),
                            key_prefix=s3_prefix_code)

    # ECR environment
    # ====================================
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
                                       instance_type='ml.c5.xlarge')

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

    workflow_graph = steps.Chain([optimizing_step])

    workflow = Workflow(
        name=workflow_name,
        definition=workflow_graph,
        role=workflow_execution_role
    )

    workflow.create()
    return workflow


# test
# ========================================================================================

def test_workflow(workflow, result_path, project, purpose):
    """
    arg:
        workflow: a stepfunctions.workflow.Workflow instance
        result_path: s3 result path
    return:
        None
    example:
        RESULT_PATH = "s3://[****]/[****]"
    """
    import time

    job = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    job_name = "{}-{}-{}".format(project, purpose, job)
    
    # Execute workflow
    execution = workflow.execute(
        inputs={
            "ProcessingJobName": job_name,
            "ResultPath": result_path, 
        }
    )
    execution_output = execution.get_output(wait=True)

    return None