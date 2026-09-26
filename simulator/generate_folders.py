import glob
import os
from itertools import product

PARENT_DIR = "/home/jahali6128/kademlia-simulator/simulator/results"

# DHT Params
latency = [10, 50, 500, 1000, 2000, 3000]
id_length = [1, 2, 3]
rps = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2]
network_size = [10, 100, 1000, 10000]


# file structure: ID -> network-size -> finality -> rps
def generate():
    comb = list(product(id_length, network_size, latency))
    for c in comb:
        os.makedirs(f"{PARENT_DIR}/ID-{c[0]}/N-{c[1]}/LAT-{c[2]}")


def remove_all():
    comb = list(product(id_length, network_size, latency))
    for c in comb:
        files = glob.glob(f"{PARENT_DIR}/ID-{c[0]}/N-{c[1]}/LAT-{c[2]}/*")
        for f in files:
            os.remove(f)


if __name__ == "__main__":
    generate()
    # remove_all()
