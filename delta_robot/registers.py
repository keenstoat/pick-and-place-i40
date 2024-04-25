

from enum import IntEnum

class Coils(IntEnum):

    HAS_AXES                = 10 # (info) Has robot axes
    HAS_EXTERNAL_AXES       = 11 # (info) Has external axes
    HAS_GRIPPER_AXES        = 12 # (info) Has gripper axes
    HAS_PLATFORM_AXES       = 13 # (info) Has platform axes
    HAS_DIGITAL_IO_MODULES  = 14 # (info) Has digital input/output modules

    MODULE_ERROR_NO_ERROR               = 20 # (info) Modules - No error
    MODULE_ERROR_TEMPERATURE            = 21 # (info) Module error - Temperature
    MODULE_ERROR_EMERGENCY_STOP         = 22 # (info) Module error - Emergency stop / undervoltage
    MODULE_ERROR_MOTOR_NOT_ACTIVATED    = 23 # (info) Module error - Motor not activated
    MODULE_ERROR_COMMUNICATION          = 24 # (info) Module error - communication
    MODULE_ERROR_COUNTOURING            = 25 # (info) Module error - contouring error
    MODULE_ERROR_ENCODER                = 26 # (info) Module error - encoder error
    MODULE_ERROR_OVERCURRENT            = 27 # (info) Module error - overcurrent
    MODULE_ERROR_DRIVER                 = 28 # (info) Module error - driver error
    MODULE_ERROR_BUS_DEAD               = 29 # (info) Module error - Bus dead
    MODULE_ERROR_MODULE_DEAD            = 30 # (info) Module error - module dead
    # 31-36 (info) Module error - reserved for future errors
    KINEMATICS_ERROR_NO_ERROR                   = 37 # (info) Kinematics - no error
    KINEMATICS_ERROR_AXIS_LIMIT_MIN             = 38 # (info) Kinematics - axis limit min
    KINEMATICS_ERROR_AXIS_LIMIT_MAX             = 39 # (info) Kinematics - axis limit max
    KINEMATICS_ERROR_CENTRAL_AXIS_SINGULARITY   = 40 # (info) Kinematics - Central axis singularity
    KINEMATICS_ERROR_OUT_OF_RANGE               = 41 # (info) Kinematics - Out of range
    KINEMATICS_ERROR_WRIST_SINGULARITY          = 42 # (info) Kinematics - wrist singularity
    KINEMATICS_ERROR_VIRTUAL_BOX_REACHED        = 43 # (info) Kinematics - Virtual box reached
    KINEMATICS_ERROR_MOVEMENT_NOT_ALLOWD        = 44 # (info) Kinematics - Movement not allowed
    # 45-49 (info) Kinematics - reserved for future errors
    CAN_BUS_CONNECTION          = 50 # (rising edge) Is CAN bus connected? / Connect (1) / Disconnect (0) (Connect / Disconnect not possible with TinyCtrl)
    SHUTDOWN_CONTROL_COMPUTER   = 51 # (rising edge) Shutdown control computer
    RESET_ROBOT                 = 52 # (rising edge) Robot reset
    ENABLE_MOTORS               = 53 # (rising edge) Are the motors active? / Enable motors (1) / Disable motors (0)
    NORMAL_OPERATION            = 54 # (info) Normal operation (see operation mode, table 35)
    REFERENCE_AXES              = 60 # (rising edge) Are all axes referenced? / reference
    # 61-66 # (rising edge) Is robot axis referenced? / reference
    # 67-69 # (rising edge) Is external axis referenced? / reference
    # 70-72 (rising edge) Is gripper axis referenced? / reference 
    SET_ALL_AXES_TO_ZERO            = 73 #(rising edge) Set all axes to 0
    START_MOVE_TO_CARTESIAN         = 100 # (rising edge) Start MoveTo - cartesian
    START_MOVE_TO_CARTESIAN_BASE    = 101 # (rising edge) Start MoveTo - Cartesian relative base coordinates
    START_MOVE_TO_CARTESIAN_TOOL    = 102 # (rising edge) Start MoveTo - Cartesian relative tool coordinates
    START_MOVE_TO_JOINTS            = 103 # (rising edge) Start MoveTo - joint movement
    START_MOVE_TO_JOINTS_RELATIVE   = 104 # (rising edge) Start MoveTo - joint movement relative
    
    IS_ZERO_TORQUE_AVAILABLE            = 110 # (info) Is Zero-Torque (manual guidance mode) available?
    ENABLE_ZERO_TORQUE                  = 111 # (boolean) Is Zero-Torque enabled? / enable (1) / disable (0)
    IS_ROBOT_MOVING                     = 112 # (info) Is the robot moving?
    IS_ROBOT_PROGRAM_LOADED             = 120 # (info) Is a robot program loaded?
    IS_LOGIC_PROGRAM_LOADED             = 121 # (info) Is a logic program loaded?
    ROBOT_PROGRAM_START_OR_CONTINUE     = 122 # (rising edge) Is the robot program running? / start / continue
    ROBOT_PROGRAM_PAUSE                 = 123 # (rising edge) Is robot program paused? / pause
    ROBOT_PROGRAM_STOP                  = 124 # (rising edge) Is the robot program stopped? / stop
    # 130 # (rising edge) Select next directory entry
    # 131 # (rising edge) Select previous directory entry
    # 132 # (info) Is the selected directory entry a program file
    # 133 # (rising edge) Load selected directory entry as robot program / open directory
    # 134 # (rising edge) Go to the base directory (.../Data/Programs)
    # 135 # (rising edge) Unload robot program
    # 136 # (rising edge) Unload logic program
    # 200-299 # (boolean) Global signals
    # 300-363 # (boolean) Digital outputs
    # 364-427 # (info) Digital inputs

