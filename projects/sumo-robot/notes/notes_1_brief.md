# Hardware.h

## Purpose

`Hardware.h` is the robot's **central hardware configuration file**.

It stores information about the robot's hardware so other files don't need to directly remember pin numbers and configuration values.

It contains things such as:

- Motor pin assignments
- Edge sensor pin assignments
- Opponent sensor pin assignments
- Start button pin
- Distance detection threshold
- Edge sensor state
- Number of sensor samples

The main idea is:

> **Hardware.h tells the program where the hardware is and what basic settings it uses. It does not contain the robot's decision-making logic.**

For example, instead of writing:

```cpp
digitalWrite(4, HIGH);
```

the program can use:

```cpp
digitalWrite(LEFT_R_EN, HIGH);
```

where `Hardware.h` defines `LEFT_R_EN` as pin `4`.

This makes the code easier to understand and means a wiring change only needs to be updated in the configuration file.

## Important Syntax

### `const int`

A typical hardware definition looks like:

```cpp
const int LEFT_L_EN = 2;
```

- `const` → the value should not be changed while the program runs.
- `int` → the value is an integer (whole number).
- `LEFT_L_EN` → the meaningful name given to the value.
- `=` → assigns the value on the right to the name on the left.
- `2` → the actual value, in this case the Arduino pin number.
- `;` → ends the statement.

Using meaningful names such as `LEFT_L_EN` is much clearer than repeatedly using raw numbers such as `2`.

### Include Guard

```cpp
#ifndef HARDWARE_H
#define HARDWARE_H

...

#endif
```

This is an **include guard**.

It prevents `Hardware.h` from being included multiple times and causing duplicate definitions.

For now, `#ifndef`, `#define`, and `#endif` can be treated as standard `.h` file boilerplate.

### Other important values

- `HIGH` and `LOW` → Arduino digital states.
- `A0`, `A1`, etc. → Arduino analog input pins.
- `DIST_THRESHOLD` → value used to determine when an opponent sensor reading counts as detected.
- `SENSOR_SAMPLES` → number of sensor readings kept for smoothing.

## Summary

`Hardware.h` is basically the robot's **hardware map and configuration sheet**.

It defines the names and values that other parts of the program use to communicate with the physical hardware.

---

# Motors.h

## Purpose

`Motors.h` defines the **motor-related functions available to the rest of the program**.

It acts like a simple interface or "menu" of motor commands:

- `initMotors()` — initialize the motors.
- `stopMotors()` — stop the motors.
- `forward(speed)` — move forward at a given speed.
- `backward(speed)` — move backward at a given speed.
- `turnLeft(speed)` — turn left.
- `turnRight(speed)` — turn right.

It does **not** contain the actual instructions for controlling the motor pins. Those are implemented in `Motors.cpp`.

This keeps the strategy code simple. The strategy can say `forward(200)` without needing to know how the BTS7960 or motor pins work.

## Function Declarations

Example:

```cpp
void forward(int speed);
```

The important syntax is:

- `void` → the function does not return a value.
- `forward` → function name.
- `int speed` → the function accepts an integer parameter called `speed`.
- `;` → ends the function declaration.

The intended speed range in this project is `0–255`.

A declaration tells the program **what function exists and what inputs it expects**. The actual implementation is written in `Motors.cpp`.

For example:

```cpp
forward(200);
```

calls the function and passes `200` as the speed.

## Include Guard

```cpp
#ifndef MOTORS_H
#define MOTORS_H

...

#endif
```

This is the same **include guard** used in `Hardware.h`. It prevents the header from being included multiple times.

## Header vs Implementation

The main distinction is:

```text
Motors.h
    ↓
"What motor commands are available?"

Motors.cpp
    ↓
"How do those commands actually control the motors?"

Strategy code
    ↓
"When should each motor command be used?"
```

So `Motors.h` provides the **motor interface** that other parts of the robot can use.

---

# Motors.cpp

## Purpose

`Motors.cpp` contains the **actual implementation of the motor commands** declared in `Motors.h`.

The flow is:

```text
Strategy
   ↓
forward(200)
   ↓
Motors.cpp
   ↓
PWM/electrical signals
   ↓
BTS7960
   ↓
Motor
```

`Motors.h` says **what motor commands exist**, while `Motors.cpp` explains **how those commands control the hardware**.

## Important Syntax

### `#include`

```cpp
#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
```

`#include` makes definitions from another file/library available to this file.

- `Arduino.h` → Arduino functions and values such as `pinMode()`, `digitalWrite()`, `analogWrite()`, `HIGH`, and `LOW`.
- `Hardware.h` → hardware pin names and configuration values.
- `Motors.h` → motor function declarations.

### Function implementation

```cpp
void forward(int speed) {
    // motor instructions
}
```

