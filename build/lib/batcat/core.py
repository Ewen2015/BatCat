#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import pandas as pd

def get_date_with_delta(delta, format='%Y/%m/%d'):
    """ Get the date delta days ago.
    arg:
        delta: the number of days ago, int
    return:
        date: strftime('%Y/%m/%d')
    """
    from datetime import date, timedelta
    return (date.today() - timedelta(days=delta)).strftime(format)

def read_data_from_bd(query, 
                      host,
                      user, 
                      port,
                      database,
                      password) -> pd.DataFrame:
    """ get data from abc database
    arg:
        query: sql 
        username: database username
        password: database password
    return:
        df: dataframe
    """
    import pymysql
    
    connection = pymysql.connect(host=host,
                                 user=user,
                                 port=port,
                                 db=database,
                                 password=password)
    
    df = pd.read_sql(query, connection)
    return df

if __name__ == '__main__':
    main()