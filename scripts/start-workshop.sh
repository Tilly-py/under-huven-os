#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON ="$PROJECT_DIR/venv/bin/python"


if [ ! -x "$PYTHON" ]; then
    echo "Python virtual enviroment not found"
    echo "Run ./install.sh first"
    read -p "Press enter to close..."
    exit 1
fi


xfce4-terminal \
    --title="Under Huven OS - Live Dashboard" \
    --working-directory="$PROJECT_DIR" \
    --command "bash -c '$PYTHON dashboard.py; read -p \"Tryck enter för att stänga...\"'"&


sleep 1


xfce4-terminal \
  --title="Under Huven OS - Experiment" \
  --working-directory="$PROJECT_DIR" \
  --command "bash -c '$PYTHON app.py; read -p \"Tryck Enter för att stänga...\"'"