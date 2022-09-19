Philosophy
**********

Engineering Side of Data Science
================================

Project or Product?
-------------------

When talking about the data science, a widely adopted mindset is that it follows a **project workflow**: start with business requirements, work out with a rough solution, get the data and explore it, do research and develop alorithms, and deploy it. The general idea behind the mindset is logically correct, while the drawback is clear as well -- it focuses on the project setup but underestimates the **application or product** nature of the data science.

Balancing the project and product nature of the data science, the **BatCat** is designed to free data scientists from project management and engineering stuffs and help them focus on data science experiments and better alogrithms. 

Two-flow Design
---------------

The **BatCat** abstracts the data science practice into **two main flows: 1) the data flow and 2) the workflow**. Each flow has its place to **store: 1) S3 and 2) GitHub** and interact at computing stage: the **Docker container**.

.. image:: images/flows.png
  :align: center
  
**The data flow** moves from the storage (AWS S3 here) to the process stage, becomes insights which is also data, and finally stores back to storage for further usage, like BI or UI/UX presentation. From this perspective, a data science product is more like **a data processing**. 

**The workflow** is triggered by events or requests or on schedule to process the data flow; and itself is managed and stored in GitHub or any other Git repository hosting services. From this perspective, a data science product is more like **a software product**.

**The two flows converges in the computing process, which happens in the Docker container in the BatCat setting.** And this is where the data science algorithms really make magic.

.. note::

    The setting above is based on **batch data science**, not real-time ones. For more about real-time data science or machine learning, check out `Chip Huyen's blog <https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html>`_.


Machine Learning Operations on AWS
==================================

Setting up a data science or machine learning workflow in the production environment follows the philosophy above but with more functions and services on AWS. The related services fall into four main categories:

1. **Data Science Experiments**: SageMaker, Git, Docker.
2. **Storage**: S3, RedShift, Athena.
3. **Processing Container**: Docker, Step Functions.
4. **Trigger**: Lambda.
5. **Monitor**: CloudWatch.

.. image:: images/aws.png 
  :align: center

.. note::
    
    The above landscape is based on the services avaible in AWS China so there remains space to improve when more serivices are accessible. 



