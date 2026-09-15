# SumoX-26 — Arduino UNO Q Wiring & Pin Map (Final, v3)

This is the definitive pin assignment — safe to code your constants against right now. The power-supply *voltages* feeding some of these pins still have a few physical checks pending (listed in Section 4); those checks won't change which pin anything plugs into, only what's allowed to sit behind it before you power up.

---

## 1. Pin assignment table — this goes to that pin

| Arduino pin | Wire goes to | Signal type |
|---|---|---|
| D2 | Left BTS7960 — **L_EN** | Digital out |
| D3 | Left BTS7960 — **R_PWM** | PWM out |
| D4 | Left BTS7960 — **R_EN** | Digital out |
| D5 | Left BTS7960 — **L_PWM** | PWM out |
| D6 | Right BTS7960 — **L_PWM** | PWM out |
| D7 | Right BTS7960 — **R_EN** | Digital out |
| D8 | Right BTS7960 — **L_EN** | Digital out |
| D9 | Right BTS7960 — **R_PWM** | PWM out |
| D10 | Edge sensor 1 — **DO** | Digital in |
| D11 | Edge sensor 2 — **DO** | Digital in |
| D12 | Edge sensor 3 — **DO** | Digital in |
| D13 | Edge sensor 4 — **DO** | Digital in |
| A0 | Opponent sensor 1 — Vo (through divider) | Analog in |
| A1 | Opponent sensor 2 — Vo (through divider) | Analog in |
| A2 | Opponent sensor 3 — Vo (through divider) | Analog in |
| A3 | Opponent sensor 4 — Vo (through divider) | Analog in |
| A4 | Free | — |
| A5 | Free | — |
| D0, D1 | Free (kept clear of RX/TX) | — |
| 3.3V | → TCRT5000 VCC ×4, pending confirmation (§4) | Power out |
| 5V | Not used for external power — board is powered via VIN instead | — |
| VIN | ← battery bus (fused, switched) | Power in |
| GND | ← common ground bus | Ground |

D3/D5/D6/D9 are confirmed PWM-capable straight from Arduino's own UNO Q pinout diagram (marked with `~` on the official pin map) — same PWM set as the classic Uno, so no assumption needed there anymore.

R_IS/L_IS on both BTS7960 modules stay disconnected.

---

## 2. Signal conditioning on the way to those pins

**GP2Y0A21 → A0–A3**, each through its own divider:

```
GP2Y Vo ──── 10kΩ ────┬──── UNO Q analog pin
                      │
                     10kΩ
                      │
                     GND
```

The GP2Y0A21 is a 5V-powered analog sensor with a distance-dependent output (not a flat 0–5V swing) — the divider isn't there because the sensor "outputs 0–5V," it's there as conservative protection because the UNO Q's ADC input ceiling is 3.3V and analog-mode pins lose their 5V tolerance even where the same pin would tolerate 5V as a plain digital input. With the divider, a sensor output of X volts becomes X/2 volts at the pin — halve your math back out in code when converting ADC counts to distance.

You'll need 8× 10kΩ resistors (two per sensor) — these aren't on your current parts list yet.

**TCRT5000 → D10–D13**: direct connection, no divider — *once* the module is confirmed to run on 3.3V (see checklist).

---

## 3. Power architecture

```
3S battery pack (confirmed, measured — see §4)
    │
    ▼
35A fuse (rating to be confirmed against actual current draw — see §4)
    │
    ▼
Main rocker switch (pinout to be confirmed with multimeter — see §4)
    │
    ├──→ Left BTS7960  B+  (B− → common GND)
    ├──→ Right BTS7960 B+  (B− → common GND)
    ├──→ UNO Q VIN
    └──→ UBEC input

UBEC output (5V, measured)
    ├──→ GP2Y sensors ×4 — VCC
    └──→ BTS7960 logic VCC ×2 — provisional, see §4

UNO Q 3.3V pin
    └──→ TCRT5000 ×4 — VCC — provisional, see §4

Common ground bus:
    battery− / UNO Q GND / both BTS7960 GND (logic + B−) / UBEC GND / all sensor GNDs
```

**BTS7960 logic VCC defaults to 5V, not 3.3V**, until your specific modules are confirmed otherwise. "Accepts 3.3–5V on the control inputs" and "VCC can be powered at 3.3V" are two different claims — most IBT-2/BTS7960 boards are built expecting a 5V logic supply even when their RPWM/LPWM/EN inputs happily read a 3.3V HIGH. So the control pins (D2–D9) go straight to the UNO Q's 3.3V logic as planned, but VCC gets 5V from the UBEC until a photo of your actual modules says otherwise.

Capacitors: your invoice has **one** 2200µF/35V cap, not two — so it sits across the shared motor-power distribution bus (positive/negative), close to where the two BTS7960 draw from it, rather than "one per driver." A second one would be needed if you want a local cap at each driver individually. The 470µF/16V cap goes across the UBEC's 5V/GND output.

---

## 4. Still needs a physical check before anything is powered on

| # | Item | What to check | Blocks |
|---|---|---|---|
| 1 | 3S battery pack | Measure holder output with a multimeter — expect ~9–12.6V depending on charge; confirm polarity | VIN connection |
| 2 | 18650 cells ×6 | Read the actual printed brand/model/discharge rating off the cells — "600–3800mAh" on the invoice isn't a real spec | Whether these cells are motor-suitable at all |
| 3 | 4-way charger | Confirm whether it's built to charge an assembled 3S series pack, or individual cells only | Charging procedure |
| 4 | 35A fuse | Confirm the rating actually fits your measured motor stall current + wiring/connector ratings, don't assume "fuse present = safe" | Fuse sizing |
| 5 | BTS7960 modules ×2 | Photo front + back, read the printed VCC/input spec off the board | Whether VCC stays at 5V default or moves to 3.3V |
| 6 | TCRT5000 modules ×4 | Read the printed voltage spec; confirm DO is actively driven and rises to VCC | Whether 3.3V is used or an alternative is needed |
| 7 | GP2Y sensors ×4 | Confirm actual printed part number (your invoice says SK0F; commonly documented part is YK0F) | Confirms exact output range |
| 8 | Rocker switch | Multimeter-test the 3 pins to identify common / switched-output / LED-negative before wiring | Main power wiring |
| 9 | 10kΩ resistors | Not yet on your parts list — need 8 for the GP2Y dividers | GP2Y wiring |

None of these change the pin table in Section 1 — they only decide what's allowed to sit on the power rails behind it. You can write and test all the digital/PWM/edge-sensor code against Section 1 right now; hold off connecting the battery until the checklist above is cleared.

---

## 5. Wiring practice notes

- Motor power path (battery → fuse → switch → driver B+/B−, driver → motor) needs real gauge wire, not the jumper-wire kit — jumpers are for logic/sensor signals only.
- Electrolytic capacitors are polarized: + to positive rail, − to ground, never reversed.
- Two UBECs (if you use both) are separate regulated branches, not isolated ones — they still share a common ground with everything else. Don't rely on a second UBEC alone for noise immunity; short sensor wiring and physical separation from motor-current paths do more of that work.
- One common ground, always, across every rail above.
