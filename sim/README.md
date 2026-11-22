# LTspice: pack-swap load switch (LOAD_A -> LOAD_B)

Run: `LTspice.exe -b pack_swap.cir`. Results are in `pack_swap.log`. Open `pack_swap.raw` in LTspice to see the waveforms.

**Setup:** Pack A 7.0 V, Pack B 8.3 V (0.15 ohm internal resistance each). 0.5 A load on VMOT plus C17/C18. LOAD_A turns off at 10 ms, then LOAD_B turns on after a break of `tbreak`, stepped over 0.2 / 0.5 / 1 / 5 ms. The MOSFET models are generic VDMOS fits to the AO3401A and 2N7002 datasheets, not vendor models.

| tbreak | Reverse current B -> A | VMOT minimum during the break | Inrush peak into VMOT |
|---|---|---|---|
| 0.2 ms | **2.4 A (cross-conduction!)** | 6.9 V | 6 A |
| 0.5 ms | 0.4 mA | 2.0 V | 26 A, about 6 us |
| 1 ms | 0.4 mA | about 0 V | 31 A, about 6 us |
| 5 ms | 0.4 mA | 0 V | 31 A, about 6 us |

## Findings
- **Turn-off takes about 0.35 ms.** The 100k gate pull-up has to charge the gates of both PFETs. Turn-on is fast because the 2N7002 pulls the gates down hard.
- **The break-before-make gap must be at least 1 ms.** At 0.2 ms, both switches conduct together and the higher pack dumps about 2.4 A into the lower one. **Keep 5 ms in the firmware** for margin over temperature and part spread.
- **VMOT drops to 0 V during the gap.** The DRV8833 goes into undervoltage lockout and the motors coast for about 5 ms. It recovers on its own (UVLO doesn't latch). The Nano and servo don't notice, because they run from the separate diode-OR + buck rail.
- **Inrush:** about 30 A for about 6 us, which is about 0.0016 A²s. A 3 A fast 1206 fuse needs roughly 0.1 A²s or more to melt, so the fuse won't blow. The simulation has no wiring inductance, so the real peak will be lower. The BMS short-circuit delay (typically 100 us or more) is much longer than this pulse.
