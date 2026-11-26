# First power-up, step by step (so nothing blows up)

Do these **in order**. Each step adds one thing. If a step fails, stop there and fix it before going on.

**You need:** a multimeter. A bench power supply with a current limit is ideal (the uni lab has them). If you don't have one, use one battery pack and watch for heat or smell.

## 0. Before any power
1. Look the board over: no solder blobs between pins, every chip's dot or stripe matches the board's marking.
2. Multimeter on **beep (continuity)**: check **+5V to GND**, **pack + to GND** and **solar + to GND** don't beep. A beep means a short. Stop.
3. **Don't solder the Arduino or the XIAO yet.**

## 1. 5 V supply only
1. Bench supply: **7.4 V, current limit 0.2 A** → into **J2** (bottom pin = +, check it!). Main switch J4 **on** (or jumper the 2 pins).
2. Measure **+5V** (any 5V header pin to GND): it should read **4.9–5.1 V**. The red **5V LED** should be on.
3. Current with nothing else connected should be **under about 20 mA**. If it hits the limit, there's a short. Stop.

## Uploading code: keep the car switched ON
The Nano Every's USB feeds its 5V pin through a diode. If you plug USB in while the car is **off**, your PC tries to power the whole 5 V side (Arduino, XIAO, servo, sensors). That's harmless, but a moving servo can make the PC's USB port cut out. **Upload with the car switched on** (a pack plugged in), or unplug the servo while uploading. The same goes for the XIAO's USB-C.

## 2. Add the Arduino
1. Solder the Nano Every. Power up again: the current rises about 20–40 mA, and +5V stays at about 5 V.
2. Upload a "blink" test. ✅ means the 5 V supply and the Arduino are good.

## 3. Battery switches
1. Upload a test that turns **LOAD_A** on (D11 HIGH) for 2 s, then off. Measure **VMOT** (C17): it should read pack voltage when on, about 0 V when off.
2. Same for LOAD_B (D12), and the charge switches CHG_A (D13) and CHG_B (A3) into a pack.
3. **Never turn LOAD_A and LOAD_B on together** (5 ms pause between them).

## 4. Motors
1. Plug in **one** motor, raise the current limit to **1 A**, set nSLEEP (D3) HIGH, and send slow PWM (25%). It should spin. Reverse it.
2. Then both motors.

## 5. Solar charging
1. Plug the solar pairs (or the 12 V USB-C adapter) into **J1**, with a pack in J2 and CHG_A on.
2. The CHRG signal (A7) goes LOW while charging. The pack voltage rises slowly and stops at **8.3 V**.

## 6. XIAO + phone
1. Solder the XIAO on pin headers (5V/GND/3V3 matching the board labels).
2. Check its **3V3 pin reads about 3.3 V**, then run the I2C test from `docs/phone_dashboard_plan.md`.

## 7. Real batteries
Only after all the above: connect the real packs (with their BMS) and do a short drive.
