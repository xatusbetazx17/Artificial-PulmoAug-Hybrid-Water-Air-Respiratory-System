# System Overview

Welcome to **Artificial PulmoAug**, the Universal Respiratory Augmentation System. This document describes the high-level architecture, module responsibilities, and data flow.

---

## 1. Architecture Diagram

```text
  [Water]          [Atmosphere]     [Polluted Air]      [High Altitude]
     │                  │                │                    │
     ▼                  ▼                ▼                    ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                    Dual-Mode Controller                    │
  │  (ESP32-S3, sensors: O₂/CO₂/pressure/flow, I²C/SPI buses)   │
  └─────────────────────────────────────────────────────────────┘
     ▲         ▲               ▲               ▲
     │         │               │               │
┌────┴───┐ ┌───┴────┐     ┌────┴─────┐     ┌───┴────────┐
│  Gill  │ │ CCR    │     │ Air      │     │ O₂         │
│ Module │ │ Core   │     │ Booster  │     │ Concentrator│
└────────┘ └────────┘     └──────────┘     └───────────┘
