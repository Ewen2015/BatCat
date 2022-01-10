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

def list_bucket_files(bucket, prefix, suffix) -> list:
    """
    arg:
        bucket: target s3 bucket
        prefix: file prefix
        suffix: file suffix
    return:
        file list
    """
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)
    
    fl = []
    for obj in my_bucket.objects.filter(Prefix=prefix):
        if obj.key.endswith(suffix):
            fl.append(obj.key)
            print(obj.key)
    return fl


def read_csv_from_bucket(bucket, key) -> pd.DataFrame:
    """
    arg:
        bucket, key: data source in s3
    return:
        df: raw data, pandas.DataFrame
    """    
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(BytesIO(response['Body'].read()))
    return df

def read_excel_from_bucket(bucket, key, sheet_name=0, header=0) -> pd.DataFrame:
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
