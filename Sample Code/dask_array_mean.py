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
