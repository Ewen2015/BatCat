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

.. image:: images/flows.svg 
  :align: center
  
**The data flow** moves from the storage (AWS S3 here) to the process stage, becomes insights which is also data, and finally stores back to storage for further usage, like BI or UI/UX presentation. From this perspective, a data science product is more like **a data processing**. 

**The workflow** is triggered by events or requests or on schedule to process the data flow; and itself is managed and stored in GitHub or any other Git repository hosting services. From this perspective, a data science product is more like **a software product**.

**The two flows converges in the computing process, which happens in the Docker container in the BatCat setting.** And this is where the data science algorithms really make magic. 