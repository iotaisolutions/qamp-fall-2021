## Project 39: Tutorial to use K8S Cluster (Qiskit Advocate Mentorship Program: Fall 2021)

## Background
Simulation of quantum applications like quantum chemistry, materials science, quantum biology, generates quantum systems which are much larger than computational NISQ devices, this gap can be handled by parallelizing the quantum simulation. \
\
**Qiskit Aer** is a Noisy quantum circuit simulator backend and runs simulation jobs on a single-worker Python multiprocessing **ThreadPool** executor so that all parallelization is handled by low-level OpenMP and CUDA code (For Multi CPU / Core & GPU environment). \
\
**Variational Quantum Eigensolver (VQE)** and the other compute intensive variational algorithms) already support generating circuits together for parallel gradient computation. In order to customize job-level parallel execution of multiple circuits, a custom multiprocessing executor can be specified, which controls the splitting of circuits using the executor and max_job_size backend options of Qiskit AerSimulator. \
\
In order  to simulate parallel execution  on premise as well as cloud  environment, dedicated compute resources might be required, but available with constraints, both on scalability and manageability.

## Solution Overview 

- For large scale job parallelization on HPC clusters, Qiskit Aer executors also support the distributed Clients from the **DASK (parallel computing library for Python). DASK         natively scales Python and suitable for applications which require a distributed, auto scaling compute environment that is completely independent of application.**
- **Using Kubernetes  clusters**, DASK worker environment can be either scaled up manually, or can be scaled as the need arises by creating auto scaling rules in Kubernetes             configuration, which means DASK only need to manage scheduling across workers in Kubernetes Cluster , as work go up or down.
- **Qiskit Aer** contains an option, **"executor"**, to use a custom executor which supports **Threadpool** Executor and DASK client . This option can be scaled up easily and speed up simulation with parallelization. If the user setups DASK cluster with multiple nodes, Aer can execute the simulation in parallel across the multiple nodes like High Performance Computing (HPC) environment. Especially, the simulation time of multiple circuits and a noise simulation can much decrease based on the number of worker nodes because multiple nodes can independently run different simulations.
- The AerSimulator supports multiple simulation methods and configurable options for each simulation method. These may be set using the appropriate kwargs during initialization.     They can also be set of updated using the **set_options()** method. Adds a new option of the backend to provide the user's executor. 
- When user gives Dask client as executor, Aer can execute a simulation on the distributed machines like HPC clusters. When the executor is set, AerJobSet object is returned         instead of a normal AerJob object. AerJobSet divides multiple experiments in one qobj into each experiment and submits each qobj to the executor as AerJob. After       simulations,AerJobSet collects each result and combines them into one result object.

                                                       
**Architecture of Clustered Backend for Aer Simulator**
                                                                             
 ![GitHub Dark](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Architecture%20of%20Clustered%20Backend%20for%20Aer%20Simulator.png#gh-light-mode-only)
 
## Solution Components Overview
### Kubernetes

Kubernetes is an open-source platform for deploying and managing containers. It provides a container runtime, container orchestration, container-centric infrastructure orchestration, self-healing mechanisms, service discovery and load balancing. It’s used for the deployment, scaling, management, and composition of application containers across clusters of hosts. 

![Kubernetes Components](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg) 

To have in-depth understanding of Kubernetes Concepts refer [Kubernetes Official Documentation](https://kubernetes.io/docs/home/)

### DASK

- Is Distributed compute scheduler built to scale  Python. Adapts to custom algorithms with a flexible task scheduler
  Parallelizes libraries like NumPy, Pandas, and Scikit-Learn.
- Scales workloads from laptops to  supercomputer clusters 
- Is Extremely modular: disjoint scheduling,  compute, data transfer and out-of-core  handling
- Parallelizes libraries like NumPy, Pandas, and Scikit-Learn
![DASK Architecture](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/DASK%20Architecture.PNG)
To have in-depth understanding of DASK Concepts refer [DASK Documentation](https://docs.dask.org/en/stable/)

### DASK Kubernetes
Dask Kubernetes Module provides cluster managers for Kubernetes.

**KubeCluster** Module deploys Dask clusters on Kubernetes clusters using native Kubernetes APIs. It is designed to dynamically launch ad-hoc deployments.

To have in-depth understanding of DASK Kubernetes Concepts refer [DASK Kubernetes Documentation](https://kubernetes.dask.org/en/latest/kubecluster.html)

### Qiskit Aer Simulator 

Qiskit is an open-source framework for working with noisy quantum computers at the level of pulses, circuits, and algorithms.

Qiskit is made up of elements that each work together to enable quantum computing. This element is **Aer**, which provides high-performance quantum computing simulators with realistic noise models.

## Application Stack 
  Below table covers Application Stack for implementing the Clustered Backend for AER Simulator:

Operating System Platform| Programming Language| Quantum Compluting Development Platform | Container Platform | Distributed / HPC Platform| Coding Environment | Cloud Platform (Optional) 
------------ | -------------| -------------| -------------| -------------|-------------|-------------|
 Ubuntu Instance with **2vCPU and 4GB RAM** ![Ubuntu](https://thumbor.forbes.com/thumbor/fit-in/1200x0/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5ec418c2ac01e2000762cfdd%2F0x0.jpg )| Python >= Version 3.8![Python](https://miro.medium.com/max/1400/0*BjcKs4_BdpYCiybp.png)  |  Qiskit >= Version 0.30.0 & AER Simulator > Version 0.10.0  ![Qiskit](https://img.shields.io/badge/Qiskit%200.30-%236929C4.svg?style=for-the-badge&logo=Qiskit&logoColor=white)| Kubernetes >= Version 19.15 ![Kubernetes](https://www.pngitem.com/pimgs/m/3-31510_svg-kubernetes-logo-hd-png-download.png) | Dask-kubernetes >= Version 2021.10.0 ![HPC Cluster Platform](https://user-images.githubusercontent.com/68344826/143777777-1dc83d72-256f-4f60-b329-356167f037a1.png)| ![Jupyter Notebook](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png) |![AWS Cloud](https://www.techrepublic.com/a/hub/i/r/2016/08/03/78fd9253-5cce-47e0-8961-77460e957405/thumbnail/770x578/30e06bd910bad09134f56e3ee490f4ef/icon-cloud-aws.png)
 
 ## Step by Step Guide for Setup of Clustered Backend Environment for AER Simulator
1. Install a compatible Linux CI host (Preferably based on Debian and Red Hat), with at least 2 CPU and 4 GB RAM , with latest patch & package level.  
2. Setup a Kubernetes Cluster Environment (with latest patch & package level):
    - On Premise or Cloud, Learning Environment [**Using Minikube : Single Node variant of K8s**](https://minikube.sigs.k8s.io/docs/start) 
    - On Premise Production Environment (**with at least one Kubernetes Master & Two (Worker) Nodes**) Environment by referring [Kubernetes Setup Documentation](https://kubernetes.io/docs/setup/) 
    - On Cloud Platform Production Environment ([like on AWS](https://zero-to-jupyterhub.readthedocs.io/en/latest/kubernetes/amazon/step-zero-aws.html)) 
    - **Snip of a Multinode Kubernetes Cluster Environment** ![Cluster](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Kubernetes%20Cluster%20Snapshot.PNG) 
3. Ensure latest patch & package on Linux CI host, Kubetnetes Master & (Worker) Nodes, for e.g. running below commands on Ubuntu 20.04 LTS OS plaform 
    - **$sudo apt update**
    - **$sudo apt -y upgrade** \
   Once the process is complete, check the version of Python 3 that is installed in the system by typing:
   - **$python3 -V**\
     You’ll receive output in the terminal window that will let you know the version number. While this number may vary, the output will be similar to this:\
     Output\
     **Python 3.8.10**
   - Install Optimized BLAS (linear algebra) library (development files) on Linux CI host, Kubetnetes Master & (Worker) Nodes\
     **$sudo apt-get install libopenblas-dev** 
4. On Linux CI host, Kubetnetes Master & (Worker) Nodes, to manage software packages for Python, install pip, a tool that will install and manage programming packages:
   - **$sudo apt install -y python3-pip**
   - (Optionally) Setup a [Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for Python, which enable you to have an isolated space on your server for Python projects, ensuring that each of your projects can have its own set of dependencies that won’t disrupt any of your other projects. 
5. **DASK Environment Preperation**
    - Install **DASK Distributed & Kubernetes** Package with Python Dependencies on Linux CI host\
       **$sudo pip install dask distributed --upgrade** # A distributed task scheduler for Dask\
       **$sudo pip install dask-kubernetes --upgrade**  # DASK Kubernetes Module 

       For other installation options refer [DASK Distributed Documentation](http://distributed.dask.org/en/stable/install.html) & [DASK Kubernetes Documentation](https://kubernetes.dask.org/en/latest/installing.html) 
    - Install Qiskit SDK package(s) 
      On Linux CI host **preferably in Python Virtual Environment** \
      **$sudo pip install qiskit**\
      Optionally install Application Modules & Visualization functionality (like Plots , Jupyter Notebooks), as per requirement of program, e.g **Qiskit Nature ( for VQE )** \
      **$sudo pip install qiskit[nature]**\
      **$sudo pip install qiskit[visualization]**
    - Prepare Dask Worker Pod Specification YAML file for Aer Simulator.  **Note: The specification should include installation of DASK & Qiskit packages**.Refer sample [Worker Spec YAML file](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Sample%20Code/worker-spec.yml).
    - Refer [KubeCluster](https://kubernetes.dask.org/en/latest/kubecluster.html) for other available options for defining DASK Worker/ Pod. 
    - Check Kubernetes Cluster Status ![Cluster Status](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Kubernetes%20Cluster%20Status.PNG)
6. **Run a simple test DASK script** 

 - ![DASK Array](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Sample%20DASK%20Test%20Script.PNG) 
 - ![Dask array pod](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Sample%20DASK%20Test%20Script%20Spawn.PNG) 
 - ![Dask Array Output](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Images/Sample%20DASK%20Test%20Script%20Output.PNG)
 
