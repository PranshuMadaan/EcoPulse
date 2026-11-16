"""
EcoPulse AI — IoT Telemetry API Endpoint
Target: CSED Computer Lab 204, Thapar Institute of Engineering & Technology
Microcontroller: ESP32 Node ESP32-THAPAR-CSED-LAB204
Sensor: HC-SR501 PIR Motion Sensor on GPIO 14
Course: Energy & Environment UEN008, Group 4, Section 1A14
"""

import json
import random
import math
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler

IST = timezone(timedelta(hours=5, minutes=30))

NODE_ID = "ESP32-THAPAR-CSED-LAB204"
BUILDING = "CSED — Computer Science & Engineering Department"
ROOM = "Computer Lab 204"
GPIO_PIN = 14
SENSOR_MODEL = "HC-SR501 PIR Motion Sensor"

SUBCIRCUITS = [
    {"name": "Lighting (LED Panels + Emergency)", "base_current": 4.2, "pf": 0.92},
    {"name": "Desktop PC Racks (42 Stations)", "base_current": 46.5, "pf": 0.85},
    {"name": "HVAC Split Units (4 × 2 TR)", "base_current": 42.8, "pf": 0.88},
]


def generate_telemetry():
    now = datetime.now(IST)
    hour = now.hour

    is_lab_open_hours = 9 <= hour < 17
    motion_detected = (random.random() < 0.65) if is_lab_open_hours else False

    voltage = round(random.uniform(228.0, 232.5), 1)

    circuits = []
    total_current = 0.0
    total_power = 0.0

    for sc in SUBCIRCUITS:
        jitter = random.uniform(0.98, 1.02)
        current = round(sc["base_current"] * jitter, 2)
        active_power = round(voltage * current * sc["pf"], 1)
        apparent_power = round(voltage * current, 1)
        reactive_power = round(math.sqrt(max(apparent_power ** 2 - active_power ** 2, 0)), 1)

        circuits.append({
            "name": sc["name"],
            "current_amps": current,
            "power_factor": sc["pf"],
            "active_power_watts": active_power,
            "apparent_power_va": apparent_power,
            "reactive_power_var": reactive_power,
        })
        total_current += current
        total_power += active_power

    total_current = round(total_current, 2)
    total_power = round(total_power, 1)
    total_power_kw = round(total_power / 1000, 1)

    occupancy_state = "OCCUPIED" if motion_detected else "UNOCCUPIED"

    alerts = []
    if not motion_detected and total_power > 1500:
        alerts.append({
            "severity": "CRITICAL",
            "code": "ECOPULSE-ALERT-001",
            "type": "UNOCCUPIED_DRAIN",
            "title": "CRITICAL UNOCCUPIED DRAIN ALERT",
            "message": f"CRITICAL UNOCCUPIED DRAIN ALERT: {total_power_kw} kW load detected in vacant lab",
            "recommended_action": "Engage BMS smart circuit cutoff for CSED Lab 204. Power down workstation banks & HVAC split units.",
            "financial_impact_per_hour_inr": round(total_power_kw * 7.80, 2),
        })

    return {
        "timestamp": now.isoformat(),
        "node_id": NODE_ID,
        "firmware_version": "3.2.1-tiet",
        "building": BUILDING,
        "room": ROOM,
        "sensor": {
            "model": SENSOR_MODEL,
            "gpio_pin": GPIO_PIN,
            "motion_detected": motion_detected,
            "occupancy_state": occupancy_state,
        },
        "grid": {
            "voltage_v": voltage,
            "frequency_hz": round(random.uniform(49.92, 50.08), 2),
            "tariff_inr_per_kwh": 7.80,
            "utility": "PSPCL (Punjab State Power Corporation Limited)",
        },
        "subcircuits": circuits,
        "totals": {
            "total_current_amps": total_current,
            "total_active_power_watts": total_power,
            "total_active_power_kw": total_power_kw,
        },
        "alerts": alerts,
        "alert_active": len(alerts) > 0,
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        payload = generate_telemetry()
        body = json.dumps(payload, indent=2)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


if __name__ == "__main__":
    from http.server import HTTPServer
    PORT = 8000
    server = HTTPServer(("0.0.0.0", PORT), handler)
    print(f"IoT Telemetry API running at http://localhost:{PORT}/api/iot")
    server.serve_forever()
