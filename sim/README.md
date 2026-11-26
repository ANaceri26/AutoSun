# Tests: does the board work, and is it safe?

Everything here can be re-run. The LTspice tests run with `LTspice.exe -b <file>.cir`, and results land in `<file>.log`. The stress check runs with KiCad's Python: `"C:\Program Files\KiCad\10.0\bin\python.exe" sim\design_check.py`.

## 1. Battery swap switch (`pack_swap.cir`)
LOAD_A turns off, then LOAD_B turns on after a pause. Pack A is 7.0 V, pack B is 8.3 V.

| Pause | Current from pack B into pack A | Verdict |
|---|---|---|
| 0.2 ms | **2.4 A**: both switches on at once | ❌ |
| 0.5 ms or more | 0.4 mA (leakage) | ✅ |

- A switch takes **0.35 ms** to turn off, so the code uses a **5 ms** pause.
- The surge when a pack connects is about 30 A for about 6 µs. That's far too short to blow the 3 A fuse.

## 2. I2C level shifter, Arduino ⇄ XIAO (`i2c_level_shifter.cir`)
BSS138 + pull-ups, tested both directions: Arduino talking and XIAO talking. BSS138 threshold tested at 0.8 V and 1.6 V (the datasheet range).

| Pull-ups | Bus capacitance | Worst rise time | Limit (100 kHz) | Verdict |
|---|---|---|---|---|
| **4.7k (used on the board)** | 30 pF (realistic) | **198 ns** | 1000 ns | ✅ (also fine at 400 kHz) |
| **4.7k (used on the board)** | 100 pF (pessimistic) | **521 ns** | 1000 ns | ✅ |
| 10k (first design) | 100 pF | 1112 ns | 1000 ns | ❌, so I changed to 4.7k |

- Logic 0 is **0.02 V** on both sides, and logic 1 is **3.30 V** on the XIAO side and **5.00 V** on the Arduino side.
- **The XIAO side never goes above 3.30 V**, so the XIAO is protected.

## 3. XIAO power diode D5 (`xiao_power_path.cir`)
| Case | XIAO voltage | Current back into the car | Verdict |
|---|---|---|---|
| Car on, no USB (Wi-Fi peak 0.35 A) | 4.69 V min | — | ✅ |
| Car off, USB plugged into the XIAO | 4.89 V | 0.025 mA (leakage) | ✅ the USB can't power the car |
| Both on | 4.89 V (from USB) | none | ✅ no fight |

## 4. Stress check on the real board file (`design_check.py` → `design_check_results.md`)
- **Voltage:** every chip, transistor, diode and capacitor is inside its datasheet maximum with the real wiring. **Result: PASS.**
- **Never wire all 4 solar panels in a row** (about 28 V). That puts the charger chip right at its 30 V limit. Always use 2 pairs (about 14 V).
- **Copper vs current:** every power track carries its worst-case current with **less than 10 °C of warming**. After this check I widened the battery, 5 V-chip and motor-power tracks, and made the main 5 V trunk 1.0 mm.
- **+5V, calculated piece by piece:** the copper is solved as a network of tiny resistors, at full worst-case load (servo stall 1.2 A + XIAO Wi-Fi 0.35 A + Arduino + sensors = 1.63 A). **No piece is over its limit.** The tightest are two stubs, 0.1 mm and 0.5 mm long, at a via. The drop from the 5 V chip to the furthest part is only about 70 mV.
- **Result: `ALL CHECKS PASS - every row green`** (see `design_check_results.md`).
- **Resistor power:** all inside their ratings. R3 reaches 80% of its rating only during full-speed USB-C charging.

## What simulation can't cover
There are no LTspice models for the CN3722 charger, the TPS563201 5 V chip or the DRV8833. For those, the parts and values follow each **datasheet's recommended circuit**, and the layout follows each datasheet's layout rules. The real test is the first power-up: see `docs/first_power_up.md`.
