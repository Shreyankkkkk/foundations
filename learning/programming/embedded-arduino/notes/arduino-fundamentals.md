# Arduino / C Programming — Fundamentals

Coming from Python. Goal: be able to read and modify the Besomi Sumo Robot kit code.

---

## 1. Big Picture Differences from Python

| Python | C / Arduino |
|---|---|
| No type declared: `x = 5` | Must declare type: `int x = 5;` |
| Indentation defines blocks | Curly braces `{ }` define blocks — indentation is just style, doesn't matter to the compiler |
| No semicolons | Every statement ends in `;` |
| `def function_name():` | Must declare a return type: `void functionName() {` (`void` = returns nothing) |
| `if x == 5:` | `if (x == 5) {` — condition always wrapped in `( )` |
| Runs top to bottom once, loop manually with `while True:` | Arduino auto-repeats `loop()` forever, forever, with no code needed to make that happen |

---

## 2. Program Structure — `setup()` and `loop()`

Every Arduino sketch (a "sketch" = an Arduino program) needs exactly these two functions:

```arduino
void setup() {
  // runs ONCE, when the board powers on / resets
}

void loop() {
  // runs FOREVER, automatically, right after setup() finishes
}
```

- `void` = this function doesn't return/give back a value, it just performs actions.
- You never write "repeat forever" — putting code inside `loop()` is what makes it repeat. This is different from Python where you'd need an explicit `while True:`.
- Use `setup()` for one-time configuration (declaring pins, starting Serial communication).
- Use `loop()` for the actual repeating robot logic (read sensors, decide, act).

---

## 3. Pins — Digital vs Analog vs Power

| Pin type | What it's for | Notes |
|---|---|---|
| **Digital pins** (0–13) | ON/OFF only (HIGH or LOW), no in-between values | Used for buttons, LEDs, motor control signals |
| **Analog input pins** (A0–A5) | Can read a *range* of values (not just on/off) via `analogRead()` | Can ALSO be read digitally with `digitalRead()` if you only need on/off — this is what the sumo kit does for its IR sensors |
| **Power pins** (5V, 3.3V, GND, VIN) | Supply / reference voltage | See GND note below |

**Important — GND is not one special pin.** A board usually has multiple pins labeled GND (ground). They are *all electrically the same point*, wired together internally. It does not matter which GND pin you use — there is no "the correct" GND, they're interchangeable. Boards just give you several so you have room to wire multiple components at once.

---

## 4. Configuring a Pin — `pinMode()`

```arduino
pinMode(13, OUTPUT);       // pin 13 will SEND power (e.g. to an LED)
pinMode(2, INPUT_PULLUP);  // pin 2 will READ a signal (e.g. from a button)
```

- Must be called once, inside `setup()`, before you use a pin.
- `OUTPUT` = this pin sends power out (LEDs, motor driver signal pins).
- `INPUT_PULLUP` = this pin reads a signal, and defaults to reading `HIGH` when nothing is connected/pressed. This means a button wired this way reads `LOW` when pressed (see button section below) — it's "backwards" on purpose, and is the standard way to wire buttons/switches to avoid needing an extra resistor.

---

## 5. Writing to a Pin — `digitalWrite()`

```arduino
digitalWrite(13, HIGH);  // turn pin 13 ON (send 5V)
digitalWrite(13, LOW);   // turn pin 13 OFF (send 0V)
```

- `HIGH` = on / 1 / full voltage. `LOW` = off / 0 / no voltage.
- Used for LEDs, and (in the sumo kit) for sending motor control signals to the motor driver pins.

---

## 6. Reading from a Pin — `digitalRead()`

```arduino
int buttonState = digitalRead(2);
```

- Checks the pin right now, returns either `HIGH` or `LOW`.
- Store the result in a variable so you can check it more than once without re-reading the pin.

---

## 7. Variables

```arduino
int buttonState = digitalRead(2);  // int = whole number
bool switchPressed = false;        // bool = true/false only
```

