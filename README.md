# Under Huven OS

Under Huven OS (“under the hood”) is a terminal-based learning environment for exploring how CPU, memory, storage, processes, and the operating system work together. Students run short experiments and observe the effects in a separate live dashboard.

The project combines a Python application with a customised **MX Linux XFCE x86_64 live environment** for classroom workshops. MX Linux provides the operating system, desktop, hardware support, and live-image tooling; this repository provides the monitoring interface, experiments, and application launchers. It does not implement a kernel or a new operating system from scratch.

The application interface and teaching prompts are primarily in Swedish. This README documents operation and image preparation in English.

## What students investigate

The workshop follows a repeatable sequence: **predict → run one experiment → observe → explain**.

- **CPU:** how runnable workers compete for processor time, and why logical CPU count matters.
- **RAM:** the difference between installed, used, and available memory, and why allocating and touching memory also requires CPU work.
- **Storage:** the difference between occupied filesystem space and read/write activity, including the effects of buffering and live-system overlays.
- **Processes:** a program becomes active through processes that need CPU time, memory, and operating-system services.
- **System behaviour:** a CPU, RAM, or disk experiment targets one resource but can affect several others.

These are teaching demonstrations, not hardware certification, controlled benchmarks, or resource-isolation tests.

## Source code and bootable image

| Artifact | Contents | How it is used |
| --- | --- | --- |
| This GitHub repository | Python source, experiment settings, dependency pins, and installation/startup scripts | Clone onto an existing Linux system |
| Workshop ISO | MX Linux, XFCE, installed dependencies, the application under /opt, launchers, and desktop defaults | Boot in a VM or from a USB drive |
| Installed workshop system | A system installed from the live image onto a selected disk | Persistent use after an intentional installation |

Cloning the repository does not download or create the ISO. Desktop defaults, the system-wide command, and the MX Snapshot configuration described below are image-build steps; they are not currently automated by the repository.

The documented image choices are **MX Linux XFCE, x86_64, distribution/reset-accounts mode, and LZ4 compression**. The repository does not include the original base-ISO filename, package manifest, final ISO checksum, or a VM test log. The build procedure recreates the workshop setup; it is not a claim of byte-for-byte reproduction of a published image.

## Architecture

~~~text
scripts/start-workshop.sh
  ├── XFCE terminal → dashboard.py → tools/live_dashboard.py → psutil
  └── XFCE terminal → app.py
                       ├── monitoring and system-information modules
                       └── tools/experiments.py
                             ├── data/experiments.json
                             ├── stress subprocesses: CPU and RAM
                             └── Python file writes: disk
~~~

The two terminals run separate Python processes. The dashboard reads system-wide measurements; it does not receive telemetry from the experiment process. There is no web server, browser frontend, database, or network service in the application.

| File | Responsibility |
| --- | --- |
| [app.py](app.py) | Main menu and module selection |
| [dashboard.py](dashboard.py) | Standalone dashboard entry point |
| [tools/live_dashboard.py](tools/live_dashboard.py) | Rich panels, usage bars, and system measurements |
| [tools/cpu_monitor.py](tools/cpu_monitor.py), [tools/memory_monitor.py](tools/memory_monitor.py), [tools/disk_info.py](tools/disk_info.py) | Individual status views |
| [tools/system_info.py](tools/system_info.py) | OS, kernel, hostname, and architecture information through Python's platform module |
| [tools/experiments.py](tools/experiments.py) | Resource sizing, subprocess execution, progress display, and temporary-file handling |
| [data/experiments.json](data/experiments.json) | Durations, load ratios, caps, observation prompts, and teaching impact levels |
| [tools/explanations.py](tools/explanations.py), [tools/visualizer.py](tools/visualizer.py) | Explanations and illustrative component-impact panels |
| [tools/ui.py](tools/ui.py) | Menu presentation and terminal styling |
| [tools/byte_formater.py](tools/byte_formater.py) | Binary byte-to-gigabyte conversion |
| [install.sh](install.sh) | Debian-family packages, venv, Python dependencies, and current-user desktop launchers |
| [scripts/start-workshop.sh](scripts/start-workshop.sh) | Opens the dashboard and main menu in two XFCE terminals |
| [requirements.txt](requirements.txt) | Pinned Python dependencies |

