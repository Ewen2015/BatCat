#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import json

def print_event(event):
    """Print Lambda event name.

    Args:
        event (str): S3 trigger event.

    Returns:
        None
    """
    print("Received event: " + json.dumps(event, indent=2))
    return None

def get_bucket_key(event):
    """Get S3 the bucket and key from event.

    Args:
        event (str): S3 trigger event.

    Returns:
        bucket, key: Bucket and key of the event.
    """
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    return bucket, key 

if __name__ == '__main__':
    main()