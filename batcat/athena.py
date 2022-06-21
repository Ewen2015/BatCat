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
    arg:
        delta: the number of days ago, int
    return:
        date: strftime('%Y/%m/%d')
    """
    from datetime import date, timedelta
    return (date.today() - timedelta(days=delta)).strftime(format)


def read_data_from_athena(query, 
                         region,
                         s3_staging_dir,
                         date_start=None, 
                         date_end=None) -> pd.DataFrame:
    """
    arg: 
        query: querry to obtain data from Athena, str
        region: region of the AWS environment, eg. "cn-northwest-1"
        s3_staging_dir: s3 staging directory, eg. "s3://#####-###-###-queryresult/ATHENA_QUERY"
        date_start: date to start, strftime('%Y/%m/%d')
        date_start: date to end, strftime('%Y/%m/%d')
    """

    cursor = connect(s3_staging_dir=s3_staging_dir,
                     region_name=region,
                     cursor_class=PandasCursor).cursor()
    
    query = query.format(date_start, date_end) 
    df = cursor.execute(query).as_pandas()
    return df

if __name__ == '__main__':
    main()