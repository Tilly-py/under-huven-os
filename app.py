from tools.system_info import get_system_info
from tools.cpu_monitor import show_cpu_usage
from tools.memory_monitor import show_memory_usage
from tools.disk_info import show_disk_info

def show_menu():
    print("\n=== Under Huven OS ===")
    print("1. Show system information")
    print("2. Show CPU usage")
    print("3. Show memory usage")
    print("4. Show disk information")
    print("5. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter Your Choice: ")

        if choice == '1':
            get_system_info()
        elif choice == '2':
            show_cpu_usage()
        elif choice == '3':
            show_memory_usage()
        elif choice == '4':
            show_disk_info()
        elif choice == '5':
            print("Exiting Under Huven OS!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
