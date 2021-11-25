GossipCat, A Cat Looks Like A Bat
===

[![GitHub version](https://badge.fury.io/gh/ewen2015%2Fbatcat.svg)](https://badge.fury.io/gh/ewen2015%2Fbatcat)
![GitHub](https://img.shields.io/github/license/ewen2015/batcat)
[![PyPI version](https://badge.fury.io/py/batcat.svg)](https://badge.fury.io/py/batcat)
[![Python Versions](https://img.shields.io/pypi/pyversions/batcat.svg)](https://pypi.python.org/pypi/batcat)

😸😹😺😻😼😽😾😿🙀🐱

BatCat is designed to help data scientists to practice machine learning operations (MLOps) on Amazon Web Services (AWS). 

Services of AWS covered:
- AWS Lambda: a serverless, event-driven compute service
- AWS S3 (Simple Storage Service): provides object storage service
- Amazon Athena: a serverless, interactive query service on S3
- Amazon Redshift: a data warehouse product

Philosophy of BatCat's MLOps
---

BatCat practices MLOps in **3 layers (ASA)**:

1. **Algorithm level**: which is on machine learning algorithm itself, it cares about learning curve, iteration rounds, metrics, etc. 
2. **System level**: which treats the machine learning project as a system itself, it focuses on resources ultized and health of the machine learning pipeline.
3. **Application level**: which put the machine learning system as one of parts in a large process, it connects data producers from upstream and data consumers from downstreams. 

#### 1. Algorithm level

Tool: [GossipCat](https://github.com/Ewen2015/GossipCat), [TensorBoard](https://www.tensorflow.org/tensorboard)

<p align="center">
<img src='https://raw.githubusercontent.com/Ewen2015/BatCat/master/gc_learning_curve.png'>
</p>

<p align="center">
<img width="600" height="400" src='https://github.com/Ewen2015/BatCat/blob/master/tensorboard.gif'>
</p>

#### 2. System level

Tool: AWS Cloudwatch

<p align="center">
<img src='https://raw.githubusercontent.com/Ewen2015/BatCat/master/aws_cloudwatch.png'>
</p>

#### 3. Application level

Tool: DataOps

BatCat realizes application level MLOps by monitoring the distributions of data inputs (data source) and data outputs (predictions). As the applicaiton levle MLOps is a part of the whole DataOps, it should algin with the practice of DataOps according to each organziation or company.

Story of the BatCat
---

The package names after a cat of my friend, Clara. 

<p align="center">
<img width="500" height="500" src="https://raw.githubusercontent.com/Ewen2015/BatCat/master/BatCat.jpeg">
</p>

License
---

BatCat is licensed under the [MIT License](https://github.com/Ewen2015/BatCat/blob/master/LICENSE). © Contributors, 2021.
