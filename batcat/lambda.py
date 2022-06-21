#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import json

def print_event(event):
    """
    arg:
        event: s3 trigger event
    return:
        None
    """
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

if __name__ == '__main__':
    main()