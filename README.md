## Project 39: Tutorial to use K8S Cluster (Qiskit Advocate Mentorship Program: Fall 2021) as backend for Aer Simulator

## Background
Simulation of quantum applications like quantum chemistry, materials science, quantum biology, generates quantum systems which are much larger than computational NISQ devices, this gap can be handled by parallelizing the quantum simulation. \
\
**Qiskit Aer** is a Noisy quantum circuit simulator backend and runs simulation jobs on a single-worker Python multiprocessing **ThreadPool** executor so that all parallelization is handled by low-level OpenMP and CUDA code (For Multi CPU / Core & GPU environment). \
\
**Variational Quantum Eigensolver (VQE)** and the other compute intensive variational algorithms) already support generating circuits together for parallel gradient computation. In order to customize job-level parallel execution of multiple circuits, a custom multiprocessing executor can be specified, which controls the splitting of circuits using the executor and max_job_size backend options of Qiskit AerSimulator. \
\
In order  to simulate parallel execution  on premise as well as cloud  environment, dedicated compute resources might be required, but available with constraints, both on scalability and manageability.

## Solution Overview 

- **Qiskit Aer** contains an option, **"executor"**, to use a custom executor which supports **Threadpool** Executor and distributed clients like **DASK (parallel computing library for Python).** This option can be scaled up easily and speed up simulation with parallelization. With DASK cluster of multiple nodes, Aer can execute the simulation in parallel across the multiple nodes like High Performance Computing (HPC) environment. Especially, the simulation time of multiple circuits and a noise simulation can much decrease based on the number of worker nodes because multiple nodes can independently run different simulations.
- **Using Kubernetes  clusters**, DASK worker environment can be either scaled up manually, or can be scaled as the need arises by creating auto scaling rules in Kubernetes             configuration, which means DASK only need to manage scheduling across workers in Kubernetes Cluster , as work go up or down.
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
- Suitable for applications which require a distributed, auto scaling compute environment that is completely independent of application.

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
    - On Cloud Platform Production Environment ([Setup Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest/kubernetes/setup-kubernetes.html)) 
    - **Snip of a Multinode Kubernetes Cluster Environment** 
     ```bash
        $ kubectl get nodes –A # One Master & 2 Worker Nodes
        NAME                            STATUS   ROLES                  AGE     VERSION
        ip-172-20-33-106.ec2.internal   Ready    node                   2d19h   v1.22.2
        ip-172-20-51-193.ec2.internal   Ready    node                   2d19h   v1.22.2
        ip-172-20-61-190.ec2.internal   Ready    control-plane,master   2d19h   v1.22.2

        $ kubectl get pods –A # Pods for Kubernetes Environment
        NAMESPACE     NAME                                                    READY   STATUS    RESTARTS        AGE
        kube-system   coredns-5dc785954d-82nf5                                1/1     Running   0               2d19h
        kube-system   coredns-5dc785954d-r5ksr                                1/1     Running   0               2d19h
        kube-system   coredns-autoscaler-84d4cfd89c-hzn5k                     1/1     Running   0               2d19h
        kube-system   dns-controller-c459588c4-rd7rd                          1/1     Running   0               2d19h
        kube-system   ebs-csi-controller-bf875d89b-r4rcz                      6/6     Running   0               2d19h
        kube-system   ebs-csi-node-dzvl9                                      3/3     Running   0               2d19h
        kube-system   ebs-csi-node-smffl                                      3/3     Running   0               2d19h
        kube-system   ebs-csi-node-spdzr                                      3/3     Running   0               2d19h
        kube-system   etcd-manager-events-ip-172-20-61-190.ec2.internal       1/1     Running   0               2d19h
        kube-system   etcd-manager-main-ip-172-20-61-190.ec2.internal         1/1     Running   0               2d19h
        kube-system   kops-controller-sr5lp                                   1/1     Running   0               2d19h
        kube-system   kube-apiserver-ip-172-20-61-190.ec2.internal            2/2     Running   1 (2d19h ago)   2d19h
        kube-system   kube-controller-manager-ip-172-20-61-190.ec2.internal   1/1     Running   3 (2d19h ago)   2d19h
        kube-system   kube-proxy-ip-172-20-33-106.ec2.internal                1/1     Running   0               2d19h
        kube-system   kube-proxy-ip-172-20-51-193.ec2.internal                1/1     Running   0               2d19h
        kube-system   kube-proxy-ip-172-20-61-190.ec2.internal                1/1     Running   0               2d19h
        kube-system   kube-scheduler-ip-172-20-61-190.ec2.internal            1/1     Running   0               2d19h
    ```

