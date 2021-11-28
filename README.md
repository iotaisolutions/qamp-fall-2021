# qamp-fall-2021
## Project 39: Tutorial to use K8S Cluster (Qiskit Advocate Mentorship Program: Fall 2021)

## Background
Simulation of quantum applications like quantum chemistry, materials science, quantum biology, generates quantum systems which are much larger than computational NISQ devices, this gap can be handled by parallelizing the quantum simulation. \
\
**Qiskit Aer** is a Noisy quantum circuit simulator backend and runs simulation jobs on a single-worker Python multiprocessing ThreadPool executor so that all parallelization is handled by low-level OpenMP and CUDA code (For Multi CPU / Core & GPU environment). \
\
**Variational Quantum Eigensolver (VQE)** and the other compute intensive variational algorithms) already support generating circuits together for parallel gradient computation. In order to customize job-level parallel execution of multiple circuits, a custom multiprocessing executor can be specified, which controls the splitting of circuits using the executor and max_job_size backend options of Qiskit AerSimulator. \
\
In order  to simulate parallel execution  on premise as well as cloud  environment, dedicated compute resources might be required, but available with constraints, both on scalability and manageability.

## Solution Overview 

- For large scale job parallelization on HPC clusters, Qiskit Aer executors also support the distributed Clients from the **DASK (parallel computing library for Python). DASK         natively scales Python and suitable for applications which require a distributed, auto scaling compute environment that is completely independent of application.**
- Using Kubernetes  clusters, DASK worker environment can be either scaled up manually, or can be scaled as the need arises by creating auto scaling rules in Kubernetes             configuration, which means DASK only need to manage scheduling across workers in Kubernetes Cluster , as work go up or down.
-The AerSimulator supports multiple simulation methods and configurable options for each simulation method. These may be set using the appropriate kwargs during initialization.     They can also be set of updated using the set_options() method. Adds a new option of the backend to provide the user's executor. 
- When user gives Dask client as executor, Aer can execute a simulation on the distributed machines like HPC clusters. When the executor is set, AerJobSet object is returned         instead of a normal AerJob object. AerJobSet divides multiple experiments in one qobj into each experiment and submits each qobj to the executor as AerJob. After       simulations,AerJobSet collects each result and combines them into one result object.
                                                       
**Architecture of Clustered Backend for Aer Simulator**
                                                                             
 ![GitHub Dark](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Architecture%20of%20Clustered%20Backend%20for%20Aer%20Simulator.png#gh-light-mode-only)
 
 # Application Stack 
  Below table covers Application Stack for implementing this project:

Programming Language| Classical (Deep) ML Framework| Quantum Compluting Development Platform | Simulator | Additional Module| Coding Collaboration Environment 
------------ | -------------| -------------| -------------| -------------|-------------
  ![Python](https://img.shields.io/badge/python%203.x%20>=%203.7-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  |  ![PyTorch](https://img.shields.io/badge/PyTorch%201.9-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) |  ![Qiskit](https://img.shields.io/badge/Qiskit%200.29-%236929C4.svg?style=for-the-badge&logo=Qiskit&logoColor=white) |  IBM QASM ( With Qiskit Runtime) & AER Simulator (for local)  from https://github.com/Qiskit-Partners/qiskit-runtime | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Naereen/badges)

