# 🌐 Network Traffic Monitoring and Analysis Platform

A real-time network traffic monitoring and analysis platform built with Python, Flask, and Scapy. The system captures live network packets directly from the host machine's active network interface and presents them through an intuitive web-based dashboard. It identifies protocol types (TCP, UDP, ICMP), maps port numbers to service names, provides real-time filtering by protocol and IP address, displays live statistics, maintains session logs, and supports reloading of previous monitoring sessions — making it a complete, functional, and practical network analysis tool.

## ✅ Features

- 🔴 Real-time Packet Capture — Captures live TCP, UDP, and ICMP packets using Scapy
- 🔍 Filtering — Filter by Protocol, Source IP, and Destination IP
- 📊 Live Statistics — Total packets, per-protocol count, average packet size
- 🗺️ Port to Service Mapping — Port 80 → HTTP, Port 443 → HTTPS, Port 53 → DNS
- 📋 System Logs — Timestamped log of all monitoring activity
- 💾 Session Management — Reload previous session data anytime
- ⚡ Auto Refresh — Interface updates every 3 seconds automatically

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.13, Flask 3.1.3 |
| Packet Capture | Scapy 2.7.0, Npcap 1.87 |
| Data Handling | Pandas 3.0.2 |
| Frontend | HTML5, CSS3, JavaScript |

## 📦 Installation

### Step 1: Install Npcap
Required for Scapy to capture packets on Windows.
👉 Download: https://npcap.com/#download

### Step 2: Install Python Libraries
```
pip install flask pandas scapy
```

## ▶️ How to Run

⚠️ Must run terminal as Administrator — required for packet capture

```
py -3.13 app.py
```

Then open browser:
```
http://localhost:5000
```

## 📁 Project Structure

```
network_project/
├── app.py            # Flask backend + Scapy packet capture
├── traffic_data.csv  # Auto-generated session dataset (created at runtime)
└── templates/
    └── index.html    # Web interface
```

## 📊 Dataset Description

This project uses **real-time packet sniffing** instead of a pre-generated dataset. The dataset (`traffic_data.csv`) is automatically created when monitoring starts and is populated with live packets captured from the host machine's active network interface.

> **Note:** Since the dataset is generated dynamically at runtime, no static CSV file is included in this repository. The file appears automatically in the project root after starting a monitoring session.

Each captured packet record contains the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| Time | Capture timestamp | `10:35:21` |
| Source_IP | Sender's IP address | `192.168.1.5` |
| Destination_IP | Receiver's IP address | `8.8.8.8` |
| Protocol | Network protocol | `TCP` / `UDP` / `ICMP` |
| Packet_Size | Total size in bytes | `512` |
| Source_Port | Sender's port number | `52341` |
| Destination_Port | Receiver's port number | `80` |
| Service | Mapped service name | `HTTP` |

## 🚀 How It Works

1. Click **Start Monitoring** → Scapy begins capturing live packets in a background thread
2. Each captured packet is processed and appended to `traffic_data.csv` in real time
3. The interface auto-refreshes every 3 seconds to display new packets and update statistics
4. Use filters (Protocol / Source IP / Destination IP) to view specific traffic
5. Click **Stop Monitoring** → capture stops but data remains saved
6. Click **Load Previous Session** → reload all captured packets from the CSV file

## 🔌 Port to Service Mapping

The system maps the following common ports to their service names:

| Port | Service |
|------|---------|
| 80 | HTTP |
| 443 | HTTPS |
| 53 | DNS |
| 22 | SSH |
| 21 | FTP |
| 25 | SMTP |
| 110 | POP3 |
| 3306 | MySQL |
| 8080 | HTTP-ALT |

Unknown ports are displayed as `Port-XXXX`.
