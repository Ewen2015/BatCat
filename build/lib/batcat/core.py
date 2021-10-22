#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
from io import StringIO, BytesIO
from datetime import datetime
import pandas as pd
import boto3

s3 = boto3.client('s3')


def print_event(event):
    """
    arg:
        event: s3 trigger event
    return:
        None
    """
    import json
    print("Received event: " + json.dumps(event, indent=2))
    return None

def get_bucket_key(event):
    """
    arg:
        event: s3 trigger event
    return:
        bucket, key: bucket and key of the event
    """
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    return bucket, key 


def SuccessSignal(bucket, key='.success'):
    """
    arg:
        bucket: target bucket to receive a signal
        key: signal file
    return:
        statue: HTTPS status code
    """
    with StringIO() as buffer:
        buffer.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S %f'))
        response = s3.put_object(Bucket=bucket, 
                                 Key=key, 
                                 Body=buffer.getvalue())
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    return status


def read_csv_from_bucket(bucket, key):
    """
    arg:
        bucket, key: data source in s3
    return:
        df: raw data, pandas.DataFrame
    """    
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(BytesIO(response['Body'].read()))
    return df

def read_excel_from_bucket(bucket, key, sheet_name=0, header=0):
    """
    arg:
        bucket, key: data source in s3
        sheet_name: target sheet name of the excel
    return:
        df: raw data, pandas.DataFrame
    """
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_excel(BytesIO(response['Body'].read()), 
                       sheet_name=sheet_name, 
                       header=header)
    return df 

def save_to_bucket(df, bucket, key):
    """
    arg:
        bucket, key: target data destination in s3
        df: a pandas.DataFrame
    return:
        statues: HTTPS status code
    """
    with StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)
        response = s3.put_object(Bucket=bucket, 
                                 Key=key, 
                                 Body=csv_buffer.getvalue())
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    return status
    
def get_data_from_athena(query, 
                         date_start, 
                         date_end,
                         region,
                         s3_staging_dir):
    """
    arg: 
        query: querry to obtain data from Athena, str
        date_start: date to start, strftime('%Y/%m/%d')
        date_start: date to end, strftime('%Y/%m/%d')
        region: region of the AWS environment, eg. "cn-northwest-1"
        s3_staging_dir: s3 staging directory, eg. "s3://#####-###-###-queryresult/ATHENA_QUERY"
    """
    from pyathena import connect
    from pyathena.pandas.cursor import PandasCursor
    
    cursor = connect(s3_staging_dir=s3_staging_dir,
                     region_name=region,
                     cursor_class=PandasCursor).cursor()
    
    query = query.format(date_start, date_end) 
    df = cursor.execute(query).as_pandas()
    return df

def get_date_with_delta(delta):
    """ Get the date delta days ago.
    arg:
        delta: the number of days ago, int
    return:
        date: strftime('%Y/%m/%d')
    """
    from datetime import date, timedelta
    return (date.today() - timedelta(days=delta)).strftime('%Y/%m/%d')

def get_data_from_redshit(query, 
                          date_start, 
                          date_end,
                          host,
                          password,
                          port=5439,
                          database='dev',
                          user='awsuser'):
    """
    arg: 
        query: querry to obtain data from Redshift, str
        date_start: date to start, strftime('%Y/%m/%d')
        date_start: date to end, strftime('%Y/%m/%d')
        host: Redshift configuration
        password: Redshift configuration
        port: Redshift configuration
        database: Redshift configuration
        user: Redshift configuration
    return:
        df: target dataframe
    """
    from redshift_connector import connect
    
    cursor = connect(host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password).cursor()
    
    query = query.format(date_start, date_end) 
    cursor.execute(query)
    
    df = cursor.fetch_dataframe()
    return df

