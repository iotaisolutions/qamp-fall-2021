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
- **Using Kubernetes  clusters**, DASK worker environment can be either scaled up manually, or can be scaled as the need arises by creating auto scaling rules in Kubernetes             configuration, which means DASK only need to manage scheduling across workers in Kubernetes Cluster , as work go up or down.
-The AerSimulator supports multiple simulation methods and configurable options for each simulation method. These may be set using the appropriate kwargs during initialization.     They can also be set of updated using the **set_options()** method. Adds a new option of the backend to provide the user's executor. 
- When user gives Dask client as executor, Aer can execute a simulation on the distributed machines like HPC clusters. When the executor is set, AerJobSet object is returned         instead of a normal AerJob object. AerJobSet divides multiple experiments in one qobj into each experiment and submits each qobj to the executor as AerJob. After       simulations,AerJobSet collects each result and combines them into one result object.
                                                       
**Architecture of Clustered Backend for Aer Simulator**
                                                                             
 ![GitHub Dark](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Architecture%20of%20Clustered%20Backend%20for%20Aer%20Simulator.png#gh-light-mode-only)
 
 # Application Stack 
  Below table covers Application Stack for implementing this project:

Operating System Platform| Programming Language| Quantum Compluting Development Platform | Container Platform | HPC Platform| Coding Documentation | Cloud Platform  
------------ | -------------| -------------| -------------| -------------|-------------
 Ubuntu Instance with 4vCPU and 16GB RAM ![Ubuntu](https://thumbor.forbes.com/thumbor/fit-in/1200x0/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5ec418c2ac01e2000762cfdd%2F0x0.jpg )|![Python](https://miro.medium.com/max/1400/0*BjcKs4_BdpYCiybp.png)  |  IBM QASM & AER Simulator  ![Qiskit](https://img.shields.io/badge/Qiskit%200.30-%236929C4.svg?style=for-the-badge&logo=Qiskit&logoColor=white)| Kubernetes >= 19.15 ![Kubernetes] (https://www.stratoscale.com/wp-content/uploads/2019/04/Kubernetes-logo.png) | ![HPC Cluster Platform](![image](https://user-images.githubusercontent.com/68344826/143777777-1dc83d72-256f-4f60-b329-356167f037a1.png))| ![Jupyter Notebook](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png) |![AWS Cloud](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.citypng.com%2Fphoto%2F2650%2Forange-cloud-contains-white-amazon-aws-logo&psig=AOvVaw2HcK543myTrB59187sE2G1&ust=1638204629726000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLDPhpTCu_QCFQAAAAAdAAAAABAD)