class InputReg(IntEnum):
    pass
    # 0 # (uint16) Software ID (902=iRC, 980=TinyCtrl)
    # 1 # (uint16) Software major version (e.g. 12)
    # 2 # (uint16) Software minor version (e.g. 6)
    # 3 # (uint16) Modbus mapping version
    # 4-5 # (uint32) minutes Uptime complete
    # 6-7 # (uint32) minutes Uptime last
    # 8-9 # (uint32) minutes Uptime enabled
    # 10-11 # (uint32) minutes Uptime movement
    # 12 # (uint16) Program starts
    # 13 # (uint16) 0.1ms Cycle time target
    # 14 # (uint16) 0.1ms Cycle time max (last 50 cycles)
    # 15 # (uint16) 0.01Hz Cycle frequency (average)
    # 16 # (uint16) 0.01% Workload
    # 20 # (uint16) Number of robot axes
    # 21 # (uint16) Number of external axes
    # 22 # (uint16) Number of gripper axes
    # 23 # (uint16) Number of platform axes
    # 24 # (uint16) Number of input/output modules
    # 25-30 # (bit field) Module error codes robot axes
    # 31-33 # (bit field) Module error codes external axes
    # 34-36 # (bit field) module error codes gripper axes
    # 37-40 # (bit field) module error codes platform axes
    # 41-43 # (bit field) module error codes input/output modules
    # 44-49 # (int16) 0.1°C Temperature electronics robot axes
    # 50-52 # (int16) 0.1°C Temperature electronics external axes
    # 53-55 # (int16) 0.1°C Temperature electronics gripper axes
    # 56-59 # (int16) 0.1°C Temperature electronics platform axes
    # 60-65 # (int16) 0.1°C Temperature motors robot axes
    # 66-68 # (int16) 0.1°C Temperature motors external axes
    # 69-71 # (int16) 0.1°C Temperature motors gripper axes
    # 72-75 # (int16) 0.1°C Temperature motors platform axes
    # 76-81 # (uint16) mA Currents robot axes
    # 82-84 # (uint16) mA Currents external axes
    # 85-87 # (uint16) mA Currents gripper axes
    # 88-91 # (uint16) mA Currents platform axes
    # 92 # (uint16) 0.01V Voltage
    # 93 # (uint16) mA Total Current
    # 94 # (uint16) 0.1% Battery charge (not in TinyCtrl)
    # 95 # (uint16) enum Kinematics - error code
    # 96 # (uint16) enum Operating mode

    # 130-135 # (int32) 0.01mm Current Cartesian position
    TARGET_POSITION_CART_X_LSB   = 130
    TARGET_POSITION_CART_X_MSB   = 131
    TARGET_POSITION_CART_Y_LSB   = 132
    TARGET_POSITION_CART_Y_MSB   = 133
    TARGET_POSITION_CART_Z_LSB   = 134
    TARGET_POSITION_CART_Z_MSB   = 135

    # 136-141 # (int16) 0.01° Actual cartesian orientation
    TARGET_ORIENTATION_CART_A_LSB = 136
    TARGET_ORIENTATION_CART_A_MSB = 137
    TARGET_ORIENTATION_CART_B_LSB = 138
    TARGET_ORIENTATION_CART_B_MSB = 139
    TARGET_ORIENTATION_CART_C_LSB = 140
    TARGET_ORIENTATION_CART_C_MSB = 141

    # 142-153 # (int32) 0.01 Actual robot axis position
    TARGET_POSITION_AXIS_A_LSB = 142
    TARGET_POSITION_AXIS_A_MSB = 143
    TARGET_POSITION_AXIS_B_LSB = 144
    TARGET_POSITION_AXIS_B_MSB = 145
    TARGET_POSITION_AXIS_C_LSB = 146
    TARGET_POSITION_AXIS_C_MSB = 147

    # 154-159 # (int32) 0.01 Actual axis position ext. axes
    # 160-165 # (int32) 0.01 Actual axis position of gripper axes
    # 166-173 # (int32) 0.01 Actual axis position platform
    # 262 # (uint16) Number of loaded robot programs
    # 263 # (int16) Number of current program, 0 for main program
    # 264 # (uint16) Number of instructions in current program

    # 265 # (int16) Number of current instruction, -1 if program is not running
    # 266 # enum Reason for last program stop or pause
    # 331 # (uint16) Number of entries in current directory
    # 333-364 # string Name of the selected directory entry
    # 365-396 # string Name of the current directory
    # 207-210 # (bit field) Digital inputs
    # 400-431 # string Info/error message short (as on manual control unit)
    # 440-455 # (int16) Number variables mb_num_r1 - mb_num_r16
    # 456-711 # (int16) 0.1 Position variables mb_pos_r1 - mb_pos_r16 (see sec. 12.4.4)

