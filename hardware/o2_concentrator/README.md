# O₂ Concentrator

**Purpose:** Produce high-purity O₂ via Pressure-Swing Adsorption or membrane separation.

---

## Contents

- `o2_concentrator.kicad_pro`  
- `membrane_stack.step`  
- `valve_control.sch`  
- `BOM.csv`  

---

## Subsystems

1. **Membrane Stack**  
   - 5 × polymer membranes in series  
   - Flow capacity: 1 L/min  

2. **Solenoid Valves**  
   - Two 3-port valves for feed/purge cycles  
   - Controlled by PWM on MCU  

3. **Support Structure**  
   - 3D-printed manifold in `manifold.step`  

---

## Getting Started

```bash
# Open KiCad project
$ kicad o2_concentrator.kicad_pro
# Validate schematic → layout → export Gerbers
