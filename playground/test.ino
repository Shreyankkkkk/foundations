/*
Arduino Sketch (.ino)

What is a .ino file?
An .ino file is the file format used by Arduino IDE for writing Arduino programs.

It contains Arduino C/C++ code that gets compiled and uploaded onto an Arduino board.

Unlike normal C++ programs, Arduino programs do not use a main() function directly.
Instead, Arduino provides two main functions:

setup()
- Runs once when the Arduino starts.
- Used for initialization (setting pin modes, starting communication, etc.)

loop()
- Runs repeatedly forever after setup() finishes.
- Contains the main behavior of the Arduino program.

The Arduino IDE compiles the .ino file into machine code and uploads it to the microcontroller.

Example flow:

.ino file
    ↓
Arduino IDE compiler
    ↓
Machine code
    ↓
Arduino microcontroller
    ↓
Hardware executes instructions


Basic structure:
void setup() {
    // Runs once
}
void loop() {
    // Runs repeatedly
}


This file exists to test Arduino sketches and understand how .ino files work.
*/


void setup() {
  Serial.begin(9600);
  Serial.println("Arduino test started");
}


void loop() {
  Serial.println("Running...");
  delay(1000);
}

/* If you take any .ino file and try to run it like a normal program through the VS Code terminal, you will get no output, 
because .ino files are not designed to run directly in your computer's terminal. */ 
