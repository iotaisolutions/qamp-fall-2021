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

**Helm** , the package manager for Kubernetes, is a useful command line tool for: installing, upgrading and managing applications on a Kubernetes cluster. Helm packages are called charts. We will be installing and managing JupyterHub on our Kubernetes cluster using a Helm chart.

Charts are abstractions describing how to install packages onto a Kubernetes cluster. When a chart is deployed, it works as a templating engine to populate multiple yaml files for package dependencies with the required variables, and then runs kubectl apply to apply the configuration to the resource and install the package.


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

To have in-depth understanding of DASK Kubernetes Concepts refer [DASK Kubernetes Documentation](https://kubernetes.dask.org/en/latest/kubecluster.html).


**KubeCluster** deploys Dask clusters on Kubernetes clusters using native Kubernetes APIs. It is designed to dynamically launch ad-hoc deployments.

**HelmCluster** is for managing an existing Dask cluster which has been deployed using Helm. You must have already installed the Dask Helm chart and have the cluster running. You can then use it to manage scaling and retrieve logs.

Kubernetes can be used to launch Dask workers in the following **two ways:**


1. **Helm:**

You can deploy Dask and (optionally) Jupyter or JupyterHub on Kubernetes easily using Helm
```bash
helm repo add dask https://helm.dask.org/    # add the Dask Helm chart repository
helm repo update                             # get latest Helm charts
# For single-user deployments, use dask/dask
helm install my-dask dask/dask               # deploy standard Dask chart
# For multi-user deployments, use dask/daskhub
helm install my-dask dask/daskhub            # deploy JupyterHub & Dask
```
This is a good choice if you want to do the following:

- Run a managed Dask cluster for a long period of time
- Also deploy a Jupyter / JupyterHub server from which to run code
- Share the same Dask cluster between many automated services
- Try out Dask for the first time on a cloud-based system like Amazon, Google, or Microsoft Azure where you already have a Kubernetes cluster. If you don’t already have Kubernetes deployed, see our Cloud documentation.

You can also use the HelmCluster cluster manager from dask-kubernetes to manage your Helm Dask cluster from within your Python session.
```bash
from dask_kubernetes import HelmCluster
cluster = HelmCluster(release_name="myrelease")
cluster.scale(10)
```

2. **Native:** You can quickly deploy Dask workers on Kubernetes from within a Python script or interactive session using Dask-Kubernetes

```bash 
from dask_kubernetes import KubeCluster
cluster = KubeCluster.from_yaml('worker-template.yaml')
cluster.scale(20)  # add 20 workers
cluster.adapt()    # or create and destroy workers dynamically based on workload

from dask.distributed import Client
client = Client(cluster)
```
This is a good choice if you want to do the following:

- Dynamically create a personal and ephemeral deployment for interactive use
- Allow many individuals the ability to launch their own custom dask deployments, rather than depend on a centralized system
- Quickly adapt Dask cluster size to the current workload


### Qiskit Aer Simulator 

Qiskit is an open-source framework for working with noisy quantum computers at the level of pulses, circuits, and algorithms.

Qiskit is made up of elements that each work together to enable quantum computing. This element is **Aer**, which provides high-performance quantum computing simulators with realistic noise models.

## Application Stack 
  Below table covers Application Stack for implementing the Clustered Backend for AER Simulator:

Operating System Platform| Programming Language| Quantum Compluting Development Platform | Container Platform | Distributed / HPC Platform| Coding Environment | Cloud Platform (Optional) 
------------ | -------------| -------------| -------------| -------------|-------------|-------------|
 Ubuntu Instance with **2vCPU and 4GB RAM** ![Ubuntu](https://thumbor.forbes.com/thumbor/fit-in/1200x0/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5ec418c2ac01e2000762cfdd%2F0x0.jpg )| Python >= Version 3.8![Python](https://miro.medium.com/max/1400/0*BjcKs4_BdpYCiybp.png)  |  Qiskit >= Version 0.30.0 & AER Simulator > Version 0.10.0  ![Qiskit](https://img.shields.io/badge/Qiskit%200.30-%236929C4.svg?style=for-the-badge&logo=Qiskit&logoColor=white)| Kubernetes >= Version 19.15 ![Kubernetes](https://www.pngitem.com/pimgs/m/3-31510_svg-kubernetes-logo-hd-png-download.png) | Dask-kubernetes >= Version 2021.10.0 ![HPC Cluster Platform](https://user-images.githubusercontent.com/68344826/143777777-1dc83d72-256f-4f60-b329-356167f037a1.png)| ![Jupyter Notebook](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png) |![AWS Cloud](https://www.techrepublic.com/a/hub/i/r/2016/08/03/78fd9253-5cce-47e0-8961-77460e957405/thumbnail/770x578/30e06bd910bad09134f56e3ee490f4ef/icon-cloud-aws.png)
 
 ## Step by Step Guide for Setup of Clustered Backend Environment for AER Simulator
 ### Setup Kubernetes Environment
  - Install a compatible Linux CI host (Preferably based on Debian and Red Hat), with at least 2 CPU and 4 GB RAM.
  - SSH to Linux CI host
  - Choose a cluster name:
    Consider there is no pre-configured DNS and use the suffix like “.k8s.local”. Per the docs, if the DNS name ends in .k8s.local the cluster will use internal hosted DNS.
     ```bash
        export NAME=<somename>.k8s.local
     ```
  - Setup an ssh keypair to use with the cluster:
     ```bash
        ssh-keygen
     ```
  - Deploy a Kubernetes Cluster Environment (with latest patch & package level):
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

  - Ensure latest patch & package on Linux CI host, Kubetnetes Master & (Worker) Nodes, for e.g. running below commands on Ubuntu 20.04 LTS OS plaform 
      ```bash
      $sudo apt update
      $sudo apt -y upgrade
      ```
    Once the process is complete, check the version of Python 3 that is installed in the system by typing:
      ```bash
      $python3 -V
      ```
    You’ll receive output in the terminal window that will let you know the version number. While this number may vary, the output will be similar to this:
      ```bash
      Python 3.8.10*
      ```
  - Install Optimized BLAS (linear algebra) library (development files) on Linux CI host, Kubetnetes Master & (Worker) Nodes
      ```bash
      $sudo apt-get install libopenblas-dev
      ```
  - On Linux CI host, Kubetnetes Master & (Worker) Nodes, to manage software packages for Python, install pip, a tool that will install and manage programming packages:
      ```bash
      $sudo apt install -y python3-pip
      ```
  - (Optionally) Setup a [Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for Python, which enable you to have an isolated space on your server for Python projects, ensuring that each of your projects can have its own set of dependencies that won’t disrupt any of your other projects. 
  - Install **Helm** on Linux CI Host using [Helm Install Documentation](https://helm.sh/docs/intro/install)
  - Install **METRICS** Server byY BITNAMI HELM CHARTS
  
 ### DASK Environment Preperation
  - Install **DASK Distributed & Kubernetes** Package with Python Dependencies on Linux CI host
      ```bash
      $sudo pip install dask distributed --upgrade # A distributed task scheduler for Dask
      $sudo pip install dask-kubernetes --upgrade  # DASK Kubernetes Module 
      ```
    For other installation options refer [DASK Distributed Documentation](http://distributed.dask.org/en/stable/install.html) & [DASK Kubernetes Documentation](https://kubernetes.dask.org/en/latest/installing.html) 
  - Install Qiskit SDK package(s) on Linux CI host **preferably in Python Virtual Environment** 
      ```bash
      $sudo pip install qiskit
      ```
    Optionally install Application Modules & Visualization functionality (like Plots , Jupyter Notebooks), as per requirement of program, e.g **Qiskit Nature ( for VQE )**
      ```bash
      $sudo pip install qiskit[nature]
      $sudo pip install qiskit[visualization]
      ```
  - Dask maintains a Helm chart repository containing various charts for the Dask community https://helm.dask.org/ . Add this to your known channels and update your local charts:
      ```bash
      helm repo add dask https://helm.dask.org/
      helm repo update
      ```
  - Check Kubernetes Cluster Status:
      ```bash
      ubuntu@ip-172-31-93-214:~$ kubectl get nodes
      NAME                            STATUS   ROLES                  AGE   VERSION
      ip-172-20-33-106.ec2.internal   Ready    node                   24d   v1.22.2
      ip-172-20-51-193.ec2.internal   Ready    node                   24d   v1.22.2
      ip-172-20-61-190.ec2.internal   Ready    control-plane,master   24d   v1.22.2
      ```  
     
  - Once your Kubernetes cluster is ready, deploy **Single-user** dask deployment using the Dask Helm chart, which has one notebook server and one Dask Cluster:
      ```bash
      helm install my-dask dask/dask # Replace helm release name as per your environment
      ```
    This deploys a dask-scheduler, several (=3) dask-worker processes, and also an optional Jupyter server.
  - **Verify Deployment** : It might take a minute to deploy, one or more pods will be visible in either a state like Init or Running. Check deplyment its status with kubectl:
      ```bash
      ubuntu@ip-172-31-93-214:~$ kubectl get pods |grep dask
      my-dask-jupyter-54ddbfdd9d-psrlh             1/1     Running   0          2m23s
      my-dask-scheduler-7f4f94bb7d-vd5sb           1/1     Running   0          2m23s
      my-dask-worker-6877d8f79f-2kxkk              1/1     Running   0          2m23s
      my-dask-worker-6877d8f79f-94bhs              1/1     Running   0          2m23s
      my-dask-worker-6877d8f79f-rj7mp              1/1     Running   0          2m23s
      my-dask-worker-6877d8f79f-zl54c              1/1     Running   0          116s


      ubuntu@ip-172-31-93-214:~$ kubectl get services|grep dask
      dask-ubuntu-1e61eab2-a      ClusterIP   100.68.40.175    <none>        8786/TCP,8787/TCP   28d
      dask-ubuntu-86f19230-5      ClusterIP   100.68.54.85     <none>        8786/TCP,8787/TCP   45h
      dask-ubuntu-b71bdf3d-9      ClusterIP   100.69.173.29    <none>        8786/TCP,8787/TCP   45h
      dask-ubuntu-dbe05783-a      ClusterIP   100.71.121.134   <none>        8786/TCP,8787/TCP   45h
      my-dask-jupyter             ClusterIP   100.70.215.20    <none>        80/TCP              3m17s
      my-dask-scheduler           ClusterIP   100.71.64.151    <none>        8786/TCP,80/TCP     3m17s
      
      ubuntu@ip-172-31-93-214:~$ kubectl get deployments|grep dask
      my-dask-jupyter             1/1     1            1           12m
      my-dask-scheduler           1/1     1            1           12m
      my-dask-worker              3/3     3            3           12m
      ```
  - (Optional) Kubernetes cluster has default **serviceType** already set as **ClusterIP**

    If Kubernetes cluster on an in house **server/minikube** change serviceType to **NodePort**
      ```bash 
      kubectl delete services my-dask-scheduler # Delete the service entry for dask scheduler
      ubuntu@ip-172-31-93-214:~$ kubectl expose deployment my-dask-scheduler --type=NodePort  --name=my-dask-scheduler
      service/my-dask-scheduler exposed
      ```
    If Kubernetes Environment is on **Cloud platform**, change serviceType  **LoadBalancer**
      ```bash
      kubectl delete services my-dask-scheduler # Delete the service entry for dask scheduler
      ubuntu@ip-172-31-93-214:~$ kubectl expose deployment my-dask-scheduler --type=LoadBalancer  --name=my-dask-scheduler
      ###Wait for few minutes (depending on response from backend Cloud platform) and again check the kubernetes services status
      ubuntu@ip-172-31-93-214:~$ kubectl get services|grep dask
      dask-ubuntu-1e61eab2-a      ClusterIP      100.68.40.175    <none>                                                                    8786/TCP,8787/TCP               28d
      dask-ubuntu-86f19230-5      ClusterIP      100.68.54.85     <none>                                                                    8786/TCP,8787/TCP               46h
      dask-ubuntu-b71bdf3d-9      ClusterIP      100.69.173.29    <none>                                                                    8786/TCP,8787/TCP               45h
      dask-ubuntu-dbe05783-a      ClusterIP      100.71.121.134   <none>                                                                    8786/TCP,8787/TCP               45h
      my-dask-jupyter             ClusterIP      100.70.215.20    <none>                                                                    80/TCP                          21m
      my-dask-scheduler           LoadBalancer   100.66.41.63     xxx4e66d7fxxx47858xx1c1cd4c13c19-1533367445.us-east-1.elb.amazonaws.com   8786:31305/TCP,8787:31970/TCP   4m19s

      ```
    When we ran kubectl get services, some externally IP is visible (like **xxx4e66d7fxxx47858xx1c1cd4c13c19-1533367445.us-east-1.elb.amazonaws.com**) against dask scheduler services, using any web browser (http://xxx4e66d7fxxx47858xx1c1cd4c13c19-1533367445.us-east-1.elb.amazonaws.com:8787/workers) the Dask diagnostic dashboard can be accessed. 
      
  - **Configure DASK Environment as Executor for Qiskit AER Simulator** : By default, the Helm deployment launches three workers using one core each and a standard conda environment. To act as a **executor** for Qiskit AER simulator, need to create a small yaml file that customizes environment by:
    - Setting variables on worker nodes: **OMP_NUM_THREAD, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS**  
      **Note:** These environment variable controls the number of threads that many libraries, including the BLAS library powering numpy.dot, use in their computations, like matrix multiply.The conflict here is that two parallel libraries that are calling each other, BLAS, and dask.distributed. Each library is designed to use as many threads as there are logical cores available in the system. 

      For example if compute platform had eight cores then dask.distributed might run function **f** eight times at once on different threads. The **numpy.dot** function call within **f** would use eight threads per call, resulting in 64 threads running at once.This is actually fine, but it will be slower than scenario if where just eight threads are used at a time, either by limiting dask.distributed or by limiting BLAS.


    - Installing **qiskit** package on worker pods.

      ```bash
      # config.yaml

      worker:
        env:
          - name: EXTRA_PIP_PACKAGES
            value: qiskit
          - name: OMP_NUM_THREAD
            value: "1"
          - name: MKL_NUM_THREADS
            value: "1"
          - name: OPENBLAS_NUM_THREADS
            value: "1"

      # Need to keep the same packages on the worker and jupyter environments
      jupyter:
        env:
          - name: EXTRA_PIP_PACKAGES
            value: qiskit
          - name: OMP_NUM_THREAD
            value: "1"
          - name: MKL_NUM_THREADS
            value: "1"
          - name: OPENBLAS_NUM_THREADS
            value: "1"
      ```
  - **Update deployment** : If this config file has the configuration for the number and size of workers then it overrides existing configuration and installs the conda and pip packages on the worker and Jupyter containers. In general, it is needed that these two container environments match.\

    Update deployment to use this configuration file (config.yaml):
      ```bash
      helm upgrade my-dask dask/dask -f config.yaml
      ```
    This will update those containers that need to be updated. It may take a minute or so.As a reminder, the names of deployments can be listed using **helm list**.
  ### Testing the environment 
  - **Running a simple DASK (non QISKIT) script**(Considering K8s on Cloud Platform)  

      ```bash
      #Python Script for Dask Array Mean Calculation

      from dask.distributed import Client

      # Connect Dask to the cluster
      client = Client("tcp://xxx4e66d7fxxx47858xx1c1cd4c13c19-1533367445.us-east-1.elb.amazonaws.com:8786") # External IP captured in kubectl get services output


      import time
      time.sleep(60)
      # Example usage
      import dask.array as da


      # Create a large array and calculate the mean
      array = da.ones((1000, 1000, 1000))
      print("Array Mean", array.mean().compute())# Should print 1.0
      ```
      ```bash
      ubuntu@ip-172-31-93-214:~$ python3 dask_array_mean.py
      /home/ubuntu/.local/lib/python3.8/site-packages/distributed/client.py:1131: VersionMismatchWarning: Mismatched versions found

      +---------+----------------+----------------+----------------+
      | Package | client         | scheduler      | workers        |
      +---------+----------------+----------------+----------------+
      | blosc   | None           | 1.10.2         | 1.10.2         |
      | lz4     | None           | 3.1.3          | 3.1.3          |
      | numpy   | 1.21.2         | 1.21.1         | 1.21.1         |
      | pandas  | 1.3.3          | 1.3.0          | 1.3.0          |
      | python  | 3.8.10.final.0 | 3.8.12.final.0 | 3.8.12.final.0 |
      | toolz   | 0.11.1         | 0.11.2         | 0.11.2         |
      +---------+----------------+----------------+----------------+
        warnings.warn(version_module.VersionMismatchWarning(msg[0]["warning"]))
      Array Mean 1.0
      ```
  - **Running a VQE script generating Qiskit Circuit List**
    - **Case 1 :** Running script without parallel execution environment
    
      ```bash
      # VQE Script generating Circuit list
      import numpy as np
      import multiprocessing
      from time import time
      import timeit
      from qiskit_nature.circuit.library import HartreeFock, UCCSD
      from qiskit_nature.converters.second_quantization import QubitConverter
      from qiskit_nature.drivers import UnitsType, Molecule
      from qiskit_nature.drivers.second_quantization.pyscfd import PySCFDriver
      from qiskit_nature.mappers.second_quantization import JordanWignerMapper, ParityMapper
      from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
      from qiskit_nature.algorithms import GroundStateEigensolver
      import warnings
      warnings.filterwarnings("ignore")

      mol_string='H .0 .0 .0; Li .0 .0 2.5'

      threads = 12
      max_evals_grouped = 1024

      driver = PySCFDriver(atom=mol_string, unit=UnitsType.ANGSTROM, basis='sto3g')
      es_problem = ElectronicStructureProblem(driver)
      qubit_converter = QubitConverter(JordanWignerMapper())

      from qiskit.algorithms.optimizers import SLSQP
      optimizer = SLSQP(maxiter=5000)

      from qiskit.providers.aer import AerSimulator
      from qiskit.utils import QuantumInstance


      import logging
      logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                          level=logging.DEBUG,
                          datefmt='%Y-%m-%d %H:%M:%S')

      from qiskit_nature.algorithms import VQEUCCFactory

      simulator = AerSimulator()
      quantum_instance = QuantumInstance(backend=simulator)

      start = timeit.default_timer()


      vqe_solver = VQEUCCFactory(quantum_instance,
                                 optimizer=optimizer,
                                 include_custom=True)

      optimizer.set_max_evals_grouped(max_evals_grouped)

      calc = GroundStateEigensolver(qubit_converter, vqe_solver)
      res = calc.solve(es_problem)

      print(res)

      stop = timeit.default_timer()

      print('Execution Time without Parallelism: ', stop - start)

      ```
      Run the script and wait for 10 -20 mins for output
      
      ```bash
      === GROUND STATE ENERGY ===

      * Electronic ground state energy (Hartree): -8.458691725491
        - computed part:      -8.458691725491
      ~ Nuclear repulsion energy (Hartree): 0.635012653104
      > Total ground state energy (Hartree): -7.823679072387

      === MEASURED OBSERVABLES ===

        0:  # Particles: 4.000 S: 0.000 S^2: 0.000 M: 0.000

      === DIPOLE MOMENTS ===

      ~ Nuclear dipole moment (a.u.): [0.0  0.0  14.17294593]

        0:
        * Electronic dipole moment (a.u.): [0.00000183  0.00000491  12.73423798]
          - computed part:      [0.00000183  0.00000491  12.73423798]
        > Dipole moment (a.u.): [-0.00000183  -0.00000491  1.43870795]  Total: 1.43870795
                       (debye): [-0.00000466  -0.00001247  3.6568305]  Total: 3.6568305

      **Execution Time without Parallelism:  757.9253145660005**
      ```
    - **Case 2 :** Running script with ThreadsPool parallel execution environment
      ```bash
      import numpy as np
      import multiprocessing
      from time import time
      import timeit
      from qiskit_nature.circuit.library import HartreeFock, UCCSD
      from qiskit_nature.converters.second_quantization import QubitConverter
      from qiskit_nature.drivers import UnitsType, Molecule
      from qiskit_nature.drivers.second_quantization.pyscfd import PySCFDriver
      from qiskit_nature.mappers.second_quantization import JordanWignerMapper, ParityMapper
      from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
      from qiskit_nature.algorithms import GroundStateEigensolver
      import warnings
      warnings.filterwarnings("ignore")

      mol_string='H .0 .0 .0; Li .0 .0 2.5'

      threads = 12
      max_evals_grouped = 1024

      driver = PySCFDriver(atom=mol_string, unit=UnitsType.ANGSTROM, basis='sto3g')
      es_problem = ElectronicStructureProblem(driver)
      qubit_converter = QubitConverter(JordanWignerMapper())

      from qiskit.algorithms.optimizers import SLSQP
      optimizer = SLSQP(maxiter=5000)

      from qiskit.providers.aer import AerSimulator
      from qiskit.utils import QuantumInstance


      import logging
      logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                          level=logging.DEBUG,
                          datefmt='%Y-%m-%d %H:%M:%S')

      from qiskit_nature.algorithms import VQEUCCFactory

      **from concurrent.futures import ThreadPoolExecutor
      exc = ThreadPoolExecutor(max_workers=2)

      simulator = AerSimulator(executor=exc)**
      quantum_instance = QuantumInstance(backend=simulator)

      start = timeit.default_timer()
      simulator = AerSimulator(executor=exc)
      quantum_instance = QuantumInstance(backend=simulator)
      start = timeit.default_timer()
      vqe_solver = VQEUCCFactory(quantum_instance,
                                 optimizer=optimizer,
                                 include_custom=True)

      optimizer.set_max_evals_grouped(max_evals_grouped)
      calc = GroundStateEigensolver(qubit_converter, vqe_solver)
      res = calc.solve(es_problem)
      print(res)
      stop = timeit.default_timer()
      print('Execution Time with ThreadPool Parallelism across 2 workers: ', stop - start)
      ```
      ```bash
      
      ```
    - **Case 3 :** Running script with DASK K8s parallel execution environment (Considering K8s on Cloud Platform)    
      ```bash
      import numpy as np
      import multiprocessing
      from time import time
      import timeit
      from qiskit_nature.circuit.library import HartreeFock, UCCSD
      from qiskit_nature.converters.second_quantization import QubitConverter
      from qiskit_nature.drivers import UnitsType, Molecule
      from qiskit_nature.drivers.second_quantization.pyscfd import PySCFDriver
      from qiskit_nature.mappers.second_quantization import JordanWignerMapper, ParityMapper
      from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
      from qiskit_nature.algorithms import GroundStateEigensolver
      from qiskit.algorithms.optimizers import SLSQP
      from qiskit.providers.aer import AerSimulator
      from qiskit.utils import QuantumInstance
      from qiskit_nature.algorithms import VQEUCCFactory
      from distributed import LocalCluster
      from dask.distributed import Client
      import logging

      def q_exec():
          import warnings
          warnings.filterwarnings("ignore")

          mol_string='H .0 .0 .0; Li .0 .0 2.5'

          threads = 12
          max_evals_grouped = 1024

          driver = PySCFDriver(atom=mol_string, unit=UnitsType.ANGSTROM, basis='sto3g')
          es_problem = ElectronicStructureProblem(driver)
          qubit_converter = QubitConverter(JordanWignerMapper())


          optimizer = SLSQP(maxiter=5000)


          logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                              level=logging.DEBUG,
                              datefmt='%Y-%m-%d %H:%M:%S')

**          from dask.distributed import Client
          exc =  Client(address="tcp://xxx4e66d7fxxx47858xx1c1cd4c13c19-1533367445.us-east-1.elb.amazonaws.com:8786")# External IP captured in kubectl get services output
          simulator = AerSimulator()
          simulator.set_options(executor=exc)**
          simulator.set_options(max_job_size=1)

          quantum_instance = QuantumInstance(backend=simulator)
          start = timeit.default_timer()

          vqe_solver = VQEUCCFactory(quantum_instance,
                                     optimizer=optimizer,
                                     include_custom=True)

          optimizer.set_max_evals_grouped(max_evals_grouped)

          calc = GroundStateEigensolver(qubit_converter, vqe_solver)
          res =  calc.solve(es_problem)
          print(res)
          stop = timeit.default_timer()
          print('Execution Time with three  Dask Cluster worker(s): ', stop - start)

      if __name__ == '__main__':
          q_exec()

      ```
      ```bash
      
      ```