Rich renders the interface, psutil supplies measurements, and the system utility stress creates CPU and memory workloads. Textual is included in requirements.txt, but the current interface uses Rich. tools/command_runner.py is an empty placeholder.

## What the dashboard measures

| Display | Implementation and interpretation |
| --- | --- |
| CPU Usage | System-wide psutil.cpu_percent(interval=None), averaged across logical CPUs |
| RAM Usage | psutil.virtual_memory().percent |
| RAM Total / Usage / Available | Total, used, and available values reported by psutil |
| DISK Usage | Percentage of filesystem capacity occupied at / |
| Disk Total / Usage / Available | Capacity values from psutil.disk_usage("/") |

The update loop sleeps for 0.5 seconds; Rich is configured to refresh once per second. Initial non-blocking CPU samples can be unrepresentative, so allow the dashboard to settle before recording a baseline.

**The disk bar is a capacity indicator, not an I/O throughput meter.** A short write may barely move it. The disk experiment reports its own written volume, elapsed time, calculated write rate, and change in system-wide disk-write counters.

Additional interpretation details:

- Values labelled GB use division by 1024³, so they are numerically GiB. Experiment sizes labelled MB use 1024²-byte units.
- Available RAM is memory the OS estimates can be used without swapping; it is not simply total minus the displayed used value.
- The dashboard measures the whole guest system in a VM, not the host machine.
- The disk experiment writes under the current user's home directory. That directory may be on a different filesystem from /.
- The component-impact bars shown before tests are predefined teaching illustrations, not measured percentages.
- The application does not show a process list. Use htop, or btop if installed, to inspect workers and PIDs.

## Adaptive experiments: exact current settings

Settings come from [data/experiments.json](data/experiments.json); sizing and execution are implemented in [tools/experiments.py](tools/experiments.py).

| Experiment | Settings | Runtime calculation |
| --- | --- | --- |
| CPU | load_ratio = 0.8; duration = 15 seconds | workers = max(1, int(logical_cpu_count × 0.8)); CPU count falls back to 1 |
| RAM | load_ratio = 0.3; max_mb = 4096; duration = 15 seconds | available_mb = int(available_bytes / 1024²); ram_mb = max(64, min(int(available_mb × 0.3), 4096)) |
| Disk | max_mb = 1024; duration = 15 seconds | Refuse if free_mb < 1024; otherwise target_mb = min(1024, int(free_mb × 0.05)) |

Sizing happens when each experiment starts. “Adaptive” means the workload is sized from the resources visible at that moment; there is no feedback controller that continuously maintains a target load.

### CPU

The generated command is:

~~~bash
stress --cpu WORKERS --timeout 15
~~~

For eight logical CPUs, the calculation produces six workers. **The 0.8 setting is a worker-count ratio, not a guaranteed 80% CPU usage.** Integer rounding, scheduling, other processes, and VM allocation affect the result. On a single logical CPU, the minimum of one worker can fully occupy that CPU.

A CPU worker still needs program instructions, a stack, and process data in memory. Consequently, a compute-heavy test can produce high CPU usage with only a small RAM increase.

### RAM

The generated command is:

~~~bash
stress --vm 1 --vm-bytes RAM_MB"M" --vm-keep --timeout 15
~~~

For 8,192 MiB available at startup, the calculation requests 2,457 MiB. The cap is 4,096 MiB and the minimum is 64 MiB. The percentage applies to **available memory**, not total installed memory.

The worker allocates and touches memory. The CPU executes those operations and the OS handles memory pages, so substantial CPU usage during this test is expected. The visible RAM change need not equal the requested amount exactly because background activity, accounting, and memory pressure also matter. The 64 MiB floor can exceed 30% of available RAM on a heavily constrained system.

### Disk

The test:

1. Creates ~/.under-huven if needed.
2. Opens ~/.under-huven/disk-test.bin for writing, replacing any existing file at that exact path.
3. Writes a reusable 4 MiB chunk containing ASCII zero characters.
4. Flushes Python's buffer and calls fsync after every 64 MiB and at the end.
5. Stops starting new writes when the target size is reached or 15 seconds have elapsed.
6. Reports the result and removes the test file in a finally block.

