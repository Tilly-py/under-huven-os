#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_DIR="$HOME/Desktop"

if [ ! -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR="$HOME/Skrivbord"

fi

echo "======================================"
echo "      Under Huven OS Installer"
echo "======================================"
echo ""

echo "[1/7] Checking operating system..."

if ! command -v apt >/dev/null 2>&1; then
    echo "This installer is made for Debian/MX/Ubuntu based systems"
    exit 1
fi

echo "[2/7] Updating package lists..."
sudo apt update

echo "[3/7] Installing system packages..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    build-essential \
    micro \
    htop \
    tree \
    stress \
    xfce4-terminal

echo "[4/7] Creating Python virtual environment..."
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
else
    echo "Virtual environment already exists, skipping..."
fi

echo "[5/7] Installing Python dependencies..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install rich psutil
    pip freeze > requirements.txt
fi

echo "[6/7] Creating desktop launchers..."
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/Under-Huven-OS.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Under Huven OS
Comment=Start Under Huven OS
Exec=xfce4-terminal --hold --working-directory=$PROJECT_DIR -e "bash -c 'source venv/bin/activate && python app.py'"
Icon=utilities-terminal
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/Live-Dashboard.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Live Dashboard
Comment=Start live system dashboard
Exec=xfce4-terminal --hold --working-directory=$PROJECT_DIR -e "bash -c 'source venv/bin/activate && python dashboard.py'"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/CPU-Stress-Test.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=CPU Stress Test
Comment=Stress CPU for 15 seconds
Exec=xfce4-terminal --hold -e "bash -c 'echo Starting CPU stress test...; stress --cpu 2 --timeout 15; echo Done.; read -p \"Press Enter to close...\"'"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/RAM-Stress-Test.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=RAM Stress Test
Comment=Stress RAM for 15 seconds
Exec=xfce4-terminal --hold -e "bash -c 'echo Starting RAM stress test...; stress --vm 1 --vm-bytes 256M --timeout 15; echo Done.; read -p \"Press Enter to close...\"'"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/System-Monitor.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=System Monitor
Comment=Open htop system monitor
Exec=xfce4-terminal --hold -e "htop"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

chmod +x "$DESKTOP_DIR/Under-Huven-OS.desktop"
chmod +x "$DESKTOP_DIR/Live-Dashboard.desktop"
chmod +x "$DESKTOP_DIR/CPU-Stress-Test.desktop"
chmod +x "$DESKTOP_DIR/RAM-Stress-Test.desktop"
chmod +x "$DESKTOP_DIR/System-Monitor.desktop"

echo "[7/7] Testing Installation..."

python3 -c "import rich, psutil; print('Python dependencies OK')"



echo ""
echo "======================================"
echo " Installation complete!"
echo "======================================"
echo ""
echo "Desktop launchers created in:"
echo "$DESKTOP_DIR"
echo ""
echo "You can now run:"
echo "cd $PROJECT_DIR"
echo "source venv/bin/activate"
echo "python app.py"
echo ""
echo "Or double-click the desktop icons."