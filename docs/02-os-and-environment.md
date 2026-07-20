# Phase 2: OS & Environment Prep

## 📦 Step 2: System Preparation & Dependencies

The legacy package repositories have been moved to an archive. We must update the system pointers before installing our core tools.

```bash
# 1. Point package manager to the legacy archives
sudo sed -i 's/raspbian.raspberrypi.com/archive.raspbian.org/g' /etc/apt/sources.list
sudo sed -i 's/raspbian.raspberrypi.org/archive.raspbian.org/g' /etc/apt/sources.list

# 2. Update the system
sudo apt update

# 3. Install core tools (Node.js, compilation tools, audio/video pipelines)
sudo apt install -y nodejs npm gcc g++ make build-essential sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1
```

---

## 🚀 Step 5: Deployment & Environment Setup

We must download the model as an `.eim` (Edge Impulse Model) executable file.

1. Run the downloader on the Pi:
```bash
edge-impulse-linux-runner --download modelfile.eim
chmod +x modelfile.eim
```

### Setting up the Python Sandbox

Compiling heavy libraries like OpenCV from source via `pip` on a Pi 2 will fail or take hours. We install pre-compiled binaries via the system manager, then link them to an isolated Python virtual environment.

```bash
# 1. Install system-level pre-compiled dependencies
sudo apt install -y python3-opencv portaudio19-dev python3-pyaudio python3-venv

# 2. Create the project folder
mkdir ~/scarecrow-vision
cd ~/scarecrow-vision
mv ~/modelfile.eim .

# 3. Create a virtual environment that can "see" the system OpenCV
python3 -m venv --system-site-packages scarecrow_env
source scarecrow_env/bin/activate

# 4. Install the lightweight Python wrapper
pip3 install edge_impulse_linux pyaudio flask
```