The size target can be exceeded by less than one 4 MiB chunk. A write or fsync already in progress can take the elapsed time beyond 15 seconds. System-wide disk counters can include unrelated activity and are not an isolated measurement of this file.

A live filesystem, page cache, virtual disk, or RAM-backed overlay can change what the experiment demonstrates. Its reported write rate is not a reliable SSD/HDD benchmark.

## Run locally on Linux

The complete workshop path targets Debian-family Linux with apt and XFCE Terminal. Other desktops can run the Python programs in two manually opened terminals. Native Windows and macOS are not the supported workshop environment.

Use a normal user account with sudo access for dependency installation. Network access is needed for installation; the installed application does not require network access to run its experiments.

### Manual setup

~~~bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv stress xfce4-terminal

git clone https://github.com/Tilly-py/under-huven-os.git
cd under-huven-os

python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -c "import rich, psutil; print('Python dependencies OK')"

venv/bin/python app.py
~~~

Use the venv directory name: the workshop launcher looks specifically for venv/bin/python. The pinned dependencies must support the Python version supplied by the chosen Linux release; treat any installation error as a setup failure before preparing an image.

### Repository installer

After cloning, the alternative is:

~~~bash
bash install.sh
~~~

The script installs Python tooling, Git, curl, wget, build-essential, micro, htop, tree, stress, and xfce4-terminal. It creates a venv, installs requirements, checks imports, and creates four desktop shortcuts in ~/Desktop, or ~/Skrivbord if ~/Desktop does not already exist.

Current installer details:

- It uses sudo for venv creation and package installation inside the venv, which can leave that environment root-owned. The manual local setup above creates a user-owned environment.
- The Systemmonitor shortcut invokes btop, but the script installs htop. Install btop separately with sudo apt install btop if using that shortcut.
- Launchers contain the checkout's absolute path. Moving the checkout requires regenerating them.
- The script prepares the current user's desktop. It does not populate /etc/skel or create an ISO.

Run the script as the normal desktop user, not with sudo bash install.sh.

### Start the workshop

~~~bash
bash scripts/start-workshop.sh
~~~

The script opens a dashboard terminal, waits one second, then opens the main-menu terminal. Arrange them side by side. In the main menu, choose 2 for experiments, then 1 for CPU, 2 for RAM, or 3 for disk.

Without XFCE Terminal, run these in two separate terminals, both from the repository directory:

~~~bash
# Terminal 1
venv/bin/python dashboard.py
~~~

~~~bash
# Terminal 2
venv/bin/python app.py
~~~

Press Ctrl+C to leave the dashboard. Main-menu option 7 is labelled SHUTDOWN but only exits the application; it does not shut down Linux.

## Build the MX Linux workshop image

Perform these steps in a dedicated MX Linux XFCE x86_64 build VM. They install software and prepare system-wide workshop files. Start with a clean VM without personal accounts, credentials, or unrelated work.

The commands below are an explicit image-preparation recipe. They supplement the repository scripts and do not modify the application code.

### 1. Prepare the base system

