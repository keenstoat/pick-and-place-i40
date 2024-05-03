/*
  Author: Yaman Alsaady
  Description: This Arduino code controls two servos - one for gripping and one
  for rotation - using an ESP32 microcontroller.
*/

#include "esp32-hal-gpio.h"
#include <Arduino.h>
#include <ESP32Servo.h>

#define SERVO 26
#define SERVO_ROT 27
#define TABLE_PIN1 12
#define TABLE_PIN2 13

Servo gripper;
Servo rotation;

void setup() {
  Serial.begin(115200); // Initialize serial communication

  pinMode(SERVO, OUTPUT);     // Set servo pin as output
  pinMode(SERVO_ROT, OUTPUT); // Set rotation servo pin as output

  pinMode(TABLE_PIN1, OUTPUT);
  pinMode(TABLE_PIN2, OUTPUT);
  digitalWrite(TABLE_PIN1, LOW);
  digitalWrite(TABLE_PIN2, LOW);

  // Attach servos to corresponding pins with min and max pulse duration
  gripper.attach(SERVO, 500, 2500);
  rotation.attach(SERVO_ROT, 500, 2500);
}

void loop() {
  // Check for incoming serial data
  while (Serial.available() > 0) {
    // Read gripping and rotation values
    int gripping_var = Serial.parseInt();
    int rotation_var = Serial.parseInt();
    int table_var = Serial.parseInt();
    // If end of line character is received
    if (Serial.read() == '\n') {
      // Constrain values to be within 0 and 180
      gripping_var = constrain(gripping_var, 0, 180);
      rotation_var = constrain(rotation_var, 0, 180);
      // Set servo positions
      gripper.write(gripping_var);
      rotation.write(rotation_var);

      digitalWrite(TABLE_PIN1, table_var > 0 ? HIGH : LOW);
      digitalWrite(TABLE_PIN2, table_var < 0 ? HIGH : LOW);
    }
  }
}
