"""
EcoPulse AI — VFD Motor Analytics & Carbon Calculator API Endpoint
Target: Thapar Auditorium (TAN) 22 kW (30 HP) AHU Centrifugal Blower Motor
Physics: Centrifugal Affinity Laws for fan/pump systems.
Course: Energy & Environment UEN008, Group 4, Section 1A14
"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Baseline Motor Parameters
RATED_POWER_KW = 22.0
RATED_POWER_HP = 30
MOTOR_TYPE = "AHU Centrifugal Blower"
FACILITY = "Thapar Auditorium (TAN)"

# Operating Parameters
ANNUAL_OPERATING_HOURS = 3500   # Active campus operating hours
FULL_ANNUAL_HOURS = 8760

# Cost & Carbon Parameters
PSPCL_TARIFF = 7.80             # ₹/kWh
CARBON_FACTOR = 0.70            # kg CO₂ per kWh
CARBON_FACTOR_TONNES = 0.0007   # Tonnes CO₂ per kWh

# Normalized Baseline
Q1_RATED = 100.0   # % rated flow
H1_RATED = 100.0   # % rated head
P1_RATED = 100.0   # % rated power


def compute_vfd(speed_pct: float) -> dict:
    """Apply centrifugal Affinity Laws and compute savings."""
    speed_pct = max(0.0, min(100.0, speed_pct))
    n_ratio = speed_pct / 100.0

    # Affinity Laws
    flow_pct = round(Q1_RATED * n_ratio, 2)              # Q ∝ N
    head_pct = round(H1_RATED * (n_ratio ** 2), 2)        # H ∝ N²
    power_pct = round(P1_RATED * (n_ratio ** 3), 2)       # P ∝ N³

    operating_power_kw = round(RATED_POWER_KW * (n_ratio ** 3), 2)
    power_saved_kw = round(RATED_POWER_KW - operating_power_kw, 2)
    energy_reduction_pct = round((1 - (n_ratio ** 3)) * 100, 1)

    annual_energy_saved_kwh = round(power_saved_kw * ANNUAL_OPERATING_HOURS, 1)
    annual_cost_savings_inr = round(annual_energy_saved_kwh * PSPCL_TARIFF, 0)
    annual_co2_avoided_kg = round(annual_energy_saved_kwh * CARBON_FACTOR, 1)
    annual_co2_avoided_tonnes = round(annual_energy_saved_kwh * CARBON_FACTOR_TONNES, 2)

    full_speed_annual_cost = round(RATED_POWER_KW * ANNUAL_OPERATING_HOURS * PSPCL_TARIFF, 0)
    vfd_annual_cost = round(operating_power_kw * ANNUAL_OPERATING_HOURS * PSPCL_TARIFF, 0)
    tree_equivalent = round(annual_co2_avoided_tonnes * 45.4)

    return {
        "facility": FACILITY,
        "asset": f"{RATED_POWER_KW} kW ({RATED_POWER_HP} HP) {MOTOR_TYPE}",
        "input_speed_pct": speed_pct,
        "affinity_laws": {
            "speed_ratio_N2_N1": round(n_ratio, 4),
            "flow_rate_pct": flow_pct,
            "head_pct": head_pct,
            "power_pct": power_pct,
            "formula": "P₂ / P₁ = (N₂ / N₁)³",
        },
        "operating_power_kw": operating_power_kw,
        "rated_power_kw": RATED_POWER_KW,
        "power_saved_kw": power_saved_kw,
        "energy_reduction_pct": energy_reduction_pct,
        "economics": {
            "pspcl_tariff_inr_per_kwh": PSPCL_TARIFF,
            "annual_operating_hours": ANNUAL_OPERATING_HOURS,
            "annual_energy_saved_kwh": annual_energy_saved_kwh,
            "annual_cost_savings_inr": annual_cost_savings_inr,
            "full_speed_annual_cost_inr": full_speed_annual_cost,
            "vfd_annual_cost_inr": vfd_annual_cost,
        },
        "carbon": {
            "grid_carbon_factor_kg_per_kwh": CARBON_FACTOR,
            "annual_co2_avoided_kg": annual_co2_avoided_kg,
            "annual_co2_avoided_tonnes": annual_co2_avoided_tonnes,
            "tree_equivalent": tree_equivalent,
        },
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        try:
            speed = float(params.get("speed", ["80"])[0])
        except (ValueError, TypeError, IndexError):
            speed = 80.0

        payload = compute_vfd(speed)
        body = json.dumps(payload, indent=2)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


if __name__ == "__main__":
    from http.server import HTTPServer
    PORT = 8002
    server = HTTPServer(("0.0.0.0", PORT), handler)
    print(f"VFD Analytics API running at http://localhost:{PORT}/api/vfd?speed=80")
    server.serve_forever()
