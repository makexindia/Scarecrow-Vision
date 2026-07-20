# Phase 1: Hardware & OS Setup

## 🛠️ Hardware Requirements
* **Compute:** Raspberry Pi 2 Model B (Vintage) + Protective Case
* **Storage:** MicroSD Card (16GB+ recommended)
* **Vision:** Standard USB 2.0 Web Camera
* **Connectivity:** Tenda USB Wi-Fi Adapter (The Pi 2 does not have onboard Wi-Fi)
* **Power:** 5V Micro-USB Power Adapter

<details>
<summary><strong>🧠 Why this specific hardware?</strong></summary>
The Raspberry Pi 2 is a low-power, 32-bit ARMv7 device with only 1GB of RAM. While modern AI usually requires heavy GPUs, this project proves that highly optimized, quantized Machine Learning models can run smoothly on decade-old, inexpensive edge devices.
</details>

---

## ⚙️ Step 1: Operating System & Headless Setup

Because the Pi 2 has a 32-bit processor, modern 64-bit OS versions will fail. We use a lightweight, legacy OS to maximize available RAM for the AI.

1. Download and install **Raspberry Pi Imager** on your PC.
2. Insert your SD card via an adapter.
3. In Imager, select **OS > Raspberry Pi OS (Other) > Raspberry Pi OS (Legacy, 32-bit) Lite**.
4. Click the **Gear Icon (Advanced Options)** to pre-fill your configuration:
   * **Hostname:** `scarecrow`
   * **Enable SSH:** Use password authentication
   * **Username/Password:** Set your credentials (e.g., `pi` / `yourpassword`)
   * **Configure Wireless LAN:** Enter your Wi-Fi SSID and password.
5. Click **Write**. Once finished, insert the SD card into the Pi, plug in the Wi-Fi adapter and camera, and power it on.
6. Wait 2-3 minutes, then SSH into the device from your PC: `ssh pi@scarecrow.local`.
