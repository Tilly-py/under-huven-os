import psutil

def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)


def show_memory_usage():
    print("\n=== Memory Usage ===")
    memory = psutil.virtual_memory()

    print(f"Total Memory: {bytes_to_gb(memory.total)} GB")
    print(f"Available Memory: {bytes_to_gb(memory.available)} GB")
    print(f"Used Memory: {bytes_to_gb(memory.used)} GB")
    print(f"Memory Percentage: {memory.percent}%")

