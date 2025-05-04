#!/usr/bin/env python3
"""
control_app.py

Unified CLI to switch between underwater (gill) and air/altitude modes.
"""
import argparse
import os
import sys

# allow importing from simulation folder
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "simulation")))

from simulate_flux import dissolved_o2_mg_per_l, required_water_flow
from simulate_gas import ambient_pressure_at_altitude

def cmd_gill(args):
    o2_conc = dissolved_o2_mg_per_l(args.temp)
    flow = required_water_flow(args.vo2, o2_conc, args.eff)
    print("--- Underwater Gill Mode ---")
    print(f"Water temp       : {args.temp:.1f} °C")
    print(f"Dissolved O₂     : {o2_conc:.1f} mg/L")
    print(f"VO₂ demand       : {args.vo2:.2f} L/min")
    print(f"Efficiency       : {args.eff * 100:.0f} %")
    print(f"Required water   : {flow:.1f} L/min")

def cmd_air(args):
    p = ambient_pressure_at_altitude(args.alt)
    boost = max(0.0, 1.0 - p)
    pure_flow = args.vo2 / args.conc_eff
    print("--- Air / Altitude Mode ---")
    print(f"Altitude         : {args.alt:.0f} m")
    print(f"Ambient P        : {p:.2f} atm")
    print(f"Pressure boost   : {boost:.2f} atm")
    print(f"Pure O₂ required : {pure_flow:.2f} L/min")

def main():
    parser = argparse.ArgumentParser(
        description="Artificial PulmoAug Control CLI"
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    gill = sub.add_parser("gill", help="Underwater O₂-extraction mode")
    gill.add_argument("--temp", type=float, default=20.0, help="Water temp °C")
    gill.add_argument("--vo2", type=float, default=1.2, help="VO₂ demand L/min")
    gill.add_argument("--eff", type=float, default=0.3, help="Gill efficiency 0–1")
    gill.set_defaults(func=cmd_gill)

    air = sub.add_parser("air", help="Air / altitude mode")
    air.add_argument("--alt", type=float, default=0.0, help="Altitude (m)")
    air.add_argument("--vo2", type=float, default=1.2, help="VO₂ demand L/min")
    air.add_argument("--conc_eff", type=float, default=0.8,
                     help="Concentrator efficiency 0–1")
    air.set_defaults(func=cmd_air)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
