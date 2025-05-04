#!/usr/bin/env python3
"""
simulate_flux.py

CLI tool to compute how much water flow (L/min) you need to 
meet a diver’s O₂ demand via an artificial gill.
"""
import argparse
import math

MG_PER_ML_O2 = 1.429         # mg O₂ per mL of gas at STP
DEFAULT_TEMP_C = 20.0        # °C
HENRY_H0 = 1500.0            # reference Henry’s constant @ 298 K (atm·L/mol)
HENRY_C = 1700.0             # temperature coefficient
HENRY_T0 = 298.0             # reference temperature (K)
O2_MOLAR_MASS = 31.998       # g/mol

def dissolved_o2_mg_per_l(temp_c: float = DEFAULT_TEMP_C) -> float:
    """
    Calculate dissolved O₂ concentration in mg/L at 1 atm partial pressure 
    for a given water temperature (°C), via Henry's law.
    """
    temp_k = temp_c + 273.15
    henry_constant = HENRY_H0 * math.exp(HENRY_C * (1/temp_k - 1/HENRY_T0))
    # mol/L = P (1 atm) / H (atm·L/mol)
    conc_mol_per_l = 1.0 / henry_constant
    # mg/L = mol/L * molar_mass (g/mol) * 1000 (mg/g)
    return conc_mol_per_l * O2_MOLAR_MASS * 1000.0

def required_water_flow(
    vo2_l_per_min: float,
    o2_mg_per_l: float,
    capture_efficiency: float
) -> float:
    """
    Compute L/min of water needed to supply vo2_l_per_min liters O₂ per minute,
    given dissolved concentration (mg/L) and membrane capture efficiency [0–1].
    """
    # convert L O₂ → mL → mg
    o2_mg_per_min = vo2_l_per_min * 1000.0 * MG_PER_ML_O2
    # mg captured per L water
    mg_per_l_captured = o2_mg_per_l * capture_efficiency
    if mg_per_l_captured <= 0:
        raise ValueError("Dissolved O₂ or efficiency must be > 0")
    return o2_mg_per_min / mg_per_l_captured

def main():
    parser = argparse.ArgumentParser(
        description="Compute required water flow for artificial gill O₂ supply."
    )
    parser.add_argument("--temp", type=float, default=DEFAULT_TEMP_C,
                        help="Water temperature in °C (default: 20)")
    parser.add_argument("--vo2", type=float, default=1.2,
                        help="Metabolic O₂ demand in L/min (e.g. rest≈0.5, swim≈1.2)")
    parser.add_argument("--eff", type=float, default=0.3,
                        help="Gill capture efficiency (0–1, default: 0.3)")
    args = parser.parse_args()

    o2_conc = dissolved_o2_mg_per_l(args.temp)
    flow = required_water_flow(args.vo2, o2_conc, args.eff)
    print("\n--- ArtificialPulmoAug Underwater Mode ---")
    print(f"Water temp       : {args.temp:.1f} °C")
    print(f"Dissolved O₂     : {o2_conc:.1f} mg/L")
    print(f"VO₂ demand       : {args.vo2:.2f} L/min")
    print(f"Efficiency       : {args.eff * 100:.0f} %")
    print(f"Required flow    : {flow:.1f} L/min\n")

if __name__ == "__main__":
    main()
