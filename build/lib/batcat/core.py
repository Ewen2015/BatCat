#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import boto3
from io import StringIO, BytesIO
import pandas as pd 

s3 = boto3.client('s3')


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

def read_excel_from_bucket(bucket, key, sheet_name=0):
    """
    arg:
        bucket, key: data source in s3
        sheet_name: target sheet name of the excel
    return:
        df: raw data, pandas.DataFrame
    """
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_excel(BytesIO(response['Body'].read()), sheet_name=sheet_name)
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

