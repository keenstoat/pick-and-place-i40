#include <ArduinoJson.h>
#include <Servo.h>

#define GRIP_SERVO_PIN 26
#define ROTATION_SERVO_PIN 27

#define GRIP_MIN_ANGLE 0
#define GRIP_MAX_ANGLE 100

#define ROTATE_MIN_ANGLE 3
#define ROTATE_MAX_ANGLE 135

Servo servoGrip;
Servo servoRotate;

int opening = 0;
int rotation = 0;

JsonDocument jsonDoc;

void setup()
{
    Serial.begin(115200);
    servoGrip.attach(GRIP_SERVO_PIN);
    servoRotate.attach(ROTATION_SERVO_PIN);

    // initialize griper openning and rotation 
    servoGrip.write(GRIP_MIN_ANGLE);
    servoRotate.write(ROTATE_MIN_ANGLE);
}

void loop()
{
    if (Serial.available() > 0) {

        const auto error = deserializeJson(jsonDoc, Serial);

        if (error) {
            Serial.print(F("{\"error\": \""));
            Serial.print(error.c_str());
            Serial.println("\"}");
            
        } else {
            String action = jsonDoc["action"];

            if (action == "status") {
                sendStatus();

            } else if (action == "open") {
                openGripper();

            } else if (action == "rotate") {
                rotateGripper();

            } else {
                sendError("unknown action '"+ action +"'");
            }
        }
    }
}

void sendError(String msg){
    Serial.print(F("{\"error\": \""));
    Serial.print(msg);
    Serial.println("\"}");
}

void sendStatus() {
    JsonDocument doc;
    deserializeJson(doc, "{}");
    doc["opening"] = opening;
    doc["rotation"] = rotation;
    serializeJson(doc, Serial);
    Serial.println();
}

void openGripper() {

    int value = jsonDoc["value"];
    bool isRelative = jsonDoc["relative"] ? jsonDoc["relative"] : false;

    if(!value) {
        sendError("must specify a value to open gripper");
        return;
    }
        
    value = isRelative ? opening + value : value;

    if (value < 0 || value > 100) {
        sendError("the gripper can only open between 0 and 100 percent");
        return;
    }

    opening = value;
    servoGrip.write(value);
}

void rotateGripper() {

    int value = jsonDoc["value"];
    bool isRelative = jsonDoc["relative"] ? jsonDoc["relative"] : false;

    if(!value) {
        sendError("must specify a value to rotate gripper");
        return;
    }

    value = isRelative ? rotation + value : value;

    if (value < 0 || value > 180) {
        sendError("the gripper can only rotate between 0 and 180 degrees");
        return;
    }

    rotation = value;
    value = ROTATE_MIN_ANGLE + (value * (ROTATE_MAX_ANGLE - ROTATE_MIN_ANGLE) / 180);
    servoRotate.write(value);
}
