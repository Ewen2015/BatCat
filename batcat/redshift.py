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
from redshift_connector import connect

def read_data_from_redshift(query, 
                            host,
                            password,
                            port=5439,
                            database='dev',
                            user='awsuser',
                            date_start=None, 
                            date_end=None) -> pd.DataFrame:
    """
    arg: 
        query: querry to obtain data from Redshift, str
        host: Redshift configuration
        password: Redshift configuration
        port: Redshift configuration
        database: Redshift configuration
        user: Redshift configuration
        date_start: date to start, strftime('%Y/%m/%d')
        date_start: date to end, strftime('%Y/%m/%d')
    return:
        df: target dataframe
    """
    
    cursor = connect(host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password).cursor()
    
    query = query.format(date_start, date_end) 
    cursor.execute(query)
    
    df = cursor.fetch_dataframe()
    return df

def save_df_to_redshift(df,
                        table_name,
                        dtype=None,
                        host=None,
                        password=None,
                        port=5439,
                        database='dev',
                        user='awsuser',
                        if_exists='replace'):
    """
    arg: 
        df: target dataframe
        table_name: target table name'
        dtype: dict or scalar, optional
            Specifying the datatype for columns. If a dictionary 
            is used, the keys should be the column names and the 
            values should be the SQLAlchemy types or strings for 
            the sqlite3 legacy mode. If a scalar is provided, it 
            will be applied to all columns.
        if_exists: {‘fail’, ‘replace’, ‘append’}, default ‘fail’
            How to behave if the table already exists.
            fail: Raise a ValueError.
            replace: Drop the table before inserting new values.
            append: Insert new values to the existing table.
        host: Redshift configuration
        password: Redshift configuration
        port: Redshift configuration
        database: Redshift configuration
        user: Redshift configuration
    """
    from sqlalchemy import create_engine
    
    con = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT, DATABASE))
    df.to_sql(name=table_name, con=con, schema=None, if_exists=if_exists, index=False, index_label=None, chunksize=None, dtype=dtype, method=None)
    return None


if __name__ == '__main__':
    main()
