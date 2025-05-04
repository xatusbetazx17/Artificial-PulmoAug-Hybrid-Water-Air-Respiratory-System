
---

## `hardware/gill_module/README.md`

```markdown
# Gill Module

**Purpose:** Harvest dissolved O₂ from water to feed the diver in underwater mode.

---

## Contents

1. **KiCad Project** (`gill_module.kicad_pro`)  
2. **PCB Layout** (`gill_module.kicad_pcb`)  
3. **3D Model** (`gill_module_drawing.step`)  
4. **BOM** (`BOM.csv`)

---

## Design Highlights

- **Membrane cassette:**  
  - 100 cm² silicone–MOF sandwich layers  
  - Removable housing for membrane replacement  

- **Pump driver PCB:**  
  - STM32F0 microcontroller  
  - DRV8316-controlled BLDC impeller (0.5 L/min max)  
  - Flow-rate sensor interface (I²C)  

---

## Opening the Project

1. Install KiCad 7.  
2. Open `gill_module.kicad_pro`.  
3. Inspect schematic (Pump/MCU) → annotate → run ERC.  
4. Switch to PCB editor → DRC check → generate Gerber outputs.  

---

## BOM Overview (`BOM.csv`)

| Ref  | Description               | Qty | Footprint           | Supplier Part #      |
|------|---------------------------|-----|---------------------|----------------------|
| U1   | STM32F042K6T6 micro-MCU   | 1   | LQFP48              | STM32F042K6T6TR      |
| U2   | DRV8316 BLDC driver       | 1   | HTSSOP36            | DRV8316PWPR          |
| F1   | Silicone/MOF membrane     | 1   | Custom (100 × 50 mm) | In-house             |
| J1   | 2 × 4 Pin Molex connector | 1   | Molex PicoBlade     | 50394-0800           |