- `void` → function returns no value.
- `forward` → function name.
- `int speed` → accepts an integer parameter called `speed`.
- `{ }` → contains the actual instructions executed by the function.

### `pinMode()`

```cpp
pinMode(LEFT_L_EN, OUTPUT);
```

Configures a pin as an `INPUT` or `OUTPUT`.

Motor-control pins are configured as outputs because the Arduino needs to send signals to the motor drivers.

### `digitalWrite()`

```cpp
digitalWrite(LEFT_L_EN, HIGH);
```

Sets a digital pin to `HIGH` or `LOW`.

In this project, the enable pins are set `HIGH` to enable the motor drivers.

### `analogWrite()`

```cpp
analogWrite(LEFT_R_PWM, speed);
```

Uses PWM to control the motor driver's power/speed signal.

The project's PWM range is:

```text
0 → 255
```

where `0` is off and `255` is full duty cycle.

### `constrain()`

```cpp
speed = constrain(speed, 0, 255);
```

Keeps `speed` within the valid range.

For example:

```cpp
forward(300);
```

would be constrained to `255`.

## Motor Direction Logic

The BTS7960 uses separate PWM inputs for the two motor directions.

Conceptually:

```text
Forward:
R_PWM = speed
L_PWM = 0

Backward:
R_PWM = 0
L_PWM = speed
```

For turning, the two motors are driven in opposite directions:

```text
Turn left:
Left  → backward
Right → forward

Turn right:
Left  → forward
Right → backward
```

This allows the robot to rotate using **differential drive**.

## Why These Functions Exist

Functions such as:

```cpp
forward(200);
turnLeft(150);
stopMotors();
```

hide the complicated hardware instructions from the strategy code.

The strategy only needs to say **what movement it wants**. `Motors.cpp` handles **how the Arduino and BTS7960 produce that movement**.

### Main idea

```text
Motors.h
"What motor commands are available?"

        ↓

Motors.cpp
"How do those commands control the motors?"

        ↓

BTS7960 + motors
"Physical movement"
```

---

# Sensors.h

## Purpose

`Sensors.h` defines the **sensor interface** for the rest of the program.

It contains:

- The structures used to represent sensor readings.
- The functions available for initializing and reading the sensors.
- Functions for checking whether an opponent or edge has been detected.

It does **not** contain the actual code for reading the physical sensors. That is handled by `Sensors.cpp`.

## `struct`

The main new concept is `struct`.

A struct is a custom data container that groups related values together.

For example:

```cpp
struct OpponentReadings {
    int frontLeft;
    int frontRight;
    int left;
    int right;
};
```

This creates a data type called `OpponentReadings` containing four integer values.

It allows the program to treat all four sensor readings as one object:

```text
OpponentReadings
├── frontLeft
├── frontRight
├── left
└── right
```

`OpponentReadings` uses `int` because the distance sensors produce numerical ADC readings.

`EdgeReadings` uses `bool` because the edge sensors only need to represent two states:

```text
true  → detected
false → not detected
```

Using a struct keeps related sensor information organized and easy to pass between functions.

## Function Declarations

The file declares functions such as:

```cpp
OpponentReadings readOpponentSensors();
```

The type before the function name is the **return type**.

For example:

- `void` → returns nothing.
- `bool` → returns `true` or `false`.
- `OpponentReadings` → returns an `OpponentReadings` object.
- `EdgeReadings` → returns an `EdgeReadings` object.

The functions in this file include:

- `initSensors()` → configure sensor pins.
- `readOpponentSensors()` → read and return the four opponent sensor values.
- `readEdgeSensors()` → read and return the four edge sensor states.
- `isOpponentDetected(int reading)` → determine whether a reading counts as opponent detection.
- `anyEdgeDetected(EdgeReadings edges)` → determine whether any edge sensor has detected the boundary.

## `Hardware.h`

```cpp
#include "Hardware.h"
```

`Sensors.h` includes `Hardware.h` because it uses configuration values defined there, such as:

- `DIST_THRESHOLD`
- `EDGE_WHITE_STATE`
- `SENSOR_SAMPLES`

## Include Guard

```cpp
#ifndef SENSORS_H
#define SENSORS_H

...

#endif
```

This is the standard **include guard** used to prevent the header from being included multiple times.

## Main Idea

`Sensors.h` defines **what sensor information looks like and what sensor operations are available**.

```text
Hardware.h
   ↓
sensor configuration

Sensors.h
   ↓
sensor data structures + available functions

Sensors.cpp
   ↓
actual sensor-reading implementation

Strategy
   ↓
uses the sensor information
```

---

# Sensors.cpp

## Purpose

`Sensors.cpp` contains the **actual implementation of the sensor system**.

