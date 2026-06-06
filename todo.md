## Next Steps / To-Do

### 1. Add visual stress test representations

The stress tests should be more visual and educational.
When a student runs a CPU, RAM or disk stress test, the program should show a live representation of what is happening.

Examples:

- CPU stress test: show CPU usage, active cores, load level and time remaining.
- RAM stress test: show allocated memory, total memory usage and available memory.
- Disk/write stress test: show how much data is being written, current write speed and progress over time.

The goal is that students should not only run a test, but also understand what kind of resource is being used and how the computer reacts.

```bash
Writing test file...
Written: 384 MB / 1024 MB
Speed: 72 MB/s
Disk usage: 41%
Time left: 8s
```

---

### 2. Review the Linux distribution for unnecessary applications

The selected Linux distribution should be reviewed to check if it contains unnecessary applications or background services that may slow down older test computers.

Things to check:

- unnecessary startup applications
- heavy background services
- preinstalled software that is not needed for the workshop
- desktop effects or compositing that may reduce performance
- whether a lighter setup of MX Linux XFCE is possible

The goal is to keep the system lightweight, fast and reliable for older hardware.

---

### 3. Test the USB installation workflow

The USB installation process needs to be tested to see if it is fast and efficient enough for the workshop.

Ideal workshop flow:

1. Students boot from the USB drive.
2. Students install the Linux distribution.
3. Students clone the repository.
4. Students run the installer script.
5. Students test the system using the dashboard and stress tests.

If this process takes too long, the computers should be prepared before the workshop instead. In that case, the workshop can focus on exploring the system rather than waiting for installations to finish.
