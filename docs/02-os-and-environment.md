# Phase 2: OS & Environment Prep

## 📦 Step 2: System Preparation & Dependencies

The legacy package repositories have been moved to an archive. We must update the system pointers before installing our core tools.

```bash
# 1. Point package manager to the legacy archives
sudo sed -i 's/raspbian.raspberrypi.com/archive.raspbian.org/g' /etc/apt/sources.list
sudo sed -i 's/raspbian.raspberrypi.org/archive.raspbian.org/g' /etc/apt/sources.list

# 2. Update the system
sudo apt update

# 3. Install core tools (Node.js, compilation tools, audio/video pipelines, git)
sudo apt install -y git nodejs npm gcc g++ make build-essential sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1
```

---

## 📥 Step 3: Download the Repository

You need the project source code containing the Python inference scripts (`src/scarecrow.py`).

```bash
cd ~
git clone https://github.com/lakshaygoel003/rpi_edge_ai.git scarecrow-vision
cd scarecrow-vision
```

---

## 🐍 Step 4: Setting up the Python Sandbox

Compiling heavy libraries like OpenCV from source via `pip` on a Pi 2 will fail or take hours. We install pre-compiled binaries via the system manager, then link them to an isolated Python virtual environment.

```bash
# 1. Install system-level pre-compiled dependencies
sudo apt install -y python3-opencv portaudio19-dev python3-pyaudio python3-venv

# 2. Create a virtual environment that can "see" the system OpenCV
# (Ensure you are still inside the scarecrow-vision folder)
python3 -m venv --system-site-packages scarecrow_env
source scarecrow_env/bin/activate

# 3. Install the lightweight Python wrapper
pip3 install edge_impulse_linux pyaudio flask
```
