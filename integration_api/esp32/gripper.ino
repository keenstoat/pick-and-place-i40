#include <ArduinoJson.h>
#include <Servo.h>

#define OPEN_SERVO_PIN 26
#define ROTATE_SERVO_PIN 27

#define OPEN_MIN_VALUE 0
#define OPEN_MAX_VALUE 100
#define OPEN_INPUT_MIN_VALUE 0
#define OPEN_INPUT_MAX_VALUE 100

#define ROTATE_MIN_ANGLE 3
#define ROTATE_MAX_ANGLE 135
#define ROTATE_INPUT_MIN_VALUE 0
#define ROTATE_INPUT_MAX_VALUE 180

int rotateMaxDelayMs = 1000;
int openMaxDelayMs = 1000;

Servo servoOpen;
Servo servoRotate;

int currentOpening = 0;
int currentRotation = 0;

JsonDocument jsonDoc;

void setup()
{
    Serial.begin(115200);
    servoOpen.attach(OPEN_SERVO_PIN);
    servoRotate.attach(ROTATE_SERVO_PIN);

    // initialize griper opening and rotation 
    servoOpen.write(OPEN_MIN_VALUE);
    servoRotate.write(ROTATE_MIN_ANGLE);
}

void loop() {
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

            } else if (action == "config") {
                config();

            } else {
                sendError("unknown action '"+ action +"'");
            }
        }
    }
}

void sendError(String msg) {
    Serial.print(F("{\"result\":\"error\", \"msg\": \""));
    Serial.print(msg);
    Serial.println("\"}");
    Serial.flush();
}

void sendOk() {
    Serial.println(F("{\"result\": \"ok\"}"));
    Serial.flush();
}

void sendStatus() {

    Serial.print(F("{\"opening\":"));
    Serial.print(currentOpening);
    Serial.print(F(",\"rotation\":"));
    Serial.print(currentRotation);
    Serial.print(F(",\"rotateMaxDelayMs\":"));
    Serial.print(rotateMaxDelayMs);
    Serial.print(F(",\"openMaxDelayMs\":"));
    Serial.print(openMaxDelayMs);
    Serial.println(F("}"));
    Serial.flush();
}

void config() {
    
    if(jsonDoc.containsKey("rotateMaxDelayMs")) {
        rotateMaxDelayMs = jsonDoc["rotateMaxDelayMs"];
    }

    if(jsonDoc.containsKey("openMaxDelayMs")) {
        openMaxDelayMs = jsonDoc["openMaxDelayMs"];
    }

    sendOk();
}

void openGripper() {
  
    if(!jsonDoc.containsKey("value")) {
        sendError("must specify a value to open gripper");
        return;
    }
    
    int value = jsonDoc["value"];
    bool isRelative = jsonDoc["relative"];

    value = isRelative ? currentOpening + value : value;

    if (value < OPEN_INPUT_MIN_VALUE || value > OPEN_INPUT_MAX_VALUE) {
        sendError(
            "the gripper can only open between " + String(OPEN_INPUT_MIN_VALUE) 
            + " and " + String(OPEN_INPUT_MAX_VALUE) + " percent"
        );
        return;
    }
    
    int relativeDelay = openMaxDelayMs * abs(value - currentOpening) / OPEN_INPUT_MAX_VALUE;
    currentOpening = value;
    servoOpen.write(value);
    delay(relativeDelay);
    sendOk();
}

void rotateGripper() {

    if(!jsonDoc.containsKey("value")) {
        sendError("must specify a value to rotate gripper");
        return;
    }
    int value = jsonDoc["value"];
    bool isRelative = jsonDoc["relative"];

    value = isRelative ? currentRotation + value : value;

    if (value < ROTATE_INPUT_MIN_VALUE || value > ROTATE_INPUT_MAX_VALUE) {
        sendError(
            "the gripper can only rotate between " + String(ROTATE_INPUT_MIN_VALUE) 
            + " and " + String(ROTATE_INPUT_MAX_VALUE) + " degrees"
        );
        return;
    }

    int relativeDelay = rotateMaxDelayMs * abs(value - currentRotation) / ROTATE_INPUT_MAX_VALUE;
    currentRotation = value;
    value = ROTATE_MIN_ANGLE + (value * (ROTATE_MAX_ANGLE - ROTATE_MIN_ANGLE) / ROTATE_INPUT_MAX_VALUE);
    servoRotate.write(value);
    delay(relativeDelay);
    sendOk();
}
