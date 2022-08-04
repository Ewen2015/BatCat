#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
from io import StringIO, BytesIO
from datetime import datetime
from redshift_connector import connect

import json
import random

import numpy as np
import pandas as pd

import boto3
import botocore.session as Session
from botocore.exceptions import WaiterError
from botocore.waiter import WaiterModel
from botocore.waiter import create_waiter_with_client

def read_data_from_redshift(query, 
                            host,
                            password,
                            port=5439,
                            database='dev',
                            user='awsuser',
                            date_start=None, 
                            date_end=None) -> pd.DataFrame:
    """
    arg: 
        query: querry to obtain data from Redshift, str
        host: Redshift configuration
        password: Redshift configuration
        port: Redshift configuration
        database: Redshift configuration
        user: Redshift configuration
        date_start: date to start, strftime('%Y/%m/%d')
        date_start: date to end, strftime('%Y/%m/%d')
    return:
        df: target dataframe
    """
    
    cursor = connect(host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password).cursor()
    
    query = query.format(date_start, date_end) 
    cursor.execute(query)
    
    df = cursor.fetch_dataframe()
    return df

def save_df_to_redshift(df,
                        table_name,
                        dtype=None,
                        host=None,
                        password=None,
                        port=5439,
                        database='dev',
                        user='awsuser',
                        if_exists='replace'):
    """
    arg: 
        df: target dataframe
        table_name: target table name'
        dtype: dict or scalar, optional
            Specifying the datatype for columns. If a dictionary 
            is used, the keys should be the column names and the 
            values should be the SQLAlchemy types or strings for 
            the sqlite3 legacy mode. If a scalar is provided, it 
            will be applied to all columns.
        if_exists: {‘fail’, ‘replace’, ‘append’}, default ‘fail’
            How to behave if the table already exists.
            fail: Raise a ValueError.
            replace: Drop the table before inserting new values.
            append: Insert new values to the existing table.
        host: in the form [name].[id].[region].redshift.amazonaws.com
        password: Redshift configuration
        port: usually 5439
        database: Redshift configuration
        user: Redshift configuration
    """
    from sqlalchemy import create_engine
    
    con = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT, DATABASE))
    df.to_sql(name=table_name, con=con, schema=None, if_exists=if_exists, index=False, index_label=None, chunksize=None, dtype=dtype, method=None)
    return None





def get_secret(secret_name, region):
    secret = dict()
    secret['name'] = secret_name
    secret['region'] = region

    session = boto3.session.Session()
    
    client = session.client(
            service_name='secretsmanager',
            region_name=secret['region']
        )

    try:
        get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        secret['arn']=get_secret_value_response['ARN']

    except ClientError as e:
        print("Error retrieving secret. Error: " + e.response['Error']['Message'])

    else:
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            Secret = get_secret_value_response['SecretString']
        else:
            Secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    secret = {**secret, **json.loads(Secret)}

    return secret

def _get_waiter(waiter_name):
    ### initiating waiter
    delay=2
    max_attempts=3

    #Configure the waiter settings
    waiter_config = {
      'version': 2,
      'waiters': {
        'DataAPIExecution': {
          'operation': 'DescribeStatement',
          'delay': delay,
          'maxAttempts': max_attempts,
          'acceptors': [
            {
              "matcher": "path",
              "expected": "FINISHED",
              "argument": "Status",
              "state": "success"
            },
            {
              "matcher": "pathAny",
              "expected": ["PICKED","STARTED","SUBMITTED"],
              "argument": "Status",
              "state": "retry"
            },
            {
              "matcher": "pathAny",
              "expected": ["FAILED","ABORTED"],
              "argument": "Status",
              "state": "failure"
            }
          ],
        },
      },
    }

    # set random seeds for reproducibility
    np.random.seed(42)
    random.seed(42)
    waiter_model = WaiterModel(waiter_config)
    return waiter_config, waiter_model

def _make_datarow(output):
    res = []
    a = []
    for i in output['Records']:
        for j in i:
            try:
                a.append(j['stringValue'])
            except:
                try:
                    a.append(j['doubleValue'])
                except:
                    try:
                        a.append(j['longValue'])
                    except:
                        a.append(np.nan)
        res.append(a)
        a = []
    return res


def read_data_from_redshift_by_secret(secret_name=None, region=None, query=None):

    secret = get_secret(secret_name, region)

    ## Data API client
    bc_session = Session.get_session()

    session = boto3.Session(
            botocore_session=bc_session,
            region_name=secret['region'],
        )

    ## Setup the client
    client_redshift = session.client("redshift-data")

    ## Setup waiter
    waiter_name = 'DataAPIExecution'
    waiter_config, waiter_model = _get_waiter(waiter_name)

    custom_waiter = create_waiter_with_client(waiter_name, waiter_model, client_redshift)

    ## Read data
    res = client_redshift.execute_statement(Database = secret['db'], 
                                            SecretArn = secret['arn'], 
                                            Sql = query, 
                                            ClusterIdentifier = secret['dbClusterIdentifier'])

    ## Reset the 'delay' attribute of the waiter back to 2 seconds.
    waiter_config["waiters"]["DataAPIExecution"]["delay"] = 2
    waiter_model = WaiterModel(waiter_config)
    custom_waiter = create_waiter_with_client(waiter_name, waiter_model, client_redshift)

    ## Waiter in try block and wait for DATA API to return
    try:
        custom_waiter.wait(Id=res['Id'])
        print("Done waiting to finish Data API.")
    except WaiterError as e:
        print(e)

    output = client_redshift.get_statement_result(Id=res['Id'])
    ncols = len(output["ColumnMetadata"])

    resrows = _make_datarow(output)

    col_labels=[]
    for i in range(ncols): 
        col_labels.append(output["ColumnMetadata"][i]['label'])

    df = pd.DataFrame(np.array(resrows), columns=col_labels)

    return df 


if __name__ == '__main__':
    main()
