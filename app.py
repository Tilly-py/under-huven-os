from tools.system_info import get_system_info
from tools.cpu_monitor import show_cpu_usage
from tools.memory_monitor import show_memory_usage
from tools.disk_info import show_disk_info
from tools.live_dashboard import show_live_dashboard
from tools.ui import show_header, show_menu, print_error
from tools.experiments import show_experiment_menu


def main():
    while True:
        show_header()
        show_menu()
        choice = input("Enter Your Choice: ")

        if choice == "1":
            show_live_dashboard()
        elif choice == "2":
            show_experiment_menu()
        elif choice == "3":
            get_system_info()
        elif choice == "4":
            show_cpu_usage()
        elif choice == "5":
            show_memory_usage()
        elif choice == "6":
            show_disk_info()
        elif choice == "7":
            print("Exiting Under Huven OS!")
            break
        else:
            print_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
