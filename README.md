# AutoSun: Solar RC Car Board

One circuit board that runs a small solar-powered RC car. It charges the batteries from solar panels, swaps between two battery packs on its own, drives two rear motors and a steering servo, and holds an Arduino Nano Every as the brain.

![Board top view](builds/A_full_assembly/preview_top.png)

## What the board does
- **Solar charging:** 4 small panels, wired as two pairs, charge the batteries, getting as much power from the sun as they can.
- **Two battery packs:** one drives the car while the other charges. The board switches between them automatically.
- **5 V supply:** powers the Arduino, the servo and the sensors. It stays on during a battery swap, so the Arduino never restarts.
- **Motor driver:** runs the left and right rear motors, with a built-in current limit so they can't be overloaded.
- **Plug-in spots:** steering servo, ultrasonic distance sensor, IR remote receiver, and a spare I2C port.
- **Phone control (Wi-Fi):** a spot for a XIAO ESP32-S3, with a built-in 3.3 V ↔ 5 V level shifter, so a phone can drive the car and show live battery and solar data. See `docs/phone_dashboard_plan.md`.
- **Plugs:** JST-PH 2.0 for the solar panels, both battery packs and both motors.

## Folders
| Where | What's in it |
|---|---|
| `solar_car.kicad_pro` | The KiCad 10 project. Open this to see the circuit and the board. |
| `builds/A_full_assembly/` | **Version A, ready to order:** the factory builds and solders everything except the Arduino and pin headers. Upload `gerbers_upload_this.zip`, `BOM_JLCPCB.csv` and `CPL_JLCPCB.csv`. |
| `builds/B_own_modules/` | **Version B (dropped, kept for reference only):** same board, but it uses my own red DRV8833 motor module and MP1584 5 V module instead of factory-soldered chips. Cheaper, with a bit more soldering. Same 3 files to upload. Its KiCad project is in `kicad/`. |
| `mechanical/` | For the car body: 3D models (STEP) and AutoCAD drawings (DXF), plus a sheet with every size, hole position and height. |
| `docs/` | The phone dashboard plan, and **first power-up steps** (follow these when the board arrives). |
| `sim/` | Tests: LTspice simulations (battery swap, level shifter, XIAO power) and a voltage/current stress check of the whole board. All pass. |
| `schematic_preview.png` | A quick picture of the circuit. |

The build folder has `YOU_SOLDER_THESE.csv` listing what you solder yourself: the Arduino, the XIAO and the pin headers.

## Board legend
Every plug, what goes in it, and which pin is +: see `board_legend.png` in each build folder.

## Winter charging (USB-C, no sun)
No board change needed. You make a small adapter cable instead of using the solar panels:

1. Get a **USB-C PD trigger board that outputs a fixed 12 V** (a few dollars). Fixed 12 V boards can't be set wrong. On adjustable ones, 5 V or 9 V just won't charge (simulated in `sim/charging_inputs.cir`).
2. Solder its output to a female JST-PH cable: **red to +, black to −**.
3. Unplug the solar panels from **J1** and plug the adapter in. On J1, the **left pin is +**.
4. Plug a USB-C power bank or wall charger into the trigger board. It must support USB-C PD at **12 V** (look for "12V" in its output specs; some only do 5 V and 9 V).
5. **Switch the car ON** with the main switch. The Arduino decides which pack charges, so nothing charges while it's off.

The charger then runs at its full rate (about 1 A), so a drained pack fills in about 2–3 hours. If + and − are swapped by mistake, the input diode blocks it: nothing breaks, it just won't charge.

## Open it
Install [KiCad 10](https://www.kicad.org/), then open `solar_car.kicad_pro`. In the board view, press `Alt+3` for 3D.

## Status
The board is fully laid out, passes KiCad's design checks, and every part has a JLCPCB part number. **Not ordered yet.**

Next up: write the Arduino code (driving, battery swap, IR remote, and self-driving with the ultrasonic sensor).
