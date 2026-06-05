import psutil
from tools.memory_monitor import bytes_to_gb

def show_disk_info():
    print("\n=== Disk Information ===")
    disk = psutil.disk_usage("/")

    print(f"Total Disk Space: {bytes_to_gb(disk.total)} GB")
    print(f"Used Disk Space: {bytes_to_gb(disk.used)} GB")
    print(f"Free Disk Space: {bytes_to_gb(disk.free)} GB")
    print(f"Disk Usage Percentage: {disk.percent}%")