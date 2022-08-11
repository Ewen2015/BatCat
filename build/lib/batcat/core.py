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

    Args:
        delta (int): The number of days ago.
    
    Returns:
        date (str): strftime('%Y/%m/%d').
    """
    from datetime import date, timedelta
    return (date.today() - timedelta(days=delta)).strftime(format)

def read_data_from_bd(query, 
                      host,
                      user, 
                      port,
                      database,
                      password):
    """Read data from a database.

    Args:
        query (str): Querry to obtain data from Redshift, str.
        host (str): Redshift configuration.
        user (str): Redshift configuration.
        port (str): Redshift configuration.
        password (str): Redshift configuration.
        database (str): Redshift configuration.

    Returns:    
        df (pandas.DataFrame): Dataframe. 
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