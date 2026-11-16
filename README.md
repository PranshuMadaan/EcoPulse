# 🌱 EcoPulse AI // Smart Campus Energy Optimization Framework

> **Autonomous Hardware Telemetry, Unsupervised Machine Learning Audit, and VFD HVAC Analytics for Thapar Institute of Engineering & Technology (TIET), Patiala.**
>
> **Course:** Energy & Environment (UEN008) · **Group:** 4 · **Section:** 1A14

---

## 📌 Executive Summary

**EcoPulse AI** is an IoT-enabled smart campus energy management platform designed to eliminate electrical waste across university campus infrastructure.

By pairing sub-second **ESP32 hardware telemetry** and **HC-SR501 PIR motion sensing** with **Isolation Forest machine learning**, EcoPulse AI detects baseline electrical anomalies and regulates heavy HVAC motor loads via **Centrifugal Affinity Laws**.

---

## ⚡ Key Modules & Features

### 1. 📡 IoT Hardware & Live Telemetry (`/api/iot`)
* **Hardware**: ESP32 Microcontroller Node `ESP32-THAPAR-CSED-LAB204` + HC-SR501 Passive Infrared (PIR) Sensor (GPIO 14).
* **Location**: **CSED Computer Lab 204** (Computer Science & Engineering Department).
* **Capabilities**: Reads real-time voltage ($228.0\,\text{V} - 232.5\,\text{V}$), current (A), and active power (W) across 3 sub-circuits (Lighting, Desktop PC Racks, HVAC split units).
* **Automated Alert Engine**: Triggers **CRITICAL UNOCCUPIED DRAIN ALERT: 18.6 kW** when active loads persist during zero-occupancy periods. Includes a solid-state relay cutoff actuation control.

### 2. 🧠 AI Energy Anomaly Audit (`/api/audit`)
* **Algorithm**: Unsupervised **Isolation Forest** (`scikit-learn`).
* **Campus Feeders**: Tracks 24-hour baseline profiles across:
  * **Nava Nalanda Central Library (Floor 2)**: $42\,\text{kWh}$ off-hour leak $\rightarrow$ ₹327.60 / night
  * **Hostel M (Block A/B Night Baseline)**: $28\,\text{kWh}$ off-hour leak $\rightarrow$ ₹218.40 / night
  * **Academic Block C (LH 102 Split ACs)**: $15\,\text{kWh}$ off-hour leak $\rightarrow$ ₹117.00 / night
* **Anomaly Window**: 02:00 AM – 05:30 AM with a **94.6% anomaly confidence score**.
* **Financial Impact**: Evaluated against the **PSPCL Commercial HT Tariff (₹7.80/kWh)**, identifying **₹1,944 / day** (₹7.1 Lakhs/year) and **41.8 Tonnes CO₂** in avoidable off-hour electrical waste.

### 3. 🌀 VFD HVAC Motor & Carbon Calculator (`/api/vfd`)
* **Physics Principle**: Centrifugal Affinity Laws governing fluid and air movement:
  $$\frac{Q_2}{Q_1} = \frac{N_2}{N_1}, \quad \frac{H_2}{H_1} = \left(\frac{N_2}{N_1}\right)^2, \quad \frac{P_2}{P_1} = \left(\frac{N_2}{N_1}\right)^3$$
* **Target Facility**: **Thapar Auditorium (TAN)** 22 kW (30 HP) Air Handling Unit (AHU) blower motor.
* **Financial & Environmental Metrics**:
  * Modeled at 3,500 active campus operating hours/year.
  * Demonstrates that a **20% speed drop (80% setpoint) yields ~48.8% energy savings**.
  * Saves **₹2,93,202 / year** and mitigates **26.32 Tonnes CO₂ / year** ($\sim 1,195$ trees planted equivalent) at $0.70\,\text{kg CO}_2/\text{kWh}$.

---

## 🏛️ Thapar Campus System Parameters

| Parameter | Value |
| :--- | :--- |
| **Institution** | Thapar Institute of Engineering & Technology (TIET), Patiala |
| **Course** | Energy & Environment (UEN008) — Group 4, Section 1A14 |
| **Target Facility (VFD)** | Thapar Auditorium (TAN) |
| **HVAC Load** | 22 kW (30 HP) AHU Centrifugal Blower Motor |
| **Electricity Tariff** | PSPCL Commercial HT Tariff, ₹7.80 / kWh |
| **Grid Carbon Factor** | CEA Northern Grid Factor, 0.70 kg CO₂ / kWh |
| **IoT Edge Node** | `ESP32-THAPAR-CSED-LAB204` on GPIO 14 |
| **IoT Test Location** | CSED Computer Lab 204 |
| **Nominal Voltage Range** | 228.0 V – 232.5 V RMS, 50 Hz |

---

## 🏗️ Repository Architecture

```text
ecopulse-ai/
├── api/
│   ├── iot_telemetry.py        # Sub-second ESP32 & HC-SR501 PIR telemetry API
│   ├── ai_audit.py             # Isolation Forest anomaly detection API
│   └── vfd_analytics.py        # VFD Affinity Law & carbon calculation API
├── public/
│   ├── index.html              # Unified Single-Page Dashboard (Stitch Astra-theme)
│   ├── css/
│   │   └── astra-theme.css     # Glassmorphism, neon glows & dark obsidian theme
│   └── js/
│       └── app.js              # SPA router, live API fetchers & dynamic sliders
├── dev_server.py               # Single-origin local full-stack development server
├── requirements.txt            # Python runtime dependencies
└── vercel.json                 # Vercel serverless routing configuration
```

---

## 🚀 Running the Project

### 1. Local Full-Stack Server
Run the built-in development server (no external dependencies required):
```bash
python dev_server.py
```
Open **`http://localhost:3000`** in your browser.

### 2. Vercel Deployment
Deploy directly to Vercel as a single-origin serverless application:
```bash
vercel deploy --prod
```
