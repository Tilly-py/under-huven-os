from tools.system_info import get_system_info
from tools.cpu_monitor import show_cpu_usage
from tools.memory_monitor import show_memory_usage
from tools.disk_info import show_disk_info
from tools.live_dashboard import show_live_dashboard
from tools.ui import show_header, show_menu, print_error



def main():
    while True:
        show_header()
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
            show_live_dashboard()
        elif choice == '6':
            print("Exiting Under Huven OS!")
            break
        else:
            print_error("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
