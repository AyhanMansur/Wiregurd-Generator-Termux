
# 🛡️ WireGuard Config Generator (Termux & Linux)

<div align="center">
  <img src="https://raw.githubusercontent.com/AyhanMansur/Wiregurd-Generator-Termux/main/First%20run%20😎.jpg" alt="Demo Screenshot" width="134">
  <br>
  <i>A lightweight, cross-platform utility for generating secure, obfuscated WireGuard configurations.</i>
</div>

---

## 📋 Overview

**WireGuard-Generator** is a high-performance Python utility designed to generate secure, single-peer WireGuard configurations with dynamic IP masking. 

This tool simplifies the process of creating privacy-focused tunnels by automatically selecting endpoints from trusted, high-performance IP ranges (such as **ArvanCloud** and **Cloudflare**). This effectively obfuscates traffic, making your tunnel traffic appear as standard HTTPS traffic to bypass restrictions and enhance anonymity.

## ✨ Key Features

- 🔐 **Automated Key Generation**: Utilizes native `wg` tools to generate cryptographically secure key pairs instantly.
- 🌐 **Traffic Obfuscation**: Dynamically selects server endpoints from trusted IP ranges to mask tunnel traffic.
- ⚡ **Optimized Performance**: Generates single-peer configurations for maximum speed and minimal latency.
- 📱 **Cross-Platform**: Fully compatible with **Linux** (Ubuntu/Debian) and **Android** (Termux).
- 📦 **Zero Dependencies**: Relies solely on standard Python libraries and system `wireguard-tools`.

## 🛠️ Installation & Usage

### Prerequisites
- **Python 3.6+**
- **WireGuard Tools** installed on the host system.
- Important Notes for Termux:
Permissions: If you choose to save to /sdcard/Download, you must run termux-setup-storage first and grant permission.

### Step 1: Install WireGuard Tools
**For Android (Termux):**
```bash
pkg update && pkg install wireguard-tools

termux-setup-storage

pkg install python

curl -O https://raw.githubusercontent.com/AyhanMansur/Wiregurd-Generator-Termux/refs/heads/main/WGAyhan.py

python3 WGAyhan.py
