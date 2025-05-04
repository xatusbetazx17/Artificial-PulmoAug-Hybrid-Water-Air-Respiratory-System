#!/usr/bin/env python3
"""
simulate_gas.py

CLI tool to compute required air pressure boost and pure O₂ flow
for high-altitude or low-oxygen environments.
"""
import argparse
import math

def ambient_pressure_at_altitude(altitude_m: float) -> float:
    """
    Approximate ambient pressure (atm) at a given altitude (m).
    Uses an exponential model with scale height ~7000 m.
    """
    return math.exp(-altitude_m / 7000.0)

def main():
    parser = argparse.ArgumentParser(
        description="Compute compressor boost & O₂ needs at altitude."
    )
    parser.add_argument("--alt", type=float, default=0.0,
                        help="Altitude in meters (default: 0)")
    parser.add_argument("--vo2", type=float, default=1.2,
                        help="Metabolic O₂ demand in L/min (default: 1.2)")
    parser.add_argument("--conc_eff", type=float, default=0.8,
                        help="O₂ concentrator efficiency (0–1, default: 0.8)")
    args = parser.parse_args()

    pressure_atm = ambient_pressure_at_altitude(args.alt)
    pressure_boost = max(0.0, 1.0 - pressure_atm)
    pure_o2_flow = args.vo2 / args.conc_eff

    print("\n--- ArtificialPulmoAug Air/Altitude Mode ---")
    print(f"Altitude         : {args.alt:.0f} m")
    print(f"Ambient P        : {pressure_atm:.2f} atm")
    print(f"Pressure boost   : {pressure_boost:.2f} atm")
    print(f"Pure O₂ required : {pure_o2_flow:.2f} L/min\n")

if __name__ == "__main__":
    main()