It reads the physical sensors, smooths the opponent sensor readings, converts edge sensor states into `true/false`, and returns clean sensor data for the strategy code.

## Sensor Buffers

The four opponent sensors each have their own array:

```cpp
static int frontLeftBuffer[SENSOR_SAMPLES];
```

An **array** stores multiple values of the same type. Since `SENSOR_SAMPLES = 4`, each buffer stores the four most recent readings.

Each sensor has its own buffer so their readings stay separate.

`static` here means these variables are kept private to `Sensors.cpp`. Other files cannot directly access the buffers.

`bufferIndex` keeps track of which position should be updated next. The buffers are therefore **rolling buffers** rather than continuously growing.

## `averageBuffer()`

The `averageBuffer()` function adds the stored readings and calculates their average.

It uses:

- `long` for the running sum.
- A `for` loop to go through the array.
- `+=` as shorthand for adding to an existing value.
- `return` to give the calculated average back.

The parameter:

```cpp
int *buffer
```

uses a **pointer**. In this case, it allows the function to receive an array of integers.

The same averaging operation can therefore be reused for all four sensor buffers.

## `initSensors()`

`initSensors()` prepares the sensor hardware.

It uses `pinMode(..., INPUT)` to configure the sensor pins as inputs.

It also initially fills the opponent sensor buffers with real sensor readings. This prevents the buffer from starting with empty/zero values that would incorrectly affect the first average.

## `readOpponentSensors()`

This function:

1. Reads the four analog sensors using `analogRead()`.
2. Stores the readings in their rolling buffers.
3. Moves `bufferIndex` to the next position.
4. Averages each buffer.
5. Stores the averages in an `OpponentReadings` struct.
6. Returns the struct.

The index is updated using:

```cpp
bufferIndex = (bufferIndex + 1) % SENSOR_SAMPLES;
```

`%` is the **modulo operator**. It gives the remainder and allows the index to wrap around:

```text
0 → 1 → 2 → 3 → 0 → ...
```

This keeps the buffer limited to the latest four readings.

## `readEdgeSensors()`

The edge sensors work differently from the opponent sensors.

They use `digitalRead()` and only need to determine whether the sensor is detecting the configured edge state.

The result is stored as `bool` values in an `EdgeReadings` struct:

```text
true  → edge detected
false → edge not detected
```

The comparison uses `==`, which means **"is equal to"**.

Remember:

```text
=   → assignment
==  → comparison
```

## `anyEdgeDetected()`

This function checks all four edge sensor values using `||`.

`||` means **OR**.

Therefore, if any one of the four sensors is `true`, the function returns `true`.

This gives the strategy a simple check:

```text
Did any edge sensor detect the boundary?
```

without needing to manually check all four sensors.

## Main Idea

The important purpose of `Sensors.cpp` is to convert **raw electrical sensor readings into clean information that the strategy can use**.

```text
Physical sensors
      ↓
analogRead / digitalRead
      ↓
Process and smooth readings
      ↓
OpponentReadings / EdgeReadings
      ↓
Strategy
```

The sensor buffers exist mainly to reduce noise and provide a more stable reading instead of trusting one instantaneous measurement.

---

# Motors.h Update

Add the following function declaration to `Motors.h`:

```cpp
void drive(int leftSpeed, int rightSpeed);
```

## Purpose

`drive()` allows the program to control the **left and right motor speeds independently**.

- `leftSpeed` → PWM speed for the left motor.
- `rightSpeed` → PWM speed for the right motor.

This is useful for both strategies:

- **Strategy 2** can use it for searching and hard turns.
- **Strategy 1** can directly calculate its left and right speeds for P-controller steering.

`drive()` provides a cleaner way to control both motors without having to combine separate movement functions.

No other changes are needed in `Motors.h`.

---

# Motors.cpp Update

Add the following function to `Motors.cpp`:

```cpp
void drive(int leftSpeed, int rightSpeed) {
    leftSpeed  = constrain(leftSpeed, 0, 255);
    rightSpeed = constrain(rightSpeed, 0, 255);

    analogWrite(LEFT_R_PWM, leftSpeed);
    analogWrite(LEFT_L_PWM, 0);

    analogWrite(RIGHT_R_PWM, rightSpeed);
    analogWrite(RIGHT_L_PWM, 0);
}
```

## Purpose

`drive()` provides **independent forward speed control** for the left and right motors.

- `leftSpeed` controls the left motor.
- `rightSpeed` controls the right motor.
- Both speeds are limited to the PWM range `0–255`.
- Both sides are configured for forward motion only.

For example:

```cpp
drive(200, 100);
```

makes the left motor faster than the right motor, causing the robot to curve right.

Because both parameters are limited to `0–255`, negative values cannot be used for reverse motion.

No other changes are required for this addition.
