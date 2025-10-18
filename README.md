# HostNowX

## 📈 V1.2 Known Issues

* Some performance issues may occur
* Updating python fixes it

* **For now, please be patient, it's unoptimized**

HostNowX is a Python application for managing multiple Minecraft servers. You can add, edit, run, stop, restart, and monitor servers easily

> ⚠️ **Windows-only for now. Linux support coming soon!**

---

## Features

- **Add and manage multiple Minecraft servers** easily through a GUI  
- **Run, stop, and restart servers** directly from the interface  
- **Server console** with real-time logs and command input  
- **Server information** including:
  - Uptime
  - RAM usage
  - CPU usage
  - Storage usage  
- **Dark themed modern GUI** built with PyQt6  
- **Server detection**
- **Customizable RAM allocation** per server (including custom RAM values)  
- **Context menu** with quick actions:
  - Edit Server
  - Open Console
  - Open Folder
  - Remove
  - Restart
  - Run
  - Stop
  - Server Info  

---

## Installation (Windows Only)

1. **Install Python 3.10 or higher**  
   - Download Python from [python.org](https://www.python.org/downloads/windows/)  
   - During installation, **check "Add Python to PATH"**.

2. **Install required Python packages**:  
   Open Command Prompt and run:
   ```cmd
   pip install PyQt6 psutil
