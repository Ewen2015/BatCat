#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""

import json
from .Logging import get_logger

def get_config(file='config.json'):
    """Get configurations.

    Args:
        file (str): Configuration file, dedault 'config.json'.

    Return:
        config: A configuration dictionary.
    """
    logger = get_logger(logName='configure')
    config = dict()
    try:
        with open(file, 'r') as f:
            config = json.load(f)
        logger.info('Configuration loaded.')
        return config 
    except Exception as e:
        logger.error('NO CONFIGURATION FILE FOUND!')
        raise e

if __name__ == '__main__':
    main()