# Gripper Firmware

This firmware reads commands and writes responses to the serial interface. 

The commands are JSON formatted strings to actuate the gripper or request status information.

Every command must return a result to let the consumer know about success or failure.

## Commmands

### Opening

Opens and closes the gripper. The value is a percentage of the max opening so it is between 0 and 100. If relative is `false` then the opening is absolute.

```json
{"action": "open", "value": 50, "relative": false}
```

### Rotating
Rotates the gripper. The value is in degrees with limits between 0 and 180. If relative is `false` then the rotation is absolute.

```json
{"action": "rotate", "value": 180, "relative": false}
```
### Status
Requests status information of the gripper.
```json
{"action": "status"}
```

The reponse of this command includes the current opening and rotation values as well as the configured time the gripper waits before returning the response (so it has time to execute the action).

```json
{
  "opening": 50, "rotation": 180, 
  "rotateMaxDelayMs": 1000, "openMaxDelayMs": 1000
}
```

## General Responses

For the `open` and `rotate` commands, if the action was successful then the response is:
```json
{"result": "ok"}
```

If there is an error while processing any command then an error response will be returned. An example is as:
```json
{
  "result": "error", 
  "msg": "the gripper can only rotate between 0 and 180 degrees"
}
```