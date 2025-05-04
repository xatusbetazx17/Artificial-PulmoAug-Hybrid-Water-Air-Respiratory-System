# Artificial PulmoAug 🌊 – Universal Respiratory Augmentation System

> **⚠️ Experimental concept only. Not a certified life‑support device. Do not attempt human trials.**

---

## 0. Project Goal

Enable seamless, multi‑environment respiration by integrating four core modules:

1. **Artificial Gill** – extract dissolved O₂ from water for underwater breathing.
2. **CCR Core** – closed‑circuit rebreather to recycle exhaled air and supply stored O₂ at sea level.
3. **Air Booster & Purifier** – pressurize, filter, and enrich ambient air (for polluted or high‑altitude environments).
4. **O₂ Concentrator** – generate high‑purity O₂ for extreme altitude or hypoxic conditions.

A **Dual‑Mode Controller** monitors environment (barometric, O₂/CO₂ sensors) and diver workload, then routes gas flows and power between modules.

---

## 1. Repository Layout

```plaintext
ArtificialPulmoAug/
├── docs/                    # White papers, compliance notes, diagrams
├── hardware/                # All hardware designs (KiCad 7)
│   ├── gill_module/         # Membrane cassette + pump housing
│   ├── ccr_core/            # CO₂ scrubber, O₂ manifold & demand valve
│   ├── air_booster/         # Microblower + filter assembly
│   ├── o2_concentrator/     # PSA or membrane stack unit
│   └── controller/          # Power & sensor-manager PCB
├── software/
│   ├── control_app/         # Python GUI & CLI for mode switching & logs
│   ├── simulation/          # Water & gas models + CLI tools
│   │   ├── simulate_flux.py # Underwater O₂-extraction calculator
│   │   └── simulate_gas.py  # Air/compressor/altitude calculator
│   └── firmware/            # ESP32-S3 C/C++ code for controller
├── datasets/                # Lab-collected permeability & test logs
├── tests/                   # Unit tests & hardware-in-loop scripts
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT license text
└── README.md                # You are here
```

---

## 2. Prerequisites

| Tool                       | Version | Purpose                                 |
| -------------------------- | ------- | --------------------------------------- |
| **Python**                 | 3.9 +   | Simulation modules & control app        |
| **pip**                    | latest  | Install dependencies                    |
| **Git**                    | 2.30 +  | Repo cloning & collaboration            |
| *Optional* **Jupyter Lab** | 4 +     | Interactive data exploration & plotting |

macOS/Linux: `brew install python git`
Windows: install **Python** & **Git for Windows** from python.org and git-scm.com.

---

## 3. Get Started (Clone & Bootstrap)

```bash
# 3.1  Clone your repo
$ git clone https://github.com/xatusbetazx17/ArtificialPulmoAug.git
$ cd ArtificialPulmoAug

# 3.2  Create Python virtual environment & activate
$ python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate

# 3.3  Install dependencies
$ pip install -r requirements.txt
```

If no errors appear, move on to **Run & Test** (Section 5).

---

## 4. Automatic Scaffold Generation

To regenerate or bootstrap the entire project structure (directories, scripts, and license), run this once in the empty repo root:

