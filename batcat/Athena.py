#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import pandas as pd

from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

def get_date_with_delta(delta, format='%Y/%m/%d'):
    """ Get the date delta days ago.

    Args:
        delta (int): The number of days ago.

    Returns:
        date (str): Strftime('%Y/%m/%d').
    """
    from datetime import date, timedelta
    return (date.today() - timedelta(days=delta)).strftime(format)


def read_data_from_athena(query, 
                         region,
                         s3_staging_dir,
                         date_start=None, 
                         date_end=None):
    """Read data as DataFrame from AWS Athena.

    Args:
        query (str): Querry to obtain data from Athena.
        region (str): Region of the AWS environment, eg. "cn-northwest-1".
        s3_staging_dir (str): S3 staging directory, eg. "s3://#####-###-###-queryresult/ATHENA_QUERY".
        date_start (str): Date to start, strftime('%Y/%m/%d').
        date_end (str): Date to end, strftime('%Y/%m/%d').
    
    Returns:    
        df (pandas.DataFrame): dataframe.
    """

    cursor = connect(s3_staging_dir=s3_staging_dir,
                     region_name=region,
                     cursor_class=PandasCursor).cursor()
    
    query = query.format(date_start, date_end) 
    df = cursor.execute(query).as_pandas()
    return df

if __name__ == '__main__':
    main()