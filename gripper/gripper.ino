#include <ArduinoJson.h>
#include <Servo.h>
//#include <ESP32Servo.h>


#define GRIP_SERVO_PIN 26
#define ROTATION_SERVO_PIN 27

#define GRIP_MIN_ANGLE 60
#define GRIP_MAX_ANGLE 165

#define ROTATE_MIN_ANGLE 48
#define ROTATE_MAX_ANGLE 134

Servo servoGrip;
Servo servoRotate;

JsonDocument jsonDoc;


void setup() {
    Serial.begin(115200);
    // servoGrip.attach(GRIP_SERVO_PIN, Servo::CHANNEL_NOT_ATTACHED, GRIP_MIN_ANGLE, GRIP_MAX_ANGLE);
    // servoRotate.attach(ROTATION_SERVO_PIN, Servo::CHANNEL_NOT_ATTACHED, ROTATE_MIN_ANGLE, ROTATE_MAX_ANGLE);
    servoGrip.attach(GRIP_SERVO_PIN);
    servoRotate.attach(ROTATION_SERVO_PIN);
    servoGrip.write(0);
    servoRotate.write(0);

}

void loop() {

    if(Serial.available() > 0) {

        /**
        {"action": "status"}
        {"action": "grip", "value": 0}
        {"action": "rotate", "value": 0}
        */

        const auto error = deserializeJson(jsonDoc, Serial);

        if(error) {
            Serial.print(F("{\"error\": \""));
            Serial.print(error.c_str());
            Serial.println("\"}");
            
        } else {
            String action = jsonDoc["action"];

            if(action == "status") {
                sendStatus();

            } else if(action == "grip") {
                int gripAngle = jsonDoc["value"];
                actuateGrip(gripAngle);

            } else if(action == "rotate") {
                int rotateAngle = jsonDoc["value"];
                rotate(rotateAngle);
                
            } else {

                Serial.println("no option");
                Serial.println(action);
            }
            
        }
    }
}

void sendStatus() {
    JsonDocument doc;
    deserializeJson(doc, "{\"ok\": true}");
    serializeJson(doc, Serial);
    Serial.println();
}

void actuateGrip(int value) {
    if(value < 0 || value > 100)
        return;
    value = GRIP_MIN_ANGLE + value;
    servoGrip.write(value);
    Serial.println(value);
}

void rotate(int value) {

    if(value < 0 || value > 180)
        return;

//    value = ROTATE_MIN_ANGLE + value;
    servoRotate.write(value);
    Serial.println(value);
}
