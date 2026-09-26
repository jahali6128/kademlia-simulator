import csv
from itertools import product
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

xPoints = [1, 2, 3, 4, 5, 10, 20]

ID_LEN = 2
NETWORK_SIZE = 100
LATENCY = [1, 5, 10, 100, 250, 500]
ALPHA = [1, 2, 3, 4, 5, 10]

DIR = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{NETWORK_SIZE}/results-{NETWORK_SIZE}.csv"
ALPHA_DIR = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{NETWORK_SIZE}/results-{NETWORK_SIZE}-alpha.csv"


def plot_latency(dir=DIR):
    for l in LATENCY:
        yPoints = []
        with open(dir, "r") as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if int(row["latency"]) == l:
                    yPoints.append(float(row["result"]) / 1000)
        plt.plot(xPoints, yPoints, label=f"lat={l}ms", linestyle="dashed")
    # plt.show()


def plot_all_latency():
    NETWORK_RANGE = [10, 50, 100, 500, 1000]
    for n in NETWORK_RANGE:
        LATENCY_DIR_LOCAL = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{n}/results-{n}.csv"
        plot_latency(dir=LATENCY_DIR_LOCAL)

        plt.title(f"Latency vs. Collision Time on Network Size: {n}")
        plt.xlabel("RPS")
        plt.ylabel("Time to (First) Collision (s)")
        plt.legend()
        plt.savefig(
            f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/plots/latency-coll-n-{n}.png"
        )
        plt.close()


def plot_alpha(alpha_dir=ALPHA_DIR):
    for a in ALPHA:
        yPoints = []
        with open(alpha_dir, "r") as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if int(row["alpha"]) == a:
                    yPoints.append(float(row["result"]) / 1000)
        plt.plot(xPoints, yPoints, label=f"alpha={a}", linestyle="dashed")


def plot_all_alpha():
    NETWORK_RANGE = [10, 50, 100, 500, 1000]
    for n in NETWORK_RANGE:
        ALPHA_DIR_LOCAL = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{n}/results-{n}-alpha.csv"
        plot_alpha(alpha_dir=ALPHA_DIR_LOCAL)

        plt.title(f"Alpha vs. Collision Time on Network Size: {n}")
        plt.xlabel("RPS")
        plt.ylabel("Time to (First) Collision (s)")
        plt.legend()
        plt.savefig(
            f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/plots/alpha-coll-n-{n}.png"
        )
        plt.close()


def plot_network_coll():
    NETWORK_RANGE = [10, 50, 100, 500, 1000]
    rps_list = [1, 2, 3, 4, 5, 10, 20]
    latencies = [1, 5, 10, 100, 250, 500]

    comb = product(rps_list, latencies)

    for c in comb:
        all_results = []
        for n in NETWORK_RANGE:
            LATENCY_DIR_LOCAL = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{n}/results-{n}.csv"
            with open(LATENCY_DIR_LOCAL, "r") as csv_file:
                csv_data = csv.DictReader(csv_file)
                # Only get the first entry from each file
                # all_results.append(float(next(iter(data))["result"]) / 1000)
                data = list(csv_data)

                rps = c[0]
                lat = c[1]
                for d in data:
                    if int(d["rps"]) == rps and int(d["latency"]) == lat:
                        all_results.append(float(d["result"]) / 1000)

        plt.title(f"rps-{c[0]}, latency-{c[1]}")
        plt.xlabel("Network Size")
        plt.ylabel("TTC")
        plt.plot(NETWORK_RANGE, all_results)

        SAVE_DIRECTORY = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/plots/network_size_vs_ttc/rps-{c[0]}-latency-{c[1]}"
        plt.savefig(SAVE_DIRECTORY)
        plt.close()


def plot_latency_ttc():
    # N-1000, RPS-20
    n = 1000
    rps = [1, 2, 3, 4, 5, 10, 20]
    latencies = [1, 5, 10, 100, 250, 500]

    LATENCY_DIR_LOCAL = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{n}/results-{n}.csv"
    with open(LATENCY_DIR_LOCAL, "r") as csv_file:
        data = list(csv.DictReader(csv_file))

    for r in rps:
        results = []
        for l in latencies:
            for row in data:
                if (int(row["latency"]) == l) and (int(row["rps"]) == r):
                    print("l:", l, "r:", r)
                    results.append(float(row["result"]) / 1000)
                    # print(row["result"])
        # print("results:", results)

        plt.title(f"Network-{n}, RPS-{r}")
        plt.plot(latencies, results)
        plt.xlabel("latencies")
        plt.ylabel("TTC")

        SAVE_DIRECTORY = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/plots/latency_vs_ttc/network-{n}-rps-{r}"
        plt.savefig(SAVE_DIRECTORY)
        plt.close()


def plot_cache():
    n = 100
    rps_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    timer_range = [1, 5, 7, 10, 20]

    CACHE_DIR_LOCAL = f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{n}/results-{n}-cache.csv"
    with open(CACHE_DIR_LOCAL, "r") as csv_file:
        data = list(csv.DictReader(csv_file))

    comb = product(timer_range, rps_range)
    # print(list(comb)) 
    # # Then add the results
    xPoints = rps_range
    yPoints = []
    for c in comb:
        rps = c[1]
        timer = c[0]
        
        for d in data:
            if (rps == int(d["rps"])) and (timer == int(d["timer"])):
                print("rps:", d["rps"], "timer:", d["timer"], "result:", d["result"])
                yPoints.append(float(d["result"])/1000)
        
        if rps == 100:
            print("xPoints:", xPoints)
            print("yPoints:", yPoints)
            plt.plot(xPoints, yPoints, label=f"timer-{timer}")
            yPoints = []
    
    plt.title(f"Cache Timer vs TTC, N-{NETWORK_SIZE}") 
    plt.xlabel("RPS")
    plt.ylabel("TTC (s)") 
    plt.legend()
    plt.show()
        # print(yPoints)

        
    # print("xPoints: ", xPoints, "yPoints:", yPoints)
    # plt.plot(xPoints, yPoints)
    # plt.xlabel("RPS")
    # plt.ylabel("TTC")
    # plt.close()
   
    # plt.legend() 
    # plt.show()
        
    # print("results:", results)    
    

if __name__ == "__main__":
    # plot_network_coll()
    # plot_latency_ttc()
    plot_cache()
    # plot_all_latency()
    # plot_all_alpha()
    # plot_latency()
    # plot_alpha()

    # plt.title(f"Alpha vs. Collision Time on Network Size: {NETWORK_SIZE}")
    # plt.xlabel("RPS")
    # plt.ylabel("Time to (First) Collision (s)")
    # plt.legend()
    # plt.show()
