# Under the Hood OS

**Under the Hood OS** is a lightweight, terminal-based application designed for workshops that teach how computers work at a low level. It runs on Linux and provides a hands-on way to explore hardware, operating systems, CPU, memory, disk and system load through a simple menu-driven interface.

---

## Purpose

The goal of Under the Hood OS is to demystify system resources by providing real-time insights into a computer's hardware and operating system.

Participants can:

- View basic system information such as OS name, version, architecture and processor details.
- Monitor CPU usage.
- Monitor RAM usage.
- Check disk usage.
- See a live dashboard with updating charts.
- Run CPU and RAM stress tests to observe how load affects the system.
- Launch terminal-based apps from desktop icons.

The program complements theoretical presentations about computer architecture, memory, storage and operating systems by making these concepts tangible.

---

## Platform

Under the Hood OS is intended for Linux distributions such as:

- MX Linux
- Debian
- Ubuntu

It was developed and tested with **MX Linux XFCE** and works best on older PCs used in workshops.

Windows and macOS are not supported as target platforms for the workshop environment.

---

## Features

- **Menu-driven interface** - navigate through options without remembering commands.
- **System information** - view details about the operating system, kernel, architecture and processor.
- **CPU monitor** - display current CPU usage and core count.
- **Memory monitor** - display total, used and free memory.
- **Disk monitor** - display total, used and free disk space.
- **Live dashboard** - real-time charts of CPU, RAM and disk usage using the Rich library.
- **Visual CPU and RAM stress tests** - load the system while showing live metrics to illustrate how resources respond.
- **Desktop launchers** - XFCE `.desktop` files to start the program, dashboard and stress tests directly from the desktop.
- **Installer script** - one-stop setup script for Debian/MX/Ubuntu-based systems.

---

## Project structure

```text
under-huven-os/
├── app.py
├── dashboard.py
├── cpu_stress.py        (optional)
├── ram_stress.py        (optional)
├── install.sh
├── requirements.txt
├── README.md
├── README_en.md
├── docs/
├── tools/
│   ├── system_info.py    # show system information
│   ├── cpu_monitor.py    # CPU usage monitor
│   ├── memory_monitor.py # memory usage monitor
│   ├── disk_info.py      # disk usage monitor
│   ├── live_dashboard.py # live dashboard implementation
│   ├── stress_visual.py  # visual CPU and RAM stress test library
│   └── ui.py             # menu and UI helpers
└── venv/
```

---

## Installation

### Using the installer script

Clone the repository:

```bash
git clone https://github.com/Tilly-py/under-huven-os.git
cd under-huven-os
```

Make the installer executable:

```bash
chmod +x install.sh
```

Run the installer:

```bash
./install.sh
```

The installer will:

- Update package lists.
- Install required system packages:
  - `python3`
  - `pip`
  - `venv`
  - `git`
  - `xfce4-terminal`
  - `stress`
  - `htop`
  - `micro`
  - `tree`
- Create a Python virtual environment.
- Install Python dependencies from `requirements.txt`, mainly Rich and psutil.
- Create desktop launchers on your desktop or `Skrivbord` for:
  - the main program
  - the live dashboard
  - stress tests
  - `htop`

If your desktop folder is called `Skrivbord`, the installer will use that directory automatically.

---

## Manual installation

If you prefer manual setup, update packages and install system dependencies:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git htop tree stress xfce4-terminal
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install dependencies manually and generate the file:

```bash
pip install rich psutil
pip freeze > requirements.txt
```

---

## Running the program

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the main menu:

```bash
python app.py
```

Start the live dashboard directly:

```bash
python dashboard.py
```

Run visual stress tests:

```bash
python cpu_stress.py
python ram_stress.py
```

Exit a test or the dashboard with:

```text
Ctrl+C
```

---

## Desktop launchers

The installer creates launchers in your desktop folder:

- **Under Huven OS** - starts the main menu.
- **Live Dashboard** - starts the dashboard directly.
- **Visual CPU Stress Test** - runs the visual CPU test.
- **Visual RAM Stress Test** - runs the visual RAM test.
- **System Monitor** - opens `htop`.

If XFCE asks to trust these files, choose:

```text
Allow Launching
```

or:

```text
Mark as Trusted
```

---

## Workshop usage

This project is designed for an educational workshop. A simple flow might be:

1. Boot into MX Linux.
2. Launch **Under Huven OS**.
3. Review system information to understand the operating system, CPU and RAM.
4. Start **Live Dashboard** to see real-time resource usage.
5. Run **Visual CPU Stress Test** and **Visual RAM Stress Test** to observe how load affects the system.
6. Open **System Monitor** using `htop` to compare metrics.
7. Discuss how CPU, memory, disk and the operating system interact.

---

## Safety notes

The stress tests intentionally allocate CPU time and memory. They are safe for a short demonstration on older hardware, but avoid large memory allocations or long runtimes.

Avoid:

- extreme stress values
- running multiple heavy tests simultaneously
- large RAM allocations on weak computers
- long stress-test sessions without supervision

---

## License

Under the Hood OS is created for educational use as part of the **Under Huven** workshop.
