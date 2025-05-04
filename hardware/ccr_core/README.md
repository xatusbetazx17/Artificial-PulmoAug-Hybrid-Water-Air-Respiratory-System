# CCR Core Module

**Purpose:** Scrub CO₂ and manage the rebreather loop at sea level.

---

## Contents

- `ccr_core.kicad_pro`  
- `CO2_scrubber.sch`  
- `O2_manifold.kicad_pcb`  
- `BOM.csv`  

---

## Key Subsystems

1. **CO₂ Scrubber**  
   - Soda-lime cartridge (100 g)  
   - Pressure relief valve  

2. **O₂ Manifold**  
   - 300 bar cylinder interface  
   - Solenoid-driven demand valve (MS542)  

3. **Sensor Suite**  
   - O₂ partial-pressure sensor (Galvanic cell)  
   - Loop pressure transducer (±2 bar)  

---

## Quick Start

```bash
# In KiCad 7
$ kicad ccr_core.kicad_pro
# Perform ERC → PCB layout → Generate fabrication files
