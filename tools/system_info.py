import platform

def get_system_info():
    print("\n=== System Information ===")
    print(f"System: {platform.system()}")
    print(f"Node: {platform.node()}")
    print(f"Distribution: {platform.platform()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")