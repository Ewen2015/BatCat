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

## i/o

def read_csv_from_bucket(bucket, key) -> pd.DataFrame:
    """
    arg:
        bucket, key: data source in s3
    return:
        df: raw data, pandas.DataFrame
    """    
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(BytesIO(response['Body'].read()), error_bad_lines=False, warn_bad_lines=False)
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


## multiple 

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

def copy_bucket_files(bucket, prefix, suffix, target_bucket, target_prefix, target_suffix, key_sub):
    """
    arg:
        bucket: source bucket
        prefix: prefix of source files
        suffix: suffix of source files
        target_bucket: target bucket
        target_prefix: prefix of target files
        target_suffix: suffix of target files
        key_sub: information to substract from source keys, a tuple
    return:
        None
    """
    import boto3
    s3 = boto3.resource('s3')
    source_bucket = s3.Bucket(bucket)
    
    for obj in source_bucket.objects.filter(Prefix=prefix):
        if obj.key.endswith(suffix):
            print(obj.key)
            copy_source_object = {'Bucket': bucket, 'Key': obj.key}
            target_key = "{}{}{}".format(target_prefix, obj.key[key_sub[0]:key_sub[1]], target_suffix)
            
            s3_client = boto3.client("s3")
            s3_client.copy_object(CopySource=copy_source_object, Bucket=target_bucket, Key=target_key)
            print('copied {}'.format(target_key))     
    return None


## signal

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

if __name__ == '__main__':
    main()