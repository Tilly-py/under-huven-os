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
chmod +x "$PROJECT_DIR/scripts/start-workshop.sh"

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

cat > "$DESKTOP_DIR/1-Starta-Workshop.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=1. Starta Workshop
Comment=Starta Under Huven OS med dashboard och experiment
Exec=$PROJECT_DIR/scripts/start-workshop.sh
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/2-Under-Huven-OS.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=2. Under Huven OS
Comment=Starta huvudappen
Exec=xfce4-terminal --hold --working-directory=$PROJECT_DIR --command "bash -c '$PROJECT_DIR/venv/bin/python $PROJECT_DIR/app.py'"
Icon=utilities-terminal
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/3-Live-Dashboard.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=3. Live Dashboard
Comment=Starta live system dashboard
Exec=xfce4-terminal --hold --working-directory=$PROJECT_DIR --command "bash -c '$PROJECT_DIR/venv/bin/python $PROJECT_DIR/dashboard.py'"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

cat > "$DESKTOP_DIR/4-Systemmonitor.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=4. Systemmonitor
Comment=Öppna btop systemmonitor
Exec=xfce4-terminal --hold --command "btop"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
EOF

chmod +x "$DESKTOP_DIR/1-Starta-Workshop.desktop"
chmod +x "$DESKTOP_DIR/2-Under-Huven-OS.desktop"
chmod +x "$DESKTOP_DIR/3-Live-Dashboard.desktop"
chmod +x "$DESKTOP_DIR/4-Systemmonitor.desktop"

echo "[7/7] Testing Installation..."

venv/bin/python -c "import rich, psutil; print('Python dependencies OK')"



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