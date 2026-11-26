# Plan: phone control + live dashboard (XIAO ESP32-S3 add-on)

**Goal:** drive the car from your phone and see live battery and solar data, without changing the PCB.

## How it fits together
```
 Phone (Wi-Fi)  ⇄  XIAO ESP32-S3  ⇄  level shifter  ⇄  J10 on the board  ⇄  Nano Every (car brain)
                   "the radio"         3.3V ↔ 5V        GND,5V,SDA,SCL       motors, servo, sensors, packs
```
- **The Nano Every stays in charge of the car:** motors, steering, battery swapping, sensors. If Wi-Fi drops, the car still works and stops safely.
- **The XIAO ESP32-S3 is only the radio and the web page.** It makes its own Wi-Fi network called `AutoSUN`, and your phone opens a page with a joystick and live numbers. Nothing to install.

## Parts
| Part | Why | Have it? |
|---|---|---|
| XIAO ESP32-S3 | Wi-Fi and the web page | ✅ |
| **4-channel level shifter (BSS138 type)**, about $1–2 | The XIAO is 3.3 V and the Nano is 5 V. Wiring them directly could kill the XIAO. | ❌ buy |
| 4 female jumper wires | J10 → level shifter → XIAO | ✅ |
| *Optional:* INA219 current sensor | Real current (amps) for the dashboard; shares the same 2 wires | — |

## Wiring
| J10 pin (board) | Level shifter | XIAO ESP32-S3 |
|---|---|---|
| 5V | HV | **5V** pin (powers the XIAO) |
| GND | GND (both sides) | GND |
| — | LV | **3V3** pin |
| SDA (Nano A4) | HV1 ⇄ LV1 | **D4 (SDA)** |
| SCL (Nano A5) | HV2 ⇄ LV2 | **D5 (SCL)** |

⚠️ **Don't plug USB into the XIAO while the car is switched on.** The USB power and the car's 5 V would fight each other. Switch the car off first, or upload the XIAO's code with it unplugged from J10.

## What travels between them (about 10 times a second)
**Nano → XIAO (status)**
- Pack A voltage, pack B voltage, solar voltage
- Which pack is driving and which is charging; charge-done status
- Motor driver fault, ultrasonic distance
- Mode (manual / self-driving / stopped), current speed and steering

**XIAO → Nano (commands)**
- Mode, throttle (−100…100), steering (−100…100), plus a "still connected" counter

**Safety rule:** in manual mode, if the Nano hears nothing from the XIAO for **0.5 s**, it stops the motors.

## The phone page
- 🕹️ **Joystick**: up/down = speed, left/right = steering (the servo stays in its limited range)
- 🔋 **Battery % for A and B**, worked out from voltage (about 6.6 V = empty, 8.3 V = full), smoothed so it doesn't jump around while driving
- 🔄 Which pack is **driving** and which is **charging**, plus a charge-done light
- ☀️ Solar voltage, and whether it's charging (or "USB charging" in winter)
- 📏 Distance to the nearest obstacle
- Buttons: **Manual / Self-driving / STOP**
- Range: about 20–30 m in the open

## Build order (one step at a time, each one tested)
1. **Bench test, no car:** wire the Nano + level shifter + XIAO on the desk and make them pass test numbers back and forth.
2. **Web page with fake data:** the XIAO shows the dashboard on your phone.
3. **Real data:** the Nano sends real battery and solar readings, and the dashboard shows them.
4. **Drive from the phone:** joystick → motors and steering, with the 0.5 s safety stop.
5. **Self-driving toggle:** switch between phone control and ultrasonic obstacle-avoiding.
6. *Optional:* add the INA219 for real current and an energy estimate.

## Notes
- Steps 1–2 can start **now**, before the PCB arrives: you only need the Nano, the XIAO and the level shifter on the desk.
- On the Nano, the right motor's speed has to come from **D10**, with D6 used only for direction. The IR remote library borrows D6's timer, so it can't do speed.
- The XIAO can sit on the car body with double-sided tape, close to J10.
