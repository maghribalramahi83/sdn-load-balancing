"""
Original algorithm design:
Dr. Maghrib A. M. Alrammahi
Mohammed Fadhil Mohammed 

decision logic, and methodological formulation
presented in this file were originally developed by Dr. Maghrib A. M. Alrammahi and Mohammed Fadhil Mohammed.
This implementation documents the proposed model for research transparency
and reproducibility.

Unauthorized removal of this attribution is not permitted.
""" 


from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import psutil
import argparse
import json
import threading

UPLOAD_DIR = "uploads"
RESOURCE_FILE = "resources.json"

lock = threading.Lock()

def initialize_resources():
    """Initialize or load system resources."""
    if os.path.exists(RESOURCE_FILE):
        with open(RESOURCE_FILE, "r") as f:
            data = json.load(f)
            return data["total_cpu"], data["total_ram_gb"], data["remaining_cpu"], data["remaining_ram_gb"]
    
    total_cpu = psutil.cpu_count(logical=True)
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    remaining_cpu = total_cpu
    remaining_ram_gb = total_ram_gb
    
    save_resources(total_cpu, total_ram_gb, remaining_cpu, remaining_ram_gb)
    return total_cpu, total_ram_gb, remaining_cpu, remaining_ram_gb


def save_resources(total_cpu, total_ram_gb, remaining_cpu, remaining_ram_gb):
    """Save current resource state to a file."""
    with open(RESOURCE_FILE, "w") as f:
        json.dump({
            "total_cpu": total_cpu,
            "total_ram_gb": total_ram_gb,
            "remaining_cpu": remaining_cpu,
            "remaining_ram_gb": remaining_ram_gb
        }, f)


def allocate_resources(cpu_percent, ram_percent):
    """Allocate resources and update remaining quantities."""
    global remaining_cpu, remaining_ram_gb
    
    with lock:
        total_cpu, total_ram_gb, remaining_cpu, remaining_ram_gb = initialize_resources()
        
        allocated_cpu = int((cpu_percent / 100) * remaining_cpu)
        allocated_ram = (ram_percent / 100) * remaining_ram_gb
        
        if allocated_cpu > remaining_cpu or allocated_ram > remaining_ram_gb:
            raise ValueError(f"Not enough resources! CPU: {allocated_cpu}/{remaining_cpu}, RAM: {allocated_ram:.2f}/{remaining_ram_gb:.2f}GB")
        
        remaining_cpu -= allocated_cpu
        remaining_ram_gb -= allocated_ram
        save_resources(total_cpu, total_ram_gb, remaining_cpu, remaining_ram_gb)
        
        return allocated_cpu, allocated_ram


class NodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        file_name = os.path.basename(self.path.lstrip("/"))
        file_path = os.path.join(UPLOAD_DIR, file_name)

        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return

        with open(file_path, "rb") as f:
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
            self.end_headers()
            self.wfile.write(f.read())

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length <= 0:
            self.send_error(400, "Empty request")
            return

        filename = "uploaded_file.bin"
        if 'Content-Disposition' in self.headers:
            parts = self.headers['Content-Disposition'].split(";")
            for part in parts:
                if "filename=" in part:
                    filename = part.split("=")[1].strip('"')

        filename = os.path.basename(filename)
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(self.rfile.read(content_length))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Upload successful")
        print(f"[+] File saved: {file_path}")


def run_node(host, cpu_percent, ram_percent):
    """Start a node with resource allocation."""
    global MAX_CPU_PERCENT, MAX_RAM_PERCENT
    try:
        allocated_cpu, allocated_ram = allocate_resources(cpu_percent, ram_percent)
        MAX_CPU_PERCENT = cpu_percent
        MAX_RAM_PERCENT = ram_percent
        
        print("\n" + "="*40)
        print(f"🔹 Starting Node: {host}:80")
        print(f"  Allocated Resources:")
        print(f"  - CPU: {allocated_cpu} cores ({cpu_percent}% of remaining)")
        print(f"  - RAM: {allocated_ram:.2f}GB ({ram_percent}% of remaining)")
        print(f"\n  Remaining Resources:")
        print(f"  - CPU Cores: {remaining_cpu}")
        print(f"  - RAM: {remaining_ram_gb:.2f}GB")
        print("="*40 + "\n")
        
        server = ThreadingHTTPServer((host, 80), NodeHandler)
        print(f"🚀 Server running on {host}:80")
        server.serve_forever()
        
    except Exception as e:
        print(f"❌ Failed to start node: {str(e)}")


if __name__ == "__main__":
    total_cpu, total_ram, remaining_cpu, remaining_ram = initialize_resources()
    print(f"\n🔹 System Resources:")
    print(f"  Total CPU Cores: {total_cpu}")
    print(f"  Total RAM: {total_ram:.2f}GB")
    print(f"  Remaining CPU Cores: {remaining_cpu}")
    print(f"  Remaining RAM: {remaining_ram:.2f}GB\n")
    
    parser = argparse.ArgumentParser(
        description="Distributed Server with Resource Tracking",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--host", required=True, help="Node IP/Hostname")
    parser.add_argument("--cpu", type=float, required=True, help="CPU percentage (of remaining)")
    parser.add_argument("--ram", type=float, required=True, help="RAM percentage (of remaining)")
    
    args = parser.parse_args()
    
    try:
        run_node(args.host, args.cpu, args.ram)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

