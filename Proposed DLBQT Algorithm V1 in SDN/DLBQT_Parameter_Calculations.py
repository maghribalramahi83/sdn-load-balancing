Python Code

"""
Original algorithm design:
Dr. Maghrib A. M. Alrammahi
Mohammed Fadhil Mohammed 

methodological formulation
presented in this file were originally developed by Dr. Maghrib A. M. Alrammahi and Mohammed Fadhil Mohammed.
This implementation documents the proposed model for research transparency
and reproducibility.

Unauthorized removal of this attribution is not permitted.
""" 


import os
import sys
import time
import requests
import random
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Configuration
url = "http://10.0.0.100/upload"
output_dir = "generated_files"

# Input validation
if len(sys.argv) < 3:
    print("❌ Usage: python3 script.py <num_requests> <output_filename>")
    sys.exit(1)

try:
    num_requests = int(sys.argv[1])
    output_filename = sys.argv[2]
except ValueError:
    print("❌ Error: num_requests must be an integer!")
    sys.exit(1)

# Prepare files
files_to_send = [os.path.join(output_dir, f) for f in os.listdir(output_dir) 
                if os.path.isfile(os.path.join(output_dir, f))]
if not files_to_send:
    print("🚨 No files found in generated_files/! Exiting.")
    sys.exit(1)

# Thread safety
lock = Lock()

# Metrics tracking
successful_requests = 0
failed_requests = 0
response_times = []
waiting_times = []
service_times = []
total_data_sent = 0
total_data_received = 0

# Open output file
output_file = open(output_filename, "w")
output_file.write("==== Request Details ====\n\n")

def send_file(file_path):
    global failed_requests, successful_requests, total_data_sent
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    with lock:
        output_file.write(f"📤 Uploading: {file_name} ({file_size} bytes)\n")
        print(f"📤 Uploading: {file_name} ({file_size} bytes)")
        output_file.flush()
    
    request_start = time.time()  # Start timing the request
    
    for attempt in range(2):
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                start_time = time.time()
                
                response = requests.post(
                    url,
                    files={'file': (file_name, file_content)},
                    timeout=10
                )
            
            if response.ok:
                elapsed = time.time() - start_time
                waiting_time = response.elapsed.total_seconds()
                service_time = elapsed - waiting_time
                
                with lock:
                    response_times.append(elapsed)
                    waiting_times.append(waiting_time)
                    service_times.append(service_time)
                    successful_requests += 1
                    total_data_sent += file_size
                    output_file.write(
                        f"✅ POST Success: {file_name} | "
                        f"Total Time: {elapsed:.4f}s | "
                        f"Waiting: {waiting_time:.4f}s | "
                        f"Service: {service_time:.4f}s | "
                        f"Status: {response.status_code}\n"
                    )
                    print(
                        f"✅ POST Success: {file_name} | "
                        f"Total Time: {elapsed:.4f}s | "
                        f"Waiting: {waiting_time:.4f}s | "
                        f"Service: {service_time:.4f}s | "
                        f"Status: {response.status_code}"
                    )
                    output_file.flush()
                return True
        except requests.exceptions.RequestException:
            time.sleep(2 ** attempt)
    
    with lock:
        failed_requests += 1
        output_file.write(f"❌ POST Failed: {file_name}\n")
        print(f"❌ POST Failed: {file_name}")
        output_file.flush()
    return False

def send_get_request():
    global failed_requests, successful_requests, total_data_received
    start_time = time.time()
    
    with lock:
        output_file.write("📥 Sending GET request\n")
        print("📥 Sending GET request")
        output_file.flush()
    
    try:
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start_time
        waiting_time = response.elapsed.total_seconds()
        service_time = elapsed - waiting_time
        data_received = len(response.content)
        
        with lock:
            response_times.append(elapsed)
            waiting_times.append(waiting_time)
            service_times.append(service_time)
            total_data_received += data_received
            successful_requests += 1
            output_file.write(
                f"✅ GET Success | "
                f"Total Time: {elapsed:.4f}s | "
                f"Waiting: {waiting_time:.4f}s | "
                f"Service: {service_time:.4f}s | "
                f"Data: {data_received} bytes | "
                f"Status: {response.status_code}\n"
            )
            print(
                f"✅ GET Success | "
                f"Total Time: {elapsed:.4f}s | "
                f"Waiting: {waiting_time:.4f}s | "
                f"Service: {service_time:.4f}s | "
                f"Data: {data_received} bytes | "
                f"Status: {response.status_code}"
            )
            output_file.flush()
        return True
    except requests.RequestException:
        with lock:
            failed_requests += 1
            output_file.write("❌ GET Failed\n")
            print("❌ GET Failed")
            output_file.flush()
        return False

# Record total test duration
start_test_time = time.time()

# Run load test
with ThreadPoolExecutor(max_workers=os.cpu_count() * 4) as executor:
    futures = []
    for _ in range(num_requests):
        if random.choice([True, False]):
            selected_file = random.choice(files_to_send)
            futures.append(executor.submit(send_file, selected_file))
        else:
            futures.append(executor.submit(send_get_request))
    
    for future in as_completed(futures):
        future.result()

# Calculate total execution time
total_test_time = time.time() - start_test_time
hours = int(total_test_time // 3600)
minutes = int((total_test_time % 3600) // 60)
seconds = total_test_time % 60

# Calculate other metrics
total_requests = successful_requests + failed_requests
packet_loss_rate = (failed_requests / total_requests) * 100 if total_requests else 0

avg_response_time = statistics.mean(response_times) if response_times else 0
avg_waiting_time = statistics.mean(waiting_times) if waiting_times else 0
avg_service_time = statistics.mean(service_times) if service_times else 0

total_data_transferred = total_data_sent + total_data_received
avg_throughput = total_data_transferred / (total_test_time * 1024 * 1024) if total_test_time else 0

if len(response_times) > 1:
    std_dev = statistics.stdev(response_times)
    load_balancing_degree = (std_dev / avg_response_time) * 100 if avg_response_time else 0
else:
    load_balancing_degree = 0

# Final report
with lock:
       output_file.write(f"Avg Waiting Time: {avg_waiting_time:.4f} seconds\n")
    output_file.write(f"Avg Service Time: {avg_service_time:.4f} seconds\n")
   

    output_file.write("\n\n==== Execution Time ====\n")
    output_file.write(f"🕒 Total Execution Time: {hours:02d}:{minutes:02d}:{seconds:.2f}\n")
    
   
    print(f"Avg Waiting Time: {avg_waiting_time:.4f} seconds")
    print(f"Avg Service Time: {avg_service_time:.4f} seconds")
    
    
    print("\n\n==== Execution Time ====")
    print(f"🕒 Total Execution Time: {hours:02d}:{minutes:02d}:{seconds:.2f}")

output_file.close()
print(f"\n✅ Results saved to: {output_filename}")