```bash
# 4.1  Create directories
mkdir -p docs \
  hardware/gill_module hardware/ccr_core hardware/air_booster hardware/o2_concentrator hardware/controller \
  software/control_app software/simulation software/firmware datasets tests

# 4.2  requirements.txt
cat > requirements.txt << 'EOF'
numpy~=1.26
matplotlib~=3.9
scipy~=1.13
pyyaml~=6.0
EOF

# 4.3  Underwater CLI (simulate_flux.py)
cat > software/simulation/simulate_flux.py << 'EOF'
#!/usr/bin/env python3
"""CLI: dissolved-O₂ flux for Artificial Gill."""
import argparse, math, textwrap

MG_PER_ML_O2 = 1.429
DEFAULT_WATER_TEMP = 20.0
H0, C, T0 = 1500, 1700, 298.0
O2_MOLAR_MASS = 31.998

def dissolved_o2_mg_per_l(temp_c=DEFAULT_WATER_TEMP):
    t_k = temp_c + 273.15
    henry = H0*math.exp(C*(1/t_k-1/T0))
    conc = (1/henry)*O2_MOLAR_MASS*1000
    return conc

def o2_ml_to_mg(o2_ml): return o2_ml*MG_PER_ML_O2

def calc_required_flow(vo2, o2_mg_l, eff):
    vo2_mg = o2_ml_to_mg(vo2*1000)
    return vo2_mg/(o2_mg_l*eff)

def main():
    p=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Compute water-flow for VO₂ demand.")
    p.add_argument("--temp",type=float,default=20)
    p.add_argument("--vo2",type=float,default=1.2)
    p.add_argument("--eff",type=float,default=0.3)
    args=p.parse_args()
    o2=o2_mg_per_l=args and dissolved_o2_mg_per_l(args.temp)
    flow=calc_required_flow(args.vo2, o2, args.eff)
    print(f"Required H₂O flow: {flow:.1f} L/min")
if __name__=='__main__': main()
EOF
chmod +x software/simulation/simulate_flux.py

# 4.4  Air/Altitude CLI (simulate_gas.py)
cat > software/simulation/simulate_gas.py << 'EOF'
#!/usr/bin/env python3
"""CLI: compute air booster & O₂ needs for altitude."""
import argparse, math

def ambient_pressure(alt_m): return math.exp(-alt_m/7000)

def main():
    p=argparse.ArgumentParser(description="Altitude/compressor/O₂ calculator.")
    p.add_argument("--alt", type=float, default=0)
    p.add_argument("--vo2",type=float,default=1.2)
    p.add_argument("--conc_eff",type=float,default=0.8)
    args=p.parse_args()
    P=ambient_pressure(args.alt)
    boost=max(0,1-P)
    o2_req=args.vo2/args.conc_eff
    print(f"Ambient P: {P:.2f} atm, Pressure boost: {boost:.2f} atm")
    print(f"Pure O₂ flow needed: {o2_req:.2f} L/min")
if __name__=='__main__': main()
EOF
chmod +x software/simulation/simulate_gas.py

# 4.5  MIT LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Marcelo Collado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
EOF
```

---

## 5. Run & Test

1. **Activate venv** & install:

   ```bash
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Underwater mode**:

   ```bash
   python software/simulation/simulate_flux.py --vo2 1.2 --temp 20 --eff 0.3
   ```
3. **Air/Altitude mode**:

   ```bash
   python software/simulation/simulate_gas.py --alt 3000 --vo2 1.2
   ```

---

## 6. Jupyter Notebook (Optional)

In `software/simulation/Gill_Flux_Model.ipynb`, include:

```python
import numpy as np, matplotlib.pyplot as plt
from simulate_flux import dissolved_o2_mg_per_l, calc_required_flow

temps=[5,10,15,20,25]; vo2=1.2
fig,ax=plt.subplots()
for T in temps:
    o2=dissolved_o2_mg_per_l(T)
    eff=np.linspace(0.1,0.8)
    flow=[calc_required_flow(vo2,o2,e) for e in eff]
    ax.plot(eff*100,flow,label=f"{T}°C")
ax.set(xlabel="Efficiency %",ylabel="Flow L/min",title="Flow vs Eff")
ax.legend(); plt.show()
```

---

## 7. Hardware Place‑holders

* `hardware/gill_module/`     – Membrane cassette & pump enclosure designs in STEP/PCB.
* `hardware/ccr_core/`        – CO₂ scrubber + O₂ tank manifold schematics.
* `hardware/air_booster/`     – Microblower + HEPA/carbon filter assembly.
* `hardware/o2_concentrator/` – PSA/membrane stack unit & flow valves.
* `hardware/controller/`      – ESP32‑S3 MCU board, sensor mux, power management.

---

## 8. Roadmap & Contributions

1. **Fork → clone → branch → PR** (`dev`).
2. Run `pytest` & pre‑commit.
3. **2025 Q3** – Bench gill cell & publish permeability data.
4. **2025 Q4** – CCR integration & shallow‑pool trials (no human breathing).
5. **2026**     – Air booster/purifier prototyping & high‑altitude demo.
6. **2027+**   – Full backpack prototype, comprehensive environmental trials.

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

