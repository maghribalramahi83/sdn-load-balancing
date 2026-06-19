"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the ML-QTLB research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
"""

import time
import math
import random
import requests

url = "http://10.0.1.1/"
files = ['1.txt', '10.txt', '25.txt', '50.txt', '75.txt']
request_count = 1000

servers = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
server_workloads = {server: 0 for server in servers}

successful_requests = 0
failed_requests = 0

total_response_time = 0.0
total_waiting_time = 0.0
total_service_time = 0.0

for i in range(request_count):
    f = random.choice(files)
    url1 = url + f

    server = min(server_workloads, key=server_workloads.get)
    server_workloads[server] += 1

    try:
        start_time = time.time()
        r = requests.get(url1, timeout=200)
        r.raise_for_status()
        end_time = time.time()

        response_time = end_time - start_time
        waiting_time = time.time() - start_time - r.elapsed.total_seconds()
        service_time = response_time - waiting_time

        total_response_time += response_time
        total_waiting_time += waiting_time
        total_service_time += service_time
        successful_requests += 1

        print(
            f"Request {i+1:>4}: file={f:>6} | "
            f"RT={response_time:>8.4f} s | "
            f"WT={waiting_time:>8.4f} s | "
            f"ST={service_time:>8.4f} s"
        )

    except requests.exceptions.RequestException as e:
        print(f"Request {i+1:>4}: file={f:>6} | Error: {e}")
        failed_requests += 1

completed = successful_requests if successful_requests > 0 else 1

average_response_time = total_response_time / completed
average_waiting_time = total_waiting_time / completed
average_service_time = total_service_time / completed

mean_workload = sum(server_workloads.values()) / len(server_workloads)
variance = sum((workload - mean_workload) ** 2 for workload in server_workloads.values()) / len(server_workloads)
std_deviation = math.sqrt(variance)
degree_of_load_balancing = 1 - (std_deviation / mean_workload) if mean_workload > 0 else 0

print("\n========== Final Results ==========")
print(f"Successful requests: {successful_requests}")
print(f"Failed requests: {failed_requests}")
print(f"Average Response Time (RT): {average_response_time:.4f} seconds")
print(f"Average Waiting Time (WT): {average_waiting_time:.4f} seconds")
print(f"Average Service Time (ST): {average_service_time:.4f} seconds")
print(f"Degree of Load Balancing (LB): {degree_of_load_balancing:.4f}")