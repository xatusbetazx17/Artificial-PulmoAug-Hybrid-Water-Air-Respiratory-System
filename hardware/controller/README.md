## BOM Snapshot
| Ref  | Item                        | Qty | Details                  |
| ---- | --------------------------- | --- | ------------------------ |
| MEM1 | Polymer separation membrane | 5   | 50 × 50 mm sheets        |
| VAL1 | 3-port solenoid valve       | 2   | 12 V, 1/4″ ports         |
| MCU1 | ESP32-S3 DevKit             | 1   | On-board 3.3 V regulator |

---

## `hardware/controller/README.md`

```markdown
# Dual-Mode Controller

**Purpose:** Central brain that reads sensors, switches modes, and drives pumps/valves.

---

## Contents

- `controller.kicad_pro`  
- `sensor_mux.kicad_pcb`  
- `power_mgmt.sch`  
- `BOM.csv`  

---

## Features

- **MCU:** ESP32-S3 (dual-core, Wi-Fi + Bluetooth)  
- **Sensors:**  
  - O₂ (I²C)  
  - CO₂ (analog)  
  - Pressure (SPI)  
  - Flow (UART)  
- **Power:**  
  - Li-Ion charger (1 cell)  
  - 3.3 V & 5 V regulators  
- **Communications:** USB-C console + CAN bus  

---

## Quick Build

1. Launch KiCad 7 → open `controller.kicad_pro`.  
2. Run ERC → annotate → PcbNew → layout.  
3. Generate BOM (`BOM.csv`) and HTML assembly drawings.  

---

## BOM Preview

| Ref   | Component             | Qty | Footprint            |
|-------|-----------------------|-----|----------------------|
| MCU   | ESP32-S3 WROOM        | 1   | SMD module           |
| REG1  | 3.3 V LDO             | 1   | SOT-223             |
| CHG1  | Li-Ion charger IC     | 1   | QFN-20              |
| MUX1  | 8-channel analog MUX  | 1   | TSSOP-16            |
