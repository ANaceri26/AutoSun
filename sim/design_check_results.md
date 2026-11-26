
## 1) Voltage vs rating

Part | Where | Worst-case V | Rating V | Margin | OK?
--- | --- | --- | --- | --- | ---
U1 CN3722 | VCC pin | 15.0 | 30.0 | 2.0x | ✅
U1 CN3722 | BAT/CSP pins | 9.0 | 28.0 | 3.1x | ✅
U1 CN3722 | CHRG/DONE pins | 5.1 | 30.0 | 5.9x | ✅
Q1 AO3407A | drain-source | 15.0 | 30.0 | 2.0x | ✅
Q1 AO3407A | gate (charger clamps it to 8 V) | 8.0 | 20.0 | 2.5x | ✅
D1/D2 SS34 | reverse voltage | 15.0 | 40.0 | 2.7x | ✅
D3/D4 SS34 | reverse voltage | 8.4 | 40.0 | 4.8x | ✅
Q2-Q12 AO3401A | drain-source | 8.4 | 30.0 | 3.6x | ✅
Q2-Q12 AO3401A | gate-source (= pack or charger V) | 9.0 | 12.0 | 1.3x | ✅
Q4-Q13 2N7002 | drain-source | 8.4 | 60.0 | 7.1x | ✅
Q4-Q13 2N7002 | gate (Arduino pin) | 5.1 | 20.0 | 3.9x | ✅
U2 TPS563201 | VIN | 8.4 | 17.0 | 2.0x | ✅
U3 DRV8833 | VM | 8.4 | 11.8 | 1.4x | ✅
U3 DRV8833 | logic inputs | 5.1 | 7.0 | 1.4x | ✅
A1 Nano Every | 5V pin (regulated 5.0 V) | 5.1 | 6.0 | 1.2x | ✅ (regulated rail)
A1 Nano Every | A0/A1 pin (full pack x0.5; reads up to 5.0 V, damage above 5.5 V) | 4.2 | 5.5 | 1.3x | ✅
A1 Nano Every | A2 pin (solar x0.175) | 2.6 | 5.0 | 1.9x | ✅
U6 XIAO | 5V pin (after D5) | 4.8 | 5.5 | 1.1x | ✅ (regulated rail)
U6 XIAO | SDA/SCL (pulled to its own 3.3 V) | 3.3 | 3.6 | 1.1x | ✅ (regulated rail)
Q14/Q15 BSS138 | drain-source | 5.1 | 50.0 | 9.8x | ✅
Q14/Q15 BSS138 | gate-source | 3.3 | 20.0 | 6.1x | ✅ (regulated rail)
C1/C2/C3 (50 V) | capacitor | 15.0 | 50.0 | 3.3x | ✅
C4/C5 (50 V) | capacitor | 9.0 | 50.0 | 5.6x | ✅
C12/C13 (50 V) | capacitor | 8.4 | 50.0 | 6.0x | ✅
C15/C16/C21 (25 V) | capacitor | 5.1 | 25.0 | 4.9x | ✅ (regulated rail)
C17/C18 (50 V) | capacitor | 8.4 | 50.0 | 6.0x | ✅

Mis-wiring check: all 4 panels in a row (~28 V) would put the CN3722 VCC at 28/30 V and Q1 at 28/30 V: at the limit. **Always wire 2 pairs.**

## 2) Thinnest track vs worst-case current (1 oz copper)

Net | Worst-case A | Thinnest track mm | Carries @10°C rise | Carries @20°C rise | OK?
--- | --- | --- | --- | --- | ---
/PACKA+ | 2.0 | 1.00 | 2.39 A | 3.24 A | ✅
/PACKB+ | 2.0 | 1.00 | 2.39 A | 3.24 A | ✅
/PACKA_F | 2.0 | 1.00 | 2.39 A | 3.24 A | ✅
/PACKB_F | 2.0 | 1.00 | 2.39 A | 3.24 A | ✅
/S_LA | 1.6 | 0.60 | 1.65 A | 2.24 A | ✅
/S_LB | 1.6 | 0.60 | 1.65 A | 2.24 A | ✅
/S_CA | 1.0 | 1.00 | 2.39 A | 3.24 A | ✅
/S_CB | 1.0 | 0.60 | 1.65 A | 2.24 A | ✅
/VMOT | 1.2 | 0.40 | 1.23 A | 1.67 A | ✅
/MA1 | 0.6 | 0.30 | 1.00 A | 1.36 A | ✅
/MA2 | 0.6 | 0.30 | 1.00 A | 1.36 A | ✅
/MB1 | 0.6 | 0.40 | 1.23 A | 1.67 A | ✅
/MB2 | 0.6 | 0.30 | 1.00 A | 1.36 A | ✅
/ISENA | 0.6 | 0.24 | 0.85 A | 1.15 A | ✅
/ISENB | 0.6 | 0.40 | 1.23 A | 1.67 A | ✅
/VCHG | 1.0 | 0.30 | 1.00 A | 1.36 A | ✅ (only 0.9 mm long, at chip pins)
/CN_CSP | 1.2 | 0.30 | 1.00 A | 1.36 A | ✅ (only 1.4 mm long, at chip pins)
/CN_SW | 1.2 | 1.00 | 2.39 A | 3.24 A | ✅
/VSOL | 0.8 | 0.30 | 1.00 A | 1.36 A | ✅
/SOL+ | 0.8 | 0.75 | 1.94 A | 2.63 A | ✅
/VOR | 1.4 | 1.00 | 2.39 A | 3.24 A | ✅
/VIN_BUCK | 1.4 | 0.60 | 1.65 A | 2.24 A | ✅
/BUCK_SW | 1.66 | 0.70 | 1.85 A | 2.51 A | ✅
/XIAO_5V | 0.4 | 0.19 | 0.71 A | 0.96 A | ✅
/3V3_X | 0.01 | 0.25 | 0.88 A | 1.19 A | ✅

## 2b) +5V: real worst-case current in every piece of copper (servo stall 1.2 A + XIAO 0.35 A + Arduino + sensors + LEDs = 1.63 A)

Pieces of copper | Total load | Tightest piece: current | Its width | It can carry @10°C rise | Load vs limit | Pieces over the limit | OK?
--- | --- | --- | --- | --- | --- | --- | ---
74 | 1.63 A | 1.63 A | 0.60 mm | 1.65 A | 99% | 0 | ✅

Tightest pieces (over 85% of their 10°C limit), board coordinates in mm from the bottom-left corner:
- 1.63 A in 0.60 mm wide, 0.1 mm long, F.Cu, (24.3,17.9)->(24.3,17.8) = 99% of limit
- 1.63 A in 0.60 mm wide, 0.5 mm long, F.Cu, (24.7,17.8)->(24.3,17.8) = 99% of limit
- 1.63 A in 0.70 mm wide, 2.5 mm long, F.Cu, (26.5,16.0)->(24.7,17.8) = 89% of limit

Voltage drop from the 5 V chip to the furthest part at full load: 67 mV

## 3) Resistor power

Part | Current | Power | Rating | OK?
--- | --- | --- | --- | ---
R3 0.2 Ω charge sense (full 1 A, USB-C charging) | 1 A | 200 mW | 250 mW | ✅
R3 on solar (~0.4 A) | 0.4 A | 32 mW | 250 mW | ✅
R32/R33 0.33 Ω motor sense (0.6 A limit) | 0.6 A | 119 mW | 250 mW | ✅
R35-R38 4.7k pull-ups | 0.00106 A | 5 mW | 100 mW | ✅

RESULT: ALL CHECKS PASS - every row green
