## BOM Preview

| Ref   | Description                       | Qty | Notes                           |
| ----- | --------------------------------- | --- | ------------------------------- |
| SCR1  | Soda-lime scrubber cartridge      | 1   | Custom canister, 100 g capacity |
| SV1   | MS542 demand-valve solenoid       | 1   | 24 V coil                       |
| SENS1 | O₂ partial-pressure transducer    | 1   | 0–100% O₂ range                 |
| CON1  | 300 bar cylinder quick-disconnect | 1   | DIN 477                         |


---

## `hardware/air_booster/README.md`

```markdown
# Air Booster & Purifier

**Purpose:** Filter and pressurize ambient air for surface and polluted environments.

---

## Contents

- `air_booster.kicad_pro`  
- `filter_stack.step`  
- `blower_driver.sch`  
- `BOM.csv`  

---

## Subsystems

1. **Micro-Blower**  
   - 5 psi max @ 0.5 L/min  
   - Brushless DC motor  

2. **Filter Stack**  
   - HEPA (0.3 µm)  
   - Activated-carbon layer  

3. **Driver Circuit**  
   - MOSFET + buck converter (12 V → 5 V)  
   - PWM speed control via microcontroller  

---

## Assembly Notes

- 3D-print blower housing from `blower_housing.step`.  
- Snap-fit filter cartridges into housing.  
- Solder driver PCB → mount blower → test at 50% PWM.  

---

## BOM Excerpt

| Ref   | Component                      | Qty | Supplier ID       |
|-------|--------------------------------|-----|-------------------|
| BLOW1 | BLDC micro-blower 5 psi        | 1   | NMB06C           |
| HEPA1 | HEPA filter 0.3 µm             | 1   | 3M 2901          |
| CBF1  | Activated-carbon filter sheet  | 1   | Filtrete 1900     |
| M1    | MOSFET IRLZ44N                 | 1   | IRLZ44N          |
