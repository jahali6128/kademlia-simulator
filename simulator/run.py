import csv
import subprocess
from itertools import product

from jproperties import Properties

# rps_range = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2]
rps_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# latency_range = [10, 50, 500, 1000, 2000, 3000]
# latency_range = [50, 500, 1000, 2000, 3000]

alpha_range = [1, 2, 3, 4, 5, 10]
latency_range = [1, 5, 10, 100, 250, 500]
# timer_range = [1, 3, 5, 7, 10, 20]
timer_range = [0.5, 1, 1.5, 2, 2.5, 3]

ID_LEN = 2
NETWORK_SIZE = 100
SIM_RUNS = 50


def edit_properties_file(rps, latency=1, alpha=3, timer=0):
    p = Properties()
    with open(
        "/home/jahali6128/kademlia-simulator/simulator/config/kademlia_putget.cfg",
        "rb+",
    ) as f:
        p.load(f, "utf-8")
        p["RPS"] = str(rps)
        p["MINDELAY"] = str(latency)
        p["MAXDELAY"] = str(latency)
        p["ALPHA"] = str(alpha)
        p["OBSERVER_STEP"] = str(timer)
        f.seek(0)
        f.truncate(0)
        p.store(f, "utf-8")


def run_single_experiment_alpha(rps, alpha):
    edit_properties_file(rps=rps, alpha=alpha)
    rps_result = []
    for _ in range(SIM_RUNS):
        check_output = subprocess.run(
            "./run.sh config/kademlia_putget.cfg > kad.log && head -n 7 kad.log | grep -m 1 'Key'",
            shell=True,
            check=False,
            capture_output=True,
            text=True,
        )
        # print(check_output.stdout.split()[6])
        time_coll = int(check_output.stdout.split()[6])
        rps_result.append(time_coll)

    get_average = sum(rps_result) / len(rps_result)
    # all_results.append(get_average)
    print(f"Finished Experiment RPS: {rps} with alpha {alpha} on N {NETWORK_SIZE}")
    result = {"rps": rps, "alpha": alpha, "result": get_average}
    return result


def write_to_csv_alpha(results, alpha):
    with open(
        f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{NETWORK_SIZE}/results-{NETWORK_SIZE}-alpha.csv",
        "w",
        newline="",
    ) as csvfile:
        fieldnames = ["rps", "alpha", "result"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def run_single_experiment_latency(rps, latency):
    edit_properties_file(rps=rps, latency=latency)
    rps_result = []
    for _ in range(SIM_RUNS):
        check_output = subprocess.run(
            "./run.sh config/kademlia_putget.cfg > kad.log && head -n 7 kad.log | grep -m 1 'Key'",
            shell=True,
            check=False,
            capture_output=True,
            text=True,
        )
        # print(check_output.stdout.split()[6])
        time_coll = int(check_output.stdout.split()[6])
        rps_result.append(time_coll)

    get_average = sum(rps_result) / len(rps_result)
    # all_results.append(get_average)
    print(f"Finished Experiment RPS: {rps} with latency {latency} on N {NETWORK_SIZE}")
    result = {"rps": rps, "latency": latency, "result": get_average}
    return result
    # with open(f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{NETWORK_SIZE}/LAT-{latency}/results.csv") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(all_results)


def run_single_experiment_cache(rps, timer):
    # Need to convert to milliseconds
    edit_properties_file(rps=rps, timer=timer * 1000, latency=100)
    rps_result = []
    for _ in range(SIM_RUNS):
        check_output = subprocess.run(
            "./run.sh config/kademlia_putget.cfg > kad.log && head -n 7 kad.log | grep -m 1 'Key'",
            shell=True,
            check=False,
            capture_output=True,
            text=True,
        )
        # print(check_output.stdout.split()[6])
        time_coll = int(check_output.stdout.split()[6])
        rps_result.append(time_coll)

    get_average = sum(rps_result) / len(rps_result)
    # all_results.append(get_average)
    print(f"Finished Experiment RPS: {rps} with T {timer} on N {NETWORK_SIZE}")
    result = {
        "rps": rps,
        "timer": timer,
        "network_size": NETWORK_SIZE,
        "result": get_average,
    }
    return result


def write_to_csv_cache(results):
    with open(
        f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{NETWORK_SIZE}/results-{NETWORK_SIZE}-cache.csv",
        "w",
        newline="",
    ) as csvfile:
        fieldnames = ["rps", "timer", "network_size", "result"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def run_all_rps_experiments_cache():
    all_results = []
    comb = list(product(rps_range, timer_range))
    for c in comb:
        result = run_single_experiment_cache(c[0], c[1])
        all_results.append(result)

    write_to_csv_cache(all_results)
    # print("all_results:", all_results)
    print("Simulation Finished!")


# Once all the data has been collected, write to a CSV file
def write_to_csv_latency(results):
    with open(
        f"/home/jahali6128/kademlia-simulator/simulator/results/ID-{ID_LEN}/N-{NETWORK_SIZE}/results-{NETWORK_SIZE}.csv",
        "w",
        newline="",
    ) as csvfile:
        fieldnames = ["rps", "latency", "result"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def run_all_rps_experiments_latency():
    all_results = []
    comb = list(product(latency_range, rps_range))
    for c in comb:
        result = run_single_experiment_latency(c[1], c[0])
        all_results.append(result)

    write_to_csv_latency(all_results)
    # print("all_results:", all_results)
    print("Simulation Finished!")


def run_all_rps_experiments_alpha():
    all_results = []
    comb = list(product(alpha_range, rps_range))
    alpha = 0
    for c in comb:
        alpha = c[1]
        result = run_single_experiment_alpha(c[1], c[0])
        all_results.append(result)

    write_to_csv_alpha(all_results, alpha=alpha)
    # print("all_results:", all_results)
    print("Simulation Finished!")


def rps_network_id_requests(rps):
    edit_properties_file(rps=rps)
    rps_result = []
    for _ in range(5):
        check_output = subprocess.run(
            "./run.sh config/kademlia_putget.cfg > kad.log && head -n 7 kad.log | grep -m 1 'Collision'",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        id_requests = float(check_output.stdout.split()[4])
        rps_result.append(id_requests)

    get_average = sum(rps_result) / len(rps_result)
    # all_results.append(get_average)
    print(f"Finished Experiment RPS: {rps} on N {NETWORK_SIZE}")
    result = {"rps": rps, "network_size": NETWORK_SIZE, "result": get_average}
    return result


if __name__ == "__main__":
    # print(run_single_experiment_latency(rps=20, latency=1))
    test_timer_range = [0.5, 1, 1.5, 2, 2.5, 3]
    # for i in test_timer_range:
    print(run_single_experiment_cache(rps=80, timer=1.5))
    # run_all_rps_experiments_cache()
    # run_all_rps_experiments_latency()
    # run_all_rps_experiments_alpha()

    # print(rps_network_id_requests(rps=10))
