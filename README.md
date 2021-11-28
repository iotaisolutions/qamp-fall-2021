# qamp-fall-2021
## Project 39: Tutorial to use K8S Cluster (Qiskit Advocate Mentorship Program: Fall 2021)##
Simulation of quantum applications like quantum chemistry, materials science, quantum biology, generates quantum systems which are much larger than computational NISQ devices, this gap can be handled by parallelizing the quantum simulation. \
Qiskit Aer is a Noisy quantum circuit simulator backend and runs simulation jobs on a single-worker Python multiprocessing ThreadPool executor so that all parallelization is handled by low-level OpenMP and CUDA code (For Multi CPU / Core & GPU environment). \
Variational Quantum Eigensolver (VQE and the other compute intensive variational algorithms) already support generating circuits together for parallel gradient computation. In order to customize job-level parallel execution of multiple circuits, a custom multiprocessing executor can be specified, which controls the splitting of circuits using the executor and max_job_size backend options of Qiskit AerSimulator. \
In order  to simulate parallel execution  on premise as well as cloud  environment, dedicated compute resources might be required, but available with constraints, both on scalability and manageability.\
![image](https://user-images.githubusercontent.com/68344826/143679187-250c4082-feca-4482-8aba-c753cbbceece.png)