3. Ensure latest patch & package on Linux CI host, Kubetnetes Master & (Worker) Nodes, for e.g. running below commands on Ubuntu 20.04 LTS OS plaform 
    ```bash
    - $sudo apt update
    - $sudo apt -y upgrade
    ```
   Once the process is complete, check the version of Python 3 that is installed in the system by typing:
   ```bash
   - $python3 -V
   ```
     You’ll receive output in the terminal window that will let you know the version number. While this number may vary, the output will be similar to this:\
   ```bash
     Python 3.8.10*
   ```
   - Install Optimized BLAS (linear algebra) library (development files) on Linux CI host, Kubetnetes Master & (Worker) Nodes\
   ```bash
     $sudo apt-get install libopenblas-dev
    ```
4. On Linux CI host, Kubetnetes Master & (Worker) Nodes, to manage software packages for Python, install pip, a tool that will install and manage programming packages:
   ```bash
   - $sudo apt install -y python3-pip
   ```
   - (Optionally) Setup a [Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for Python, which enable you to have an isolated space on your server for Python projects, ensuring that each of your projects can have its own set of dependencies that won’t disrupt any of your other projects. 
5. **DASK Environment Preperation**
    - Install **DASK Distributed & Kubernetes** Package with Python Dependencies on Linux CI host\
       ```bash
       $sudo pip install dask distributed --upgrade # A distributed task scheduler for Dask
       $sudo pip install dask-kubernetes --upgrade  # DASK Kubernetes Module 
       ```
       For other installation options refer [DASK Distributed Documentation](http://distributed.dask.org/en/stable/install.html) & [DASK Kubernetes Documentation](https://kubernetes.dask.org/en/latest/installing.html) 
    - Install Qiskit SDK package(s) 
      On Linux CI host **preferably in Python Virtual Environment** \
      ```bash
      $sudo pip install qiskit
      ```
      Optionally install Application Modules & Visualization functionality (like Plots , Jupyter Notebooks), as per requirement of program, e.g **Qiskit Nature ( for VQE )** \
      ```bash
      $sudo pip install qiskit[nature]
      $sudo pip install qiskit[visualization]
      ```
    - Prepare Dask Worker Pod Specification YAML file for Aer Simulator.  **Note: The specification should include installation of DASK & Qiskit packages**.Refer sample [Worker Spec YAML file](https://github.com/iotaisolutions/qamp-fall-2021/blob/main/Sample%20Code/worker-spec.yml).
    - Refer [KubeCluster](https://kubernetes.dask.org/en/latest/kubecluster.html) for other available options for defining DASK Worker/ Pod. 
    - Check Kubernetes Cluster Status:
    ```bash
         ubuntu@ip-172-31-93-214:~$ kubectl get nodes
         NAME                            STATUS   ROLES                  AGE   VERSION
         ip-172-20-33-106.ec2.internal   Ready    node                   24d   v1.22.2
         ip-172-20-51-193.ec2.internal   Ready    node                   24d   v1.22.2
         ip-172-20-61-190.ec2.internal   Ready    control-plane,master   24d   v1.22.2
    ```  
   
6. **Run a simple test DASK script** 

   ```bash
      #Python Script for Dask Array Mean Calculation

      from dask_kubernetes import KubeCluster
      from dask.distributed import Client
      cluster = KubeCluster('worker-spec.yml')

      cluster.scale(3)  # specify number of DASK workers explicitly
      cluster.adapt(minimum=1, maximum=10)  # or dynamically scale based on current workload

      # Connect Dask to the cluster
      client = Client(cluster)


      import time
      time.sleep(60)
      # Example usage
      import dask.array as da


      # Create a large array and calculate the mean
      array = da.ones((1000, 1000, 1000))
      print("Ärray Mean", array.mean().compute())# Should print 1.0
      ```
      
      **#During Script execution Dask Worker Pod(s) are automatically spawned on Kubernetes Nodes as per load**
      ```bash
      $ kubectl get pods -A|grep -i dask
      default       dask-ubuntu-c3d47733-3xx6k8  1/1     Running   0  18s
      ```
      #Script Output
      ```bash
      Creating scheduler pod on cluster. This may take some time.
      distributed.deploy.adaptive - INFO - Adaptive scaling started: minimum=1 maximum=10
      distributed.deploy.adaptive - INFO - Retiring workers [0, 1]
      /usr/local/lib/python3.8/dist-packages/distributed/client.py:1128: Version MismatchWarning: Mismatched versions found

      +-------------+------------------------+-----------+---------+
      | Package     | client                 | scheduler | workers |
      +-------------+------------------------+-----------+---------+
      | blosc       | None                   | 1.10.2    | None    |
      | dask        | 2021.09.1              | 2021.10.0 | None    |
      | distributed | 2021.09.1+43.g842cc758 | 2021.10.0 | None    |
      | lz4         | None                   | 3.1.3     | None    |
      +-------------+------------------------+-----------+---------+
        warnings.warn(version_module.VersionMismatchWarning(msg[0]["warning"]))
      Ärray Mean 1.0
      distributed.deploy.adaptive_core - INFO - Adaptive stop
      distributed.deploy.adaptive_core - INFO - Adaptive stop
      ```



 