- Unlike Python, you must state the type when creating a variable.
- `int` = integer (whole number). `bool` = true or false.
- `const int PIN_NAME = 2;` — `const` means this value never changes after being set; commonly used for naming pins so code is readable (e.g. `SWITCH_PIN` instead of a bare number `2`).

---

## 8. Pausing — `delay()`

```arduino
delay(1000);  // pause for 1000 milliseconds = 1 second
```

- Nothing else happens on the board while `delay()` is running — it's a full stop.
- 1000 = 1 second. 500 = half a second. Etc.

---

## 9. Conditionals — `if / else if / else`

```arduino
if (buttonState == LOW) {
  // do this if true
} else if (otherCondition == HIGH) {
  // do this if the first was false but this is true
} else {
  // do this if none of the above were true
}
```

- Same logic as Python's `if/elif/else`, different punctuation: parentheses around the condition, curly braces around the block, no colons.
- `==` (double equals) means "is equal to" — a comparison/question.
- `=` (single equals) means "set this variable to" — an assignment. Mixing these up is a very common bug.
- **Order matters.** Conditions are checked top to bottom, and the first one that's true "wins" — the rest are skipped. This is why safety checks (like edge/line detection) should always be the *first* `if`, checked before anything else, every single loop cycle — so nothing can override it.

---

## 10. Functions

```arduino
void forward() {
  digitalWrite(13, HIGH);
}
```

- A named, reusable block of code, just like Python's `def`.
- `void` before the name = it doesn't return a value, it just performs an action.
- Call it elsewhere in the code by writing `forward();`

---

## 11. Serial Monitor — debugging output

```arduino
Serial.begin(9600);              // put in setup() — turns on communication, 9600 = speed
Serial.println("Hello");         // put in loop() or anywhere — prints text + a line break
```

- Lets you see what your code is "thinking" in real time on your computer screen while it runs.
- Extremely useful for debugging sensor readings and confirming which `if` branch is running.

---

## 12. Pushbuttons — wiring logic

A 4-legged pushbutton is **not 4 separate connections** — it's 2 pairs of legs (2 "contacts"). Each contact has a left pin and a right pin that are **always connected to each other**, pressed or not. Pressing the button connects the two *different* contacts to each other.

- Wokwi pin names: `1.l`, `1.r` (contact 1, left/right legs), `2.l`, `2.r` (contact 2, left/right legs).
- **Wrong wiring (what I tried first):** `1.l` → pin, `1.r` → GND. This fails because `1.l` and `1.r` are the *same* contact — always connected to each other regardless of whether the button is pressed. Wiring both legs of one contact just makes a permanent short, not a switch.
- **Correct wiring:** one leg from contact 1 (e.g. `1.r`) → digital pin, one leg from contact 2 (e.g. `2.l`) → GND. Now pressing the button is what completes the circuit between the two different contacts.
- With `INPUT_PULLUP`: pin reads **LOW when pressed**, **HIGH when not pressed** (this feels backwards until you remember why — see `pinMode` section above).

**Momentary vs. a switch:** the pushbutton used here is a *momentary* button — it's only "pressed" while physically held down, and returns to released the instant you let go. This is different from a toggle switch, which stays in whatever position you last set it to (like a light switch) until you flip it again. This is why holding the button kept the LED on, but letting go turned it off immediately — that's correct, expected behavior for a momentary button, not a bug.

**Bouncing (good to know, not used yet):** physical buttons rapidly connect/disconnect many times over about 1ms when pressed, due to the mechanical contacts. Wokwi simulates this by default. It can cause a single press to be read as multiple presses in more advanced code. Not an issue for the simple on/off checks done so far, but relevant later if counting button presses.

---

## 13. Exercises Completed So Far

