import os
import psutil
from prometheus_client import start_http_server, Gauge
from dotenv import load_dotenv
import time

load_dotenv()

HOST = os.getenv('EXPORTER_HOST', '0.0.0.0')
PORT = int(os.getenv('EXPORTER_PORT', 8080))

cpu_usage = Gauge('cpu_usage', 'Usage of CPU cores', ['core'])
memory_total = Gauge('memory_total', 'Total memory in the system')
memory_used = Gauge('memory_used', 'Used memory in the system')
disk_total = Gauge('disk_total', 'Total disk space')
disk_used = Gauge('disk_used', 'Used disk space')


def collect_metrics():
    psutil.cpu_percent(interval=0.5, percpu=True)
    time.sleep(1)
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_usage.labels(core=f'core_{i}').set(percentage)

    # Memory Usage
    memory = psutil.virtual_memory()
    memory_total.set(memory.total)
    memory_used.set(memory.used)

    # Disk Usage
    disk = psutil.disk_usage('/')
    disk_total.set(disk.total)
    disk_used.set(disk.used)


if __name__ == '__main__':
    start_http_server(PORT, addr=HOST)
    print(f"Exporter running on {HOST}:{PORT}")

    while True:
        collect_metrics()