class HoldingReg(IntEnum):
    
    # Position is a 32bit value, writen to 2 16bit regs, so least and most significant bytes are needed
    # int32 0.01mm Target position cartesian
    TARGET_POSITION_CART_X_LSB   = 130
    TARGET_POSITION_CART_X_MSB   = 131
    TARGET_POSITION_CART_Y_LSB   = 132
    TARGET_POSITION_CART_Y_MSB   = 133
    TARGET_POSITION_CART_Z_LSB   = 134
    TARGET_POSITION_CART_Z_MSB   = 135

    # 136-141 # int16 0.01° Target orientation cartesian
    TARGET_ORIENTATION_CART_A_LSB = 136
    TARGET_ORIENTATION_CART_A_MSB = 137
    TARGET_ORIENTATION_CART_B_LSB = 138
    TARGET_ORIENTATION_CART_B_MSB = 139
    TARGET_ORIENTATION_CART_C_LSB = 140
    TARGET_ORIENTATION_CART_C_MSB = 141


    # 142-153 # int32 0.01 Target position robot axes
    TARGET_POSITION_AXIS_A_LSB = 142
    TARGET_POSITION_AXIS_A_MSB = 143
    TARGET_POSITION_AXIS_B_LSB = 144
    TARGET_POSITION_AXIS_B_MSB = 145
    TARGET_POSITION_AXIS_C_LSB = 146
    TARGET_POSITION_AXIS_C_MSB = 147

# 154-159 # int32 0.01 Target position external axes
# 174-177 # int32 0.01mm Target position platform
# 178-179 # int32 0.01° Target orientation platform
    MOVE_SPEED = 180 # int16 0.1 Speed for MoveTo (percent or mm/s)
# 181-186 # int32 0.1 Target velocity of ext. axes in velocity mode
# 181-186 # uint16 0.01% Velocity override
    MOVE_SPEED_OVERRIDE = 187 # int16 0.1 Speed for MoveTo (percent or mm/s)
# 188 # enum Jog mode
    ROBOT_PROGRAM_RUN_STATE = 260 # enum Robot program RunState
    ROBOT_PROGRAM_REPLAY_MODE = 261 # enum Robot program Replay mode
    ROBOT_PROGRAM_NAME_START    = 267 # 267-298 # string Name of loaded robot program / load on write
    ROBOT_PROGRAM_NAME_END      = 298 # 267-298 # string Name of loaded robot program / load on write
# 299-330 # string Name of the loaded logic program / load on write
# 332 # uint16 Number of the selected directory entry
# 200-206 # bit field Global signals
# 207-210 # bit field Digital outputs
# 440-455 # int16 Number variables mn_num_w1 - mb_num_w16
# 456-711 # int16 0.1 Position variables mb_pos_w1 - mb_pos_w16 (see sec. 12.4.4)