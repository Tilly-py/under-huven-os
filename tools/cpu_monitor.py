import psutil


def show_cpu_usage():
    print("\n=== CPU Usage ===")
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=True)

    print(f"CPU Cores: {cpu_cores}")
    print(f"CPU Usage: {cpu_percent}%")