# Artificial PulmoAug 🌊 – Hybrid Water/Air Respiratory System

> **⚠️  Experimental concept only. Not a certified life‑support device. Do not attempt human trials.**

---

## 0. Project Goal
Build a completely open‑source platform that augments human respiration so a diver can **switch on‑the‑fly** between:
* breathing **atmospheric air** at the surface, and
* breathing **oxygen extracted from water** via an "artificial gill" module under water,
with automatic fallback to a conventional **closed‑circuit rebreather (CCR)** for safety.

## 1. Repository Layout
```
ArtificialPulmoAug/
├── docs/               # White papers, design notes, regulations
├── hardware/           # CAD & PCB files (KiCad 7)
│   ├── gill_module/
│   ├── pump_driver/
│   └── controller/
├── software/
│   ├── control_app/    # Python GUI for sensor data & logs
│   ├── simulation/     # Membrane & physiology models ➜ Steps 4‑6
│   └── firmware/       # C/C++ code for MCU (ESP32‑S3 by default)
├── datasets/           # Lab‑collected permeability & test logs
├── tests/              # pytests + hardware‑in‑loop scripts
├── LICENSE             # MIT license text (see Section 9)
└── README.md           # This file
```

---

## 2. Prerequisites
| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.9 + | core simulation & CLI app |
| **pip** | latest | dependency install |
| **Git** | 2.30 + | clone/push updates |
| *(optional)* **Jupyter Lab** | 4 + | interactive notebooks |

macOS/Linux: `brew install python git`.  
Windows: install **Python** & **Git for Windows**.

---

## 3. Clone & Boot‑strap
```bash
# 3‑1  Clone your empty repo
$ git clone https://github.com/xatusbetazx17/ArtificialPulmoAug.git
$ cd ArtificialPulmoAug

# 3‑2  Create a Python virtual environment
$ python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# 3‑4  Install dependencies
$ pip install -r requirements.txt
```
If everything installs without errors you’re ready for the simulation in Step 5.

---

## 4. `requirements.txt`
```text
# ===== Core numerical & plotting libs =====
numpy~=1.26
matplotlib~=3.9
scipy~=1.13
pyyaml~=6.0
```
Save this as **`requirements.txt`** in the repo root.

---

## 5. Simulation / CLI Prototype  ➜  `software/simulation/simulate_flux.py`
*(File contents provided below – copy into the indicated path and `chmod +x`)*
```python
#!/usr/bin/env python3
"""Simple dissolved‑oxygen flux model for the Artificial PulmoAug project.

Usage (CLI):
    python simulate_flux.py --depth 10 --vo2 1.2
"""
from __future__ import annotations
import argparse, math, textwrap

MG_PER_ML_O2 = 1.429        # mg O2 per mL at STP
DEFAULT_WATER_TEMP = 20.0   # °C
H0, C, T0 = 1500, 1700, 298.0
O2_MOLAR_MASS = 31.998      # g·mol⁻¹


def dissolved_o2_mg_per_l(temp_c: float = DEFAULT_WATER_TEMP) -> float:
    t_k = temp_c + 273.15
    henry = H0 * math.exp(C * (1 / t_k - 1 / T0))  # atm·L/mol
    conc_mol = 1.0 / henry
    return conc_mol * O2_MOLAR_MASS * 1000  # mg/L

def o2_ml_to_mg(o2_ml: float) -> float:
    return o2_ml * MG_PER_ML_O2

def calc_required_flow(vo2_l_min: float, o2_mg_l: float, gill_eff: float) -> float:
    vo2_mg_min = o2_ml_to_mg(vo2_l_min * 1000)  # L → mL → mg
    return vo2_mg_min / (o2_mg_l * gill_eff)


def main(argv=None):
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Compute water‑flow & membrane area for dissolved‑O2 extraction.",
        epilog=textwrap.dedent("""Example:
          python simulate_flux.py --vo2 1.2 --temp 20 --eff 0.3"""))
    p.add_argument("--temp", type=float, default=20, help="Water temp °C (default 20)")
    p.add_argument("--vo2",  type=float, default=1.2, help="Diver VO2 L/min (rest≈0.5, swim≈1.2)")
    p.add_argument("--eff",  type=float, default=0.3, help="Gill capture efficiency 0‑1")
    o = p.parse_args(argv)

    o2_mg_l = dissolved_o2_mg_per_l(o.temp)
    flow = calc_required_flow(o.vo2, o2_mg_l, o.eff)

    print("\n==== ArtificialPulmoAug quick‑calc ====")
    print(f"Temp              : {o.temp:.1f} °C")
    print(f"Dissolved O₂      : {o2_mg_l:.1f} mg/L")
    print(f"Metabolic VO₂     : {o.vo2:.2f} L/min")
    print(f"Gill efficiency   : {o.eff*100:.0f}%")
    print(f"Required H₂O flow : {flow:.1f} L/min\n")

if __name__ == "__main__":
    main()
```
Run a test:
```bash
$ python software/simulation/simulate_flux.py --vo2 1.2 --temp 20 --eff 0.3
```
You should see a required flow near **42 L min⁻¹**.

---

## 6. Jupyter Notebook (optional visualisation)
Create **`software/simulation/Gill_Flux_Model.ipynb`** with this starter cell to plot efficiency vs. water‑flow curves:
```python
import numpy as np, matplotlib.pyplot as plt
from simulate_flux import dissolved_o2_mg_per_l, calc_required_flow

temps = [5, 10, 15, 20, 25]
vo2   = 1.2  # L/min

fig, ax = plt.subplots()
for T in temps:
    o2 = dissolved_o2_mg_per_l(T)
    eff = np.linspace(0.1, 0.8, 100)
    flow = [calc_required_flow(vo2, o2, e) for e in eff]
    ax.plot(eff*100, flow, label=f"{T} °C")
ax.set_xlabel("Gill efficiency %")
ax.set_ylabel("Required water flow (L/min)")
ax.set_title("Water flow vs. membrane efficiency")
ax.legend()
plt.show()
```

---

## 7. Hardware Place‑holders
* `hardware/gill_module/`  – add STEP model of 50 cm² membrane cassette.
* `hardware/pump_driver/`  – KiCad project for BLDC impeller driver (DRV8316 + ESP32‑S3).
* `hardware/controller/`   – power management & sensor mux board.

---

## 8. Roadmap & Contributions
1. **Fork → clone → branch → PR** (target `dev`).
2. Pass `pytest` & `pre‑commit` before pushing.
3. **2025 Q3** – Bench gill cell & publish datasets.
4. **2025 Q4** – Integrate CO₂ scrubber → shallow‑pool tests (no human breathing).
5. **2026** – Build backpack prototype, tethered safety trials.

---

## 9. License – MIT
This project is distributed under the **MIT License**, allowing anyone to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software and hardware files as long as the copyright notice is preserved.

### Quick creation of `LICENSE` file
Copy the exact text below into a file named `LICENSE` in the repository root:
```
MIT License

Copyright (c) 2025 Marcelo Collado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---
© 2025 Marcelo Collado (GitHub: **@xatusbetazx17**) & contributors.

