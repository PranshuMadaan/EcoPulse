# 🌱 EcoPulse AI // Smart Campus Energy Optimization Framework

> **Autonomous Hardware Telemetry, Unsupervised Machine Learning Audit, and VFD HVAC Analytics for Thapar Institute of Engineering & Technology (TIET).**

---

## 📌 Executive Summary

**EcoPulse AI** is a low-cost, IoT-enabled smart energy management platform designed to eliminate electrical waste across university campus infrastructure.

By pairing sub-second **ESP32 hardware telemetry** and **HC-SR501 PIR motion sensing** with **Isolation Forest machine learning**, EcoPulse AI detects baseline electrical anomalies and regulates heavy HVAC motor loads via **Variable Frequency Drive (VFD) Affinity Laws**.

---

## ⚡ Key Modules & Features

### 1. 📡 IoT Hardware & Live Telemetry (`/api/iot`)

* **Hardware**: ESP32 Microcontroller + HC-SR501 Passive Infrared (PIR) Sensor (GPIO 14).
* **Location Focus**: **CSED Computer Lab 204** (Computer Science & Engineering Dept).
* **Capabilities**: Reads real-time voltage (220 V – 232 V), current (A), and active power (W). Automatically triggers a **CRITICAL UNOCCUPIED DRAIN ALERT** when active loads exceed the threshold during zero-occupancy periods.

### 2. 🧠 AI Energy Anomaly Audit (`/api/audit`)

* **Algorithm**: Unsupervised **Isolation Forest** (Scikit-Learn).
* **Campus Feeders**: Tracks 24-hour baseline profiles across **Nava Nalanda Central Library (Floor 2)**, **Hostel M**, and **Block C (LH 102)**.
* **Impact**: Flags late-night off-hour power leaks (2:00 AM – 5:30 AM), converting wasted kilowatt-hours into financial loss in Indian Rupees (₹).

### 3. 🌀 VFD HVAC Motor & Carbon Calculator (`/api/vfd`)

* **Physics Principle**: Centrifugal Affinity Laws governing fluid and air movement:

  $$\frac{P_2}{P_1} = \left(\frac{N_2}{N_1}\right)^3$$

* **Target Facility**: **Thapar Auditorium (TAN)** 22 kW (30 HP) Air Handling Unit (AHU) blower motor.
* **Financial & Environmental Metrics**: Evaluated against the **PSPCL HT Institutional Tariff (₹7.80 / kWh)** and a carbon emission factor (0.7 kg CO₂ / kWh), demonstrating that a **20% speed drop yields ~48.8% energy savings**.

---

## 🏫 Thapar Campus Parameters

| Parameter | Value |
| :--- | :--- |
| Target Facility | Thapar Auditorium (TAN) |
| HVAC Load | 22 kW (30 HP) AHU blower motor |
| Electricity Tariff | PSPCL HT Institutional Tariff, ₹7.80 / kWh |
| Carbon Emission Factor | 0.7 kg CO₂ / kWh |
| Modeled Speed Reduction | 20% |
| Estimated Energy Savings | ~48.8% |
| IoT Test Location | CSED Computer Lab 204 |
| Supply Voltage Range | 220 V – 232 V |

---

## 🏗️ Architecture & Directory Structure

```text
ecopulse-ai/
├── api/                        # Vercel Python Serverless Handlers
│   ├── iot_telemetry.py        # Sub-second ESP32 & PIR telemetry API
│   ├── ai_audit.py             # Isolation Forest anomaly detection API
│   └── vfd_analytics.py        # VFD Affinity Law & carbon math API
├── public/                     # Static Single-Page Astra UI Shell
│   ├── index.html              # EcoPulse UI dashboard (GPT-6 Astra style)
│   ├── css/
│   │   └── astra-theme.css     # Glassmorphism, neon glows & dark obsidian theme
│   └── js/
│       └── app.js              # Single-page tab switcher & API fetch handlers
├── design.md                   # Complete UX design specification
├── requirements.txt            # Python runtime dependencies
├── vercel.json                 # Single-origin route configuration
└── README.md                   # Project documentation
```
