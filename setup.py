#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'batcat'
DESCRIPTION = 'BatCat, A Cat Looks Like A Bat.'
URL = 'https://github.com/Ewen2015/BatCat'
EMAIL = 'wolfgangwong2012@gmail.com'
AUTHOR = 'Ewen Wang'
REQUIRED = [
    'pandas', 
    'boto3==1.18.57',
    'botocore==1.21.57',
    'protobuf==3.20.*',
    'awscli==1.20.57', 
    'requests==2.26.0', 
    'sagemaker==2.59.8', 
    'stepfunctions==2.2.0',
    'sagemaker-experiments==0.1.35', 
    'pyathena==2.3.0', 
    'redshift_connector==2.0.888', 
    'sqlalchemy==1.3.23',
    'psycopg2-binary==2.9.1'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