Obtain the MX Linux XFCE x86_64 ISO from [MX Linux](https://mxlinux.org/download-links/) and verify it against the checksum supplied for that exact download.

Boot the base ISO. **For the original project image, the systemd entry was the second boot-menu option.** Match the entry by its label on other MX versions; menu ordering can change. The Python application itself does not require systemd.

Install MX Linux onto the build VM's virtual disk, then boot that installed system. The workshop ISO will later be generated from this configured installation.

Confirm the architecture and record the base system:

~~~bash
uname -m
cat /etc/os-release
uname -r
python3 --version
~~~

The architecture must be x86_64. Record the base ISO filename and checksum along with these outputs for each build.

### 2. Install the application at a stable path

A reset-accounts snapshot creates a new live user. Keeping the application in a builder's home directory would make launchers depend on an account that is not preserved. Use /opt/under-huven-os instead.

For a fresh build where this directory does not already exist:

~~~bash
sudo apt update
sudo apt install -y \
  git python3 python3-pip python3-venv \
  stress xfce4-terminal htop btop

sudo git clone https://github.com/Tilly-py/under-huven-os.git /opt/under-huven-os

sudo python3 -m venv /opt/under-huven-os/venv
sudo /opt/under-huven-os/venv/bin/python -m pip install \
  -r /opt/under-huven-os/requirements.txt

sudo chmod 755 /opt/under-huven-os/scripts/start-workshop.sh
/opt/under-huven-os/venv/bin/python -c \
  "import rich, psutil; print('Python dependencies OK')"
~~~

Create the venv at its final location; do not move one created in another directory. Python environments and launchers can contain absolute paths.

For repeat builds, check out the same recorded full source commit before creating the environment, rather than silently taking a newer main. Record the installed source and package versions:

~~~bash
git -C /opt/under-huven-os rev-parse HEAD
/opt/under-huven-os/venv/bin/python -m pip freeze
dpkg-query -W > "$HOME/under-huven-packages.txt"
~~~

This recipe leaves application files owned by root and readable by workshop users. Launch the application as the normal user. Its disk experiment writes to that user's home, so /opt does not need to be writable.

### 3. Create the system-wide launcher

Create /usr/local/bin/under-huven as a wrapper around the existing two-terminal launcher:

~~~bash
sudo tee /usr/local/bin/under-huven >/dev/null <<'EOF'
#!/bin/sh
exec /opt/under-huven-os/scripts/start-workshop.sh
EOF

sudo chmod 755 /usr/local/bin/under-huven
~~~

From the XFCE desktop, test:

~~~bash
under-huven
~~~

Both terminals should open and imports should succeed without sudo.

### 4. Prepare the desktop template

Create a workshop shortcut in /etc/skel/Desktop:

~~~bash
sudo install -d -m 755 /etc/skel/Desktop

sudo tee /etc/skel/Desktop/1-Starta-Workshop.desktop >/dev/null <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=1. Starta Workshop
Comment=Open the Under Huven OS dashboard and experiments
Exec=/usr/local/bin/under-huven
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

sudo chmod 755 /etc/skel/Desktop/1-Starta-Workshop.desktop
~~~

Set the desktop directory for newly created accounts:

~~~bash
sudo install -d -m 755 /etc/skel/.config

sudo tee /etc/skel/.config/user-dirs.dirs >/dev/null <<'EOF'
XDG_DESKTOP_DIR="$HOME/Desktop"
EOF
~~~

Test the same shortcut in the build user's desktop:

~~~bash
mkdir -p "$HOME/Desktop"
cp /etc/skel/Desktop/1-Starta-Workshop.desktop "$HOME/Desktop/"
chmod +x "$HOME/Desktop/1-Starta-Workshop.desktop"
~~~

If XFCE asks whether to trust or allow launching the shortcut, approve it in that test session. Executable permission and launcher trust can be separate checks; confirm the behaviour again with the generated live user.

### 5. Set XFCE defaults for new users

Configure the dedicated build account's desktop and terminal through XFCE settings: readable font size, suitable colours, desktop icons, and a layout that leaves room for both windows.

Copy only the required settings into the skeleton. For example, preserve the terminal preferences if the file exists:

~~~bash
sudo install -d -m 755 /etc/skel/.config/xfce4/terminal

if [ -f "$HOME/.config/xfce4/terminal/terminalrc" ]; then
  sudo install -m 644 \
    "$HOME/.config/xfce4/terminal/terminalrc" \
    /etc/skel/.config/xfce4/terminal/terminalrc
fi
~~~

For appearance and desktop defaults, review the XML files generated by XFCE before copying them:

~~~bash
sudo install -d -m 755 /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml

for channel in xsettings xfwm4 xfce4-desktop; do
  config_file="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/$channel.xml"
  if [ -f "$config_file" ]; then
    sudo install -m 644 "$config_file" \
      "/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/$channel.xml"
  fi
done
~~~

Use system-wide paths for wallpaper and other referenced assets. Remove references to the build user's home and inspect monitor-specific desktop settings. Do not copy an entire home directory, browser profile, credentials, or cached XFCE sessions. These examples establish defaults; the repository does not define a fixed visual theme.

### 6. Create the snapshot

Open **MX Tools → MX Snapshot** on the configured build system.

1. Choose an output location with enough free space for the working files and ISO.
2. Select **Resetting accounts (for distribution to others)**.
3. Select **LZ4** compression, the choice used for this workshop image.
4. Review the exclusion settings. Retain /opt/under-huven-os, its venv, /usr/local/bin/under-huven, and the intended /etc/skel files.
5. Check the system for credentials and personal material outside /home as well as inside the desktop template.
6. Generate the ISO and retain the build log.

In reset-accounts mode, the live user's home is populated from /etc/skel rather than the builder's home. LZ4 prioritises compression speed over ISO size. See the [MX Snapshot documentation](https://mxlinux.org/wiki/help-files/help-mx-save-system-to-iso-snapshot/) for version-specific behaviour.

Account reset is not a substitute for inspecting the image contents. Test the resulting live login and any default credentials before distribution.

### 7. Generate and verify the checksum

In the directory containing the completed ISO, use its actual filename:

~~~bash
sha256sum under-huven-os-x86_64.iso > under-huven-os-x86_64.iso.sha256
sha256sum -c under-huven-os-x86_64.iso.sha256
~~~

On macOS, the equivalent verification is:

~~~bash
shasum -a 256 -c under-huven-os-x86_64.iso.sha256
~~~

The filename above is an example, not an advertised download. Keep the ISO and its checksum together, and verify the checksum again after copying or downloading. Publish the expected checksum through a trusted channel; generating a checksum alone does not authenticate an image.

### 8. Test the generated ISO in a fresh UTM VM

Create a new VM from the generated ISO, independent of the build VM. Do not reuse the build disk: that could hide missing dependencies or files.

- Select an x86_64 guest. On Apple Silicon, use UTM's QEMU **Emulate** path for x86_64; ARM virtualisation is a different architecture. See [UTM architecture documentation](https://docs.getutm.app/settings-qemu/system/).
- Leave the CPU model and emulation settings at suitable defaults. Record the actual CPU and RAM allocation.
- Boot the generated ISO into the live desktop without installing it.
- Verify the workshop icon exists for the fresh live user.
- Launch it and confirm that two terminals open.
- Run CPU, RAM, and disk tests separately. Confirm the selected sizes match guest resources.
- Confirm the disk-test file is removed and the dashboard can be closed normally.
- Confirm the workshop works without network access after boot.
- Reboot the live session and repeat the launcher check.

This validates the image's completeness, not physical-machine performance. Record the ISO checksum, UTM version, guest resources, and pass/fail results. A new ISO needs a new test; this repository does not contain a completed verification record.

### 9. Flash and boot a USB drive

After the fresh-VM test:

1. Back up the USB drive; flashing replaces its contents.
2. Use MX Live USB Maker or another ISO-capable image writer.
3. Select the generated ISO and verify the target USB device by its size and identity.
4. Write the image, allow verification to finish, and eject it safely.
5. On a compatible x86_64 computer, open the firmware's one-time boot menu and select the USB device.
6. Choose the appropriate live entry. For the original project image, use the second, systemd-labelled option; verify labels on other builds.
7. At the XFCE desktop, open Starta Workshop or run under-huven.

Copying an ISO onto an ordinary USB filesystem is not the same as flashing a bootable image. UEFI/legacy boot support depends on the image and target machine; test representative workshop hardware before class.

## Live session versus installation

**A live session boots the workshop from the ISO/USB without requiring installation onto the computer's internal disk.** Without configured persistence, session changes are normally lost at shutdown. Persistence is a separate live-USB configuration and is not created by the Python application.

The MX installer writes a persistent system to the selected disk and can alter partitions or erase existing data. It is optional for a workshop. Use it only when installation is intended and the target disk has been checked.

The application itself does not partition disks or invoke the installer. However, a live desktop can access mounted internal disks. “Live” does not mean that all writes are automatically harmless.

In a live session, the disk experiment may write into an overlay backed by RAM or persistence storage. Do not present that result as the internal drive's performance.

## Workshop procedure

1. Open the dashboard and experiment menu side by side.
2. Wait for an idle baseline and note CPU usage, available RAM, and the environment: physical machine, VM, or live session.
3. Ask which components should change before starting a test.
4. Run one experiment and observe the entire system.
5. Read the result, allow the system to settle, then compare with the prediction.
6. Use htop to connect the load to running processes.
7. Repeat with the next resource and explain the cross-effects.

Useful discussion prompts:

- Why does the CPU test need RAM even though it allocates no large data structure?
- Why does the RAM test consume CPU time?
- Why can disk writes finish without a visible change in the disk-capacity bar?
- How do VM resources and live overlays change the interpretation?
- Why do a program, a process, and a physical component describe different things?

## Safety and implementation limits

- Run experiments as a normal user, one at a time, on a dedicated workshop machine or VM. CPU load can increase heat and reduce responsiveness.
- The RAM cap and disk-space check reduce workload size; they do not reserve headroom against other processes. The RAM minimum can still be too large under severe memory pressure.
- The disk test owns ~/.under-huven/disk-test.bin. Do not store personal data there or run concurrent disk tests against that path.
- Disk cleanup uses finally, but forced termination, power loss, or filesystem errors can leave the file behind.
- CPU and RAM subprocesses receive a 15-second timeout. The application does not implement explicit process-group cleanup on every interruption.
- The stress runner suppresses stdout/stderr and does not validate its exit status before printing “Klart.” A completion message alone does not prove the load ran successfully.
- The dashboard has no temperature display, per-process metrics, experiment history, or live disk-throughput graph.

## Troubleshooting

| Symptom | Checks and action |
| --- | --- |
| “Python virtual enviroment not found” | The launcher requires venv/bin/python beside the source. Create the environment at that location and install requirements. |
| ModuleNotFoundError | Start with venv/bin/python or /opt/under-huven-os/venv/bin/python; install requirements using that same interpreter. |
| pip cannot install a pinned package | Check the actual Python version, package availability, and the first installation error. Do not distribute an image with a partially installed environment. |
| CPU/RAM experiment does not run | Confirm command -v stress. Install it with sudo apt install stress. For diagnosis, run the generated command in a terminal where errors are visible. |
| Workshop command opens no windows | Run it inside an XFCE graphical session; confirm xfce4-terminal is installed. From a text-only session, start the two Python entry points manually. |
| Desktop shortcut is missing after snapshot | Check /etc/skel/Desktop, user-dirs.dirs, and the snapshot exclusions. A shortcut only in the builder's home will not supply the reset live user's desktop. |
| Shortcut is untrusted or permission is denied | Check executable permissions and XFCE's allow-launching prompt. Confirm referenced files exist at the recorded absolute paths. |
| Systemmonitor shortcut fails | Install btop separately, or run the installed htop manually. |
| Disk bar barely changes | It measures used capacity at /, not I/O. Read the disk experiment's output and check which filesystem contains the home directory. |
| Disk test refuses to start | It requires at least 1,024 MiB free on the filesystem containing ~/.under-huven. Live overlay capacity may be smaller than the physical disk. |
| RAM increase differs from the displayed percentage | The size uses available RAM at test startup, with a 64 MiB floor and 4,096 MiB cap. Other activity and memory accounting affect measurements. |
| Stress load continues after interruption | Inspect your user's stress processes in htop and terminate only the workers belonging to the interrupted test. |
| disk-test.bin remains after an interrupted run | Confirm no disk test is running, inspect ~/.under-huven/disk-test.bin, and remove that generated file if needed. |
| x86_64 ISO will not boot in UTM on Apple Silicon | Check that the VM emulates x86_64 rather than virtualising an ARM guest. |
| ISO works in the build VM but not a fresh VM | Check for dependencies in the builder's home, missing /opt files, snapshot exclusions, and hard-coded account paths. |
| USB does not appear in the boot menu | Check that the ISO was flashed, that the write verified, and that the selected firmware boot mode supports the image. |

## License

No license file is currently included in this repository. This README does not assign a license to the project. MX Linux and bundled third-party software retain their own licenses.