| # | File | What it proved |
|---|---|---|
| 1 | `exercises/01-blink-led.ino` | `setup()`/`loop()`, `pinMode`, `digitalWrite`, `delay` |
| 2 | `exercises/02-button-led.ino` | `INPUT_PULLUP`, `digitalRead`, variables, `if/else`, `Serial` |
| 3 | `exercises/03-multi-sensor-priority.ino` | Multiple inputs, `else if` priority chains — structurally identical to the real sumo kit's `loop()` |
| 4 | `exercises/04-button-toggle-edge-detection.ino` | Edge detection (reacting to a state *change*, not just current state), the `!` toggle operator, variables that persist across loops, basic debounce with `delay()` |

---

## 14. Edge Detection — Reacting to a CHANGE, not a state

So far (Exercises 01-03), every `if` checked the button's **current** state each loop: "is it LOW right now?" That's fine for a held-down action (LED on only while held), but it can't do something like "toggle on a single press" — if you just toggle every time you see `LOW`, the LED would flip on and off dozens of times per second while the button is held (because `loop()` runs continuously, and the button stays `LOW` for the whole hold).

**The fix: remember the previous reading, and compare it to the current one.**

```arduino
bool previousButtonState = HIGH;  // declared OUTSIDE loop() so it survives between loops
...
bool buttonState = digitalRead(BUTTON);

if (previousButtonState == HIGH && buttonState == LOW) {
  // this exact instant is the moment the button WENT from released to pressed
  // (a "falling edge") — not just "the button happens to be pressed right now"
}

previousButtonState = buttonState;  // save for next loop's comparison
```

This only becomes true for exactly one loop cycle — the specific moment the transition happens — even though the button might stay held (and `LOW`) for hundreds of loop cycles afterward. This is called **edge detection**: reacting to a *change* in a signal, rather than its current level.

**Why this needs a variable declared outside `loop()`:** any variable created *inside* `loop()` gets wiped and recreated fresh every single time `loop()` runs — it can't remember anything from the previous cycle. `previousButtonState` is declared above `setup()`/`loop()`, alongside `ledState`, so both persist across every loop iteration. This is the same reason the kit code declares `lastDirection` at the top of the file instead of inside `loop()`.

## 14b. The `!` (NOT) Operator — Toggling

```arduino
ledState = !ledState;
```

`!` flips a `bool`: `!true` becomes `false`, `!false` becomes `true`. This is how a toggle is written in one line — instead of an `if/else` that separately sets `true` or `false`, `!ledState` always flips whatever it currently is. Then `digitalWrite(LED, ledState)` applies it — note `digitalWrite` accepts a `bool` here the same way it accepts `HIGH`/`LOW`, since `HIGH` is really just `1` (true-like) and `LOW` is `0` (false-like) under the hood.

## 14c. Debounce — `delay(50)` at the end of loop

Physical buttons don't cleanly switch from released to pressed — the metal contacts can bounce (rapidly connect/disconnect several times within about 1ms) before settling, which without protection could register as several presses instead of one. A short `delay(50)` at the end of each loop is a simple (not perfect, but good enough for this) way to slow down how often the button is re-checked, giving the contact time to settle before the next reading — this is called **debouncing**. More robust debounce techniques exist (checking elapsed time with `millis()` instead of blocking with `delay()`), but a small delay is a reasonable first tool.

## 15. Direct Mapping to the Besomi Sumo Kit Code

Everything above appears directly in the kit's source code:

```arduino
const int SWITCH_PIN = A0;                              // → Section 7 (variables)
pinMode(SWITCH_PIN, INPUT_PULLUP);                       // → Section 4
switchPressed = (digitalRead(SWITCH_PIN) == LOW);        // → Sections 6, 9, 12
digitalWrite(LEFTMOTOR_LPWM_PIN, HIGH);                  // → Section 5
if (lineLeft == WHITE || lineRight == WHITE) { ... }     // → Section 9 (priority order — checked FIRST)
else if (obstacleCenter == DETECTED) { ... }             // → Section 9
```

The kit's edge/line check is written as the *first* `if` in `loop()`, before the attack/search checks — this is exactly the "safety check goes first" principle from Section 9, so the robot can never accidentally attack its way over the edge.
