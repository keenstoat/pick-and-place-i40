
from time import sleep, time
from pyModbusTCP.client import ModbusClient
from ctypes import c_int32
from math import sin, cos, radians
from numpy import arange, linspace

from .registers import Coils, HoldingReg, InputReg


class DeltaRobot:
    is_connected = False

    def __init__(self, modbus_ip_address:str, port:int=502):
        """
        Initialize a Robot instance and establish the communication

        :param address: The IP address of the Robot.
        :type address: str
        :param port: The port for Modbus TCP communication (default is 502).
        :type port: int
        """
        self.address = modbus_ip_address
        self.modbus_client = ModbusClient(host=modbus_ip_address, port=port, timeout=1)
        self.is_connected = self.modbus_client.open()
        self._fail_if_not_connected()

    def __del__(self):
        """
        Close current TCP connection.

        :return: None
        """
        self.set_global_signal(6, False)
        self.modbus_client.close()

    def _fail_if_not_connected(self, retries=3):
        if self.modbus_client.is_open:
            return
        
        for i in range(retries):
            if self.modbus_client.open():
                return
            if i < retries-1: sleep(1)

        assert self.modbus_client.open(), f"DeltaRobot instance could not connect after {retries} retries"
        
    def _send_rising_edge(self, reg_address):
        self.modbus_client.write_single_coil(reg_address, False)
        self.modbus_client.write_single_coil(reg_address, True)
        
    def _log(self, *msg):

        print(*msg)

    def shutdown(self):
        """
        Shutdown the Delta Robot
        """
        self._fail_if_not_connected()

        self.modbus_client.write_single_coil(Coils.SHUTDOWN_CONTROL_COMPUTER, False)
        self.modbus_client.write_single_coil(Coils.SHUTDOWN_CONTROL_COMPUTER, True)

    def reset(self):

        self._fail_if_not_connected()
        self.stop_robot_program()
        self._send_rising_edge(Coils.RESET_ROBOT)

    def is_enabled(self):

        self._fail_if_not_connected()
        return bool(self.modbus_client.read_coils(Coils.ENABLE_MOTORS)[0])
    
    def enable(self):

        self._fail_if_not_connected()

        if self.is_enabled():
            return
        
        self._send_rising_edge(Coils.ENABLE_MOTORS)
        while not self.is_enabled(): sleep(0.1)

    def disable(self):
        self._fail_if_not_connected()

        if not self.is_enabled():
            return
        
        self._send_rising_edge(Coils.ENABLE_MOTORS)
        while self.is_enabled(): sleep(0.1)
    
    def reference(self, max_delay_ms=1_000_000):

        self._fail_if_not_connected()

        if self.is_referenced():
            return

        self._send_rising_edge(Coils.REFERENCE_AXES)

        self._log("Referencing robot now. This might take a while...")
        timeout = time() + max_delay_ms/1000
        while not self.is_referenced() and time() < timeout:
            sleep(0.5)

        return self.is_referenced()

    def is_referenced(self):

        self._fail_if_not_connected()
        
        return bool(self.modbus_client.read_coils(Coils.REFERENCE_AXES)[0])

    def is_moving(self):

        self._fail_if_not_connected()
        return bool(self.modbus_client.read_coils(Coils.IS_ROBOT_MOVING)[0])

    def set_override_velocity(self, velocity_percentage:int=20):
        self._fail_if_not_connected()

        # override velocity percentage has a precision of 0.01% so it needs to be multiplied by 100
        if 0 < velocity_percentage <= 100:
            self.modbus_client.write_single_register(HoldingReg.MOVE_SPEED_OVERRIDE, velocity_percentage * 100)
            return True
        return False
    
    def set_velocity(self, velocity:int):
        """
        Set the velocity of the Robot.

        This method sets the velocity of the robot in millimeters per second.
        For cartesian motions the value is set as a multiple of 1mm/s,
        for joint motions it is a multiple of 1% (relative to the maximum velocity)
        The actual motion speed also depends on the global override value (holding register 187).

        :param velocity: The desired velocity in millimeters per second (or in percent).
        :type velocity: float
        :return: None
        """
        self._fail_if_not_connected()

        self.modbus_client.write_single_register(HoldingReg.MOVE_TO_SPEED, velocity * 10)

    # Cartesian movement functions =====================================================================================
    
    def set_target_position_cart(self, x:float, y:float, z:float):
        
        self._fail_if_not_connected()
        
        x = int(x * 100)
        y = int(y * 100)
        z = int(z * 100)

        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_CART_X_LSB, (x & 0x0000FFFF))
        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_CART_X_MSB, (x >> 16) & 0x0000FFFF)

        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_CART_Y_LSB, (y & 0x0000FFFF))
        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_CART_Y_MSB, (y >> 16) & 0x0000FFFF)

        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_CART_Z_LSB, (z & 0x0000FFFF))
        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_CART_Z_MSB, (z >> 16) & 0x0000FFFF)

    def get_target_position_cart(self):

        self._fail_if_not_connected()

        x1 = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_CART_X_LSB)[0]
        x2 = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_CART_X_MSB)[0]
        y1 = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_CART_Y_LSB)[0]
        y2 = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_CART_Y_MSB)[0]
        z1 = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_CART_Z_LSB)[0]
        z2 = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_CART_Z_MSB)[0]
        # Combine the two 16-bit values into a 32-bit integer for each position
        # Values are in units of 0.01mm, and have to be returned in units of 1mm
        x1 = c_int32(x1 | (x2 << 16)).value / 100
        y1 = c_int32(y1 | (y2 << 16)).value / 100
        z1 = c_int32(z1 | (z2 << 16)).value / 100
        return x1, y1, z1

    def set_target_orientation_cart(self, a: float, b: float, c: float):
        # TODO check if this function is needed - delta robot does not have orientation of the end effector
        self._fail_if_not_connected()

        a *= 100
        b *= 100
        c *= 100

        self.modbus_client.write_single_register(HoldingReg.TARGET_ORIENTATION_CART_A_LSB, a)
        self.modbus_client.write_single_register(HoldingReg.TARGET_ORIENTATION_CART_B_LSB, b)
        self.modbus_client.write_single_register(HoldingReg.TARGET_ORIENTATION_CART_C_LSB, c)

    def get_target_orientation_cart(self):
        
        self._fail_if_not_connected()

        a = self.modbus_client.read_input_registers(InputReg.TARGET_ORIENTATION_CART_A_LSB)[0] / 100
        b = self.modbus_client.read_input_registers(InputReg.TARGET_ORIENTATION_CART_B_LSB)[0] / 100
        c = self.modbus_client.read_input_registers(InputReg.TARGET_ORIENTATION_CART_C_LSB)[0] / 100
        return a, b, c

    def start_move_to_cartesian(self, relative_to:str=None, max_delay_ms:int=10_000_000):

        assert isinstance(max_delay_ms, int), f"The max_delay_value must be an int"

        self._fail_if_not_connected()

        if relative_to is None:
            self.modbus_client.write_single_coil(Coils.START_MOVE_TO_CARTESIAN, False)
            self.modbus_client.write_single_coil(Coils.START_MOVE_TO_CARTESIAN, True)
        elif relative_to == "base":
            self.modbus_client.write_single_coil(Coils.START_MOVE_TO_CARTESIAN_BASE, False)
            self.modbus_client.write_single_coil(Coils.START_MOVE_TO_CARTESIAN_BASE, True)
        elif relative_to == "tool":
            self.modbus_client.write_single_coil(Coils.START_MOVE_TO_CARTESIAN_TOOL, False)
            self.modbus_client.write_single_coil(Coils.START_MOVE_TO_CARTESIAN_TOOL, True)
        else:
            raise Exception("Relative to value must be None, 'base', or 'tool'")
        
        if max_delay_ms > 0:
            timeout = time() + max_delay_ms/1000
            while self.is_moving() and time() < timeout:
                self._log("moving to > ", self.get_target_position_cart())
                sleep(0.1)

    # Axis movement functions ==========================================================================================
    
    def set_target_position_axes(self, a1:float, a2:float, a3:float):

        self._fail_if_not_connected()

        a1 = int(a1 * 100)
        a2 = int(a2 * 100)
        a3 = int(a3 * 100)

        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_AXIS_A_LSB, (a1 & 0x0000FFFF))
        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_AXIS_A_MSB, (a1 >> 16) & 0x0000FFFF)

        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_AXIS_B_LSB, (a2 & 0x0000FFFF))
        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_AXIS_B_MSB, (a2 >> 16) & 0x0000FFFF)

        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_AXIS_C_LSB, (a3 & 0x0000FFFF))
        self.modbus_client.write_single_register(HoldingReg.TARGET_POSITION_AXIS_C_MSB, (a3 >> 16) & 0x0000FFFF)

    def get_target_position_axes(self):
        self._fail_if_not_connected()
        
        a1_lsb = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_AXIS_A_LSB)[0]
        a1_msb = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_AXIS_A_MSB)[0]
        a2_lsb = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_AXIS_B_LSB)[0]
        a2_msb = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_AXIS_B_MSB)[0]
        a3_lsb = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_AXIS_C_LSB)[0]
        a3_msb = self.modbus_client.read_input_registers(InputReg.TARGET_POSITION_AXIS_C_MSB)[0]

        # Combine the two 16-bit values into a 32-bit integer for each axis
        a1 = c_int32(a1_lsb | (a1_msb << 16)).value / 100
        a2 = c_int32(a2_lsb | (a2_msb << 16)).value / 100
        a3 = c_int32(a3_lsb | (a3_msb << 16)).value / 100
        return a1, a2, a3

    def start_move_to_axes(self, relative:bool=False, max_delay_ms:int=10_000_000):

        self._fail_if_not_connected()

        if relative:
            self._send_rising_edge(Coils.START_MOVE_TO_JOINTS_RELATIVE)
        else:
            self._send_rising_edge(Coils.START_MOVE_TO_JOINTS)

        if max_delay_ms > 0:
            timeout = time() + max_delay_ms/1000
            while self.is_moving() and time() < timeout:
                sleep(0.01)
    
    # Robot programs ===================================================================================================

    def start_robot_program(self):

        self._fail_if_not_connected()
        self._send_rising_edge(Coils.ROBOT_PROGRAM_START_OR_CONTINUE)

    def pause_robot_program(self):

        self._fail_if_not_connected()
        self._send_rising_edge(Coils.ROBOT_PROGRAM_PAUSE)

    def stop_robot_program(self):

        self._fail_if_not_connected()
        self._send_rising_edge(Coils.ROBOT_PROGRAM_STOP)

    def get_robot_program_runstate(self):

        self._fail_if_not_connected()

        code = self.modbus_client.read_holding_registers(HoldingReg.ROBOT_PROGRAM_RUN_STATE)[0]
        match code:
            case 0: return "Program is not running"
            case 1: return "Program is running"
            case 2: return "Program is paused"
            case _: return f"Unknown robot program state: '{code}'"

    def set_robot_program_replay_mode(self, mode):
        
        self._fail_if_not_connected()

        if mode == "once":
            self.modbus_client.write_single_register(HoldingReg.ROBOT_PROGRAM_REPLAY_MODE, 0)
        elif mode == "repeat":
            return self.modbus_client.write_single_register(HoldingReg.ROBOT_PROGRAM_REPLAY_MODE, 1)
        elif mode == "step":
            return self.modbus_client.write_single_register(HoldingReg.ROBOT_PROGRAM_REPLAY_MODE, 2)
        elif mode == "fast":
            return self.modbus_client.write_single_register(HoldingReg.ROBOT_PROGRAM_REPLAY_MODE, 3)
        else:
            return False

    def get_program_replay_mode(self):

        self._fail_if_not_connected()

        code = self.modbus_client.read_holding_registers(HoldingReg.ROBOT_PROGRAM_REPLAY_MODE)[0]
        match code:
            case 0: return "Run program once"
            case 1: return "Repeat program"
            case 2: return "Execute instructions step by step"
            case 3: return "Fast (not used)"
            case _: return f"Unknown robot program replay mode: '{code}'"

    def set_robot_program_name(self, name):

        self._fail_if_not_connected()
        self.write_string_to_holding_regs(name, HoldingReg.ROBOT_PROGRAM_NAME_START)

    def get_robot_program_name(self):

        self._fail_if_not_connected()

        int_list = self.modbus_client.read_holding_registers(HoldingReg.ROBOT_PROGRAM_NAME_START, 32)
        return self.read_string(int_list)

    def is_robot_program_loaded(self):
        self._fail_if_not_connected()
        return bool(self.modbus_client.read_coils(Coils.IS_ROBOT_PROGRAM_LOADED)[0])

    def get_list_of_porgrams(self):
        
        self._fail_if_not_connected()

        num_programs = self.modbus_client.read_input_registers(InputReg.NUMBER_OF_ENTRIES_IN_CURRENT_DIR)[0]

        # Ensure that the list starts from the top by repeatedly navigating to the previous program
        for _ in range(num_programs):
            self._send_rising_edge(Coils.SELECT_PREVIOUS_DIR_ENTRY)

        # Loop through the program indices
        program_list = []
        for _ in range(num_programs):
            program_name = self.read_string(self.modbus_client.read_input_registers(InputReg.NAME_OF_SELECTED_DIRECTORY_ENTRY_START, 32))
            # Remove null characters from the program name
            program_name = str(program_name).replace("\x00", "")
            program_list.append(program_name)
            self._send_rising_edge(Coils.SELECT_NEXT_DIR_ENTRY)

        return program_list

    def get_number_of_loaded_robot_programs(self):

        self._fail_if_not_connected()
        return self.modbus_client.read_input_registers(InputReg.NUMBER_OF_LOADED_ROBOT_PROGRAMS)[0]

    def get_number_of_current_robot_program(self):
        self._fail_if_not_connected()
        return self.modbus_client.read_input_registers(InputReg.NUMBER_OF_CURRENT_ROBOT_PROGRAM)[0]

    # Errors and info functions ========================================================================================

    def has_module_error(self):

        self._fail_if_not_connected()
        return not bool(self.modbus_client.read_coils(Coils.MODULE_ERROR_NO_ERROR)[0])

    def has_kinematics_error(self):

        self._fail_if_not_connected()
        return not bool(self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_NO_ERROR)[0])

    def get_module_error_list(self):

        self._fail_if_not_connected()
        errors_list = []

        if self.modbus_client.read_coils(Coils.MODULE_ERROR_NO_ERROR)[0]:
            return []
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_TEMPERATURE)[0]:
            errors_list.append("Temperature")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_EMERGENCY_STOP)[0]:
            errors_list.append("Emergency stop")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_MOTOR_NOT_ACTIVATED)[0]:
            errors_list.append("Motor not activated")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_COMMUNICATION)[0]:
            errors_list.append("Communication")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_COUNTOURING)[0]:
            errors_list.append("Contouring error")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_ENCODER)[0]:
            errors_list.append("Encoder error")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_OVERCURRENT)[0]:
            errors_list.append("Overcurrent")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_DRIVER)[0]:
            errors_list.append("Driver error")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_BUS_DEAD)[0]:
            errors_list.append("Bus dead")
        if self.modbus_client.read_coils(Coils.MODULE_ERROR_MODULE_DEAD)[0]:
            errors_list.append("Module dead")

        return errors_list

    def get_kinematics_error(self):

        self._fail_if_not_connected()

        error_code = self.modbus_client.read_input_registers(InputReg.KINEMATICS_ERROR_CODE)[0]
        match error_code:
            case 00: return "" # No error
            case 13: return "Axis limit Min"
            case 14: return "Axis limit max"
            case 21: return "Central axis singularity"
            case 22: return "Out of range"
            case 23: return "Wrist singularity"
            case 30: return "Virtual box violated in X+"
            case 31: return "Virtual box violated in X-"
            case 32: return "Virtual box violated in Y+"
            case 33: return "Virtual box violated in Y-"
            case 34: return "Virtual box violated in Z+"
            case 35: return "Virtual box violated in Z-"
            case 50: return "NAN in calculation"
            case 90: return "Motion not allowed"
            case 65535: return "Unknown error" #(0xFFFF)

    def get_kinematics_error_list(self):

        self._fail_if_not_connected()
        errors_list = []

        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_NO_ERROR)[0]:
            return [] # No error
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_AXIS_LIMIT_MIN)[0]:
            errors_list.append("Axis limit Min") 
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_AXIS_LIMIT_MAX)[0]:
            errors_list.append("Axis limit Max")
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_CENTRAL_AXIS_SINGULARITY)[0]:
            errors_list.append("Central axis singularity")
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_OUT_OF_RANGE)[0]:
            errors_list.append("Out of range")
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_WRIST_SINGULARITY)[0]:
            errors_list.append("Wrist singularity")
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_VIRTUAL_BOX_REACHED)[0]:
            errors_list.append("Virtual box reached")
        if self.modbus_client.read_coils(Coils.KINEMATICS_ERROR_MOVEMENT_NOT_ALLOWED)[0]:
            errors_list.append("Motion not allowed")
        
        return errors_list

    def get_info_or_message(self):

        self._fail_if_not_connected()
        msg = self.modbus_client.read_holding_registers(InputReg.INFO_OR_ERROR_SHORT_MESSAGE_START, 32)
        return self.read_string(msg)

    # Gripper ==========================================================================================================
    def control_gripper(self, opening:int, orientation:int, signal:int=6):
        """
        Control the gripper using specified values and a Modbus signal.

        :param opening: The value for the gripper opening.
        :type opening: int
        :param orientation: The value for the gripper orientation.
        :type orientation: int
        :param signal: The Modbus signal number to enable/disable gripper control.
                       Default is 6.
        :type signal: int
        :return: True if the gripper control was successful, False otherwise.
        :rtype: bool
        """
        self._fail_if_not_connected()

        self.set_number_variables(15, opening)
        self.set_number_variables(16, orientation)

        self.set_global_signal(signal, True)
        sleep(0.2)
        self.set_global_signal(signal, False)


    def is_gripper_moving(self):
        return self.get_global_signal(7)


    #  Utility functions =======================================================================

    def move_cartesian(self, x:int, y:int, z:int, velocity:int=None, max_delay_ms=10_000_000, relative_to=None):
        self._fail_if_not_connected()
        
        if velocity:
            self.set_velocity(velocity)

        self.set_target_position_cart(x, y, z)
        self.start_move_to_cartesian(relative_to=relative_to, max_delay_ms=max_delay_ms)

    def move_circular(self, radius:float, angle_step:float=0.5, start_angle:float=0, stop_angle:float=360):
        self._fail_if_not_connected()
        
        x_offset, y_offset, z_offset = self.get_target_position_cart()
        for angle in linspace(start_angle, stop_angle, angle_step):
            x = radius * cos(radians(angle)) + x_offset
            y = radius * sin(radians(angle)) + y_offset

            self.set_target_position_cart(x, y, z_offset)
            self.start_move_to_cartesian()

    def write_string_to_holding_regs(self, string, regs_address):

        self._fail_if_not_connected()

        # the string max length is 32 words (word = 16bits). Each character is 8 bits, so 64 is max length of string
        length = 64

        assert len(string) <= length, f"string to write must be {length} characters of fewer"

        # if string is not full of characters, then fill it up with nulls
        if len(string) < length:
            padding = length - len(string)
            string += "\x00" * padding
        
        int_list = []
        for i in range(0, length, 2): 
            int_value =  ord(string[i+1]) << 8 | (ord(string[i]) & 0x00FF)
            int_list.append(int_value)

        assert len(int_list) == 32, "Int list must have 32 elements"
        self.modbus_client.write_multiple_registers(regs_address, int_list)

    def read_string(self, int_list):

        self._fail_if_not_connected()

        # Each  input reg is a word (word = 16bits). Each character in the string is encoded in 8 bits.
        # There are 2 characters in each word. 
        # So for each word, the MSB and the LSB are converted to a char and concatenated.
        return "".join(list(map(lambda int_val: chr(int_val & 0x00FF) + chr(int_val >> 8), int_list)))
        



    # Reviewed but unused functions ====================================================================================

    def is_zero_torque_available(self):
        
        self._fail_if_not_connected()
        return bool(self.modbus_client.read_coils(Coils.IS_ZERO_TORQUE_AVAILABLE)[0])
    
    def is_zero_torque_enabled(self):
        
        self._fail_if_not_connected()
        return bool(self.modbus_client.read_coils(Coils.ENABLE_ZERO_TORQUE)[0])

    def set_zero_torque(self, enable:bool=True):
        self._fail_if_not_connected()

        # TODO check logic - may need to reference the robot after enabling zero torque
        self.modbus_client.write_single_coil(Coils.ENABLE_ZERO_TORQUE, enable)
        # if enable & (not self.is_zero_torque_enabled()):
        #     self.client.write_single_coil(111, False)
        #     self.client.write_single_coil(Coils.ENABLE_ZERO_TORQUE, True)
        # elif not enable & (self.is_zero_torque_enabled()):
        #     self.client.write_single_coil(111, False)
        #     self.reset()
        #     sleep(0.2)
        #     self.enable()

    # Un-reviewed Functions ============================================================================================

    

    def set_global_signal(self, number: int, state: bool):
        """
        Set the state of a global signal.

        This method allows you to set the state of a global signal by specifying its number and state.

        :param number: The number of the global signal (1 to 100).
        :type number: int
        :param state: The state to set (True for ON, False for OFF).
        :type state: bool
        """
        if not self.is_connected:
            return
        if 1 <= number <= 100:
            self.modbus_client.write_single_coil(199 + number, state)

    def set_digital_output(self, number: int, state: bool):
        """
        Set the state of a digital output.

        This method allows you to set the state of a digital output by specifying its number and state.

        :param number: The number of the digital output (1 to 64).
        :type number: int
        :param state: The state to set (True for ON, False for OFF).
        :type state: bool
        """
        if not self.is_connected:
            return False
        number += 20
        if 1 <= number <= 64:
            return self.modbus_client.write_single_coil(299 + number, state)
        else:
            return False

    def get_global_signal(self, number: int):
        """
        Get the state of a global signal.

        This method allows you to get the state of a global signal by specifying its number.

        :param number: The number of the global signal (1 to 100).
        :type number: int
        :return: The state of the global signal (True for ON, False for OFF).
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if 1 <= number <= 100:
            return self.modbus_client.read_coils(199 + number)[0]
        else:
            return False

    def get_digital_output(self, number):
        """
        Get the state of a digital output.

        This method allows you to get the state of a digital output by specifying its number.

        :param number: The number of the digital output (1 to 64).
        :type number: int
        :return: The state of the digital output (True for ON, False for OFF).
        :rtype: bool
        """
        if not self.is_connected:
            return False
        number += 20
        if 1 <= number <= 64:
            return self.modbus_client.read_coils(299 + number)[0]
        else:
            return False

    def get_digital_input(self, number: int):
        """
        Get the state of a digital input.

        This method allows you to get the state of a digital input by specifying its number.

        :param number: The number of the digital input (1 to 64).
        :type number: int
        :return: The state of the digital input (True for ON, False for OFF).
        :rtype: bool
        """
        if not self.is_connected:
            return False
        number += 20
        if 1 <= number <= 64:
            return self.modbus_client.read_coils(263 + number)[0]
        else:
            return False

    def set_number_variables(self, number: int = 1, value: int = 0):
        """
        Set the value of a writable Modbus variable.

        This method allows you to set the value of a Modbus variable for program use. Please note that
        the variable name in your program should follow the naming convention: mb_num_w1 - mb_num_w16.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :param value: The value to set for the Modbus variable.
        :type value: int
        :return: True if the operation was successful, False if the number is out of range.
        :rtype: bool
        """
        if not self.is_connected:
            return
        if 1 <= number <= 16:
            return self.modbus_client.write_single_register(439 + number, value)

    def set_position_variable(
        self,
        number=1,
        movement: str = "cartesian",
        a1: int = None,
        a2: int = None,
        a3: int = None,
        x: int = None,
        y: int = None,
        z: int = None,
        a: int = 0,
        b: int = 0,
        c: int = 180,
        conversion: int = 0,
    ):
        """
        Set the target position for robot movement in a robot program.

        This method allows you to set the target position for robot movement in a program. You can specify
        the target position either in Cartesian or axis values. Ensure the variable name in your program
        follows the naming convention, e.g., mb_pos_w1.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :param movement: The type of movement (either "cartesian" or "axes").
        :type movement: str
        :param a1: The value of axis A1 (if movement is "axes").
        :type a1: int
        :param a2: The value of axis A2 (if movement is "axes").
        :type a2: int
        :param a3: The value of axis A3 (if movement is "axes").
        :type a3: int
        :param x: The X-coordinate value (if movement is "cartesian").
        :type x: int
        :param y: The Y-coordinate value (if movement is "cartesian").
        :type y: int
        :param z: The Z-coordinate value (if movement is "cartesian").
        :type z: int
        :param a: The orientation A value (if movement is "cartesian").
        :type a: int
        :param b: The orientation B value (if movement is "cartesian").
        :type b: int
        :param c: The orientation C value (if movement is "cartesian").
        :type c: int
        :param conversion: The conversion type (useful for converting between joint and cartesian positions).
        :type conversion: int
        :return: True if the operation was successful, False if the number is out of range or invalid parameters.
        :rtype: bool
        """
        if not self.is_connected:
            return
        if not (1 <= number <= 16):
            return False
        number = 456 + (16 * (number - 1))
        if movement == "cartesian":
            x *= 10
            y *= 10
            z *= 10
            a *= 10
            b *= 10
            c *= 10
            return self.modbus_client.write_multiple_registers(
                number, [0, 0, 0, 0, 0, 0, 0, 0, 0,
                         x, y, z, a, b, c, conversion]
            )
        elif movement == "axes":
            a1 *= 10
            a2 *= 10
            a3 *= 10
            return self.modbus_client.write_multiple_registers(
                number, [a1, a2, a3, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, conversion]
            )
        else:
            return False

    def get_readable_number_variable(self, number: int):
        """
        Get the value of a readable Modbus variable.

        This method allows you to retrieve the value of a Modbus variable for reading. Please ensure that
        the variable name in your program follows the naming convention: mb_num_r1 - mb_num_r16.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: The value of the Modbus variable, or False if the number is out of range.
        :rtype: int or bool
        """
        if not self.is_connected:
            return 0
        if 1 <= number <= 16:
            return self.modbus_client.read_input_registers(439 + number)[0]
        else:
            return 0

    def get_writable_number_variable(self, number: int):
        """
        Get the value of a writable Modbus variable.

        This method allows you to retrieve the value of a Modbus variable for writing. Ensure that the
        variable name in your program adheres to the naming convention: mb_num_w1 - mb_num_w16.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: The value of the Modbus variable, or False if the number is out of range.
        :rtype: int or bool
        """
        if not self.is_connected:
            return
        if 1 <= number <= 16:
            return self.modbus_client.read_holding_registers(439 + number)[0]
        else:
            return False

    def get_readable_position_variable(self, number: int):
        """
        Get the value of a readable position Modbus variable.

        This method allows you to retrieve the value of a readable position Modbus variable.
        Ensure that the variable name in your program follows the naming convention, e.g., mb_pos_r1.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: A list containing axis, cartesian, orientation values, and conversion type,
                 or False if the number is out of range.
        :rtype: list
        """
        if not self.is_connected:
            return []
        if not (1 <= number <= 16):
            return []
        number = 456 + (16 * (number - 1))
        postion = self.modbus_client.read_input_registers(number, 16)
        if not postion:
            return []
        axes = {"a1": postion[0], "a2": postion[1], "a3": postion[2]}
        cartesian = {
            "x_val": postion[9],
            "y_val": postion[10],
            "z_val": postion[11],
        }
        orientation = {"a": postion[12], "b": postion[13], "c": postion[14]}
        conversion = postion[15]
        return [axes, cartesian, orientation, conversion]

    def get_writable_position_variable(self, number: int):
        """
        Get the value of a writable position Modbus variable.

        This method allows you to retrieve the value of a writable position Modbus variable.
        Ensure that the variable name in your program follows the naming convention, e.g., mb_pos_w1.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: A list containing axis, cartesian, orientation values, and conversion type,
                 or False if the number is out of range.
        :rtype: list
        """
        if not self.is_connected:
            return []
        if not (1 <= number <= 16):
            return []
        number = 456 + (16 * (number - 1))
        postion = self.modbus_client.read_holding_registers(number, 16)
        if not postion:
            return []
        axes = {"a1": postion[0] / 10,
                "a2": postion[1] / 10, "a3": postion[2] / 10}
        cartesian = {
            "x_val": postion[9] / 10,
            "y_val": postion[10] / 10,
            "z_val": postion[11] / 10,
        }
        orientation = {
            "a": postion[12] / 10,
            "b": postion[13] / 10,
            "c": postion[14] / 10,
        }
        conversion = postion[15]
        return [axes, cartesian, orientation, conversion]

    
    
    def get_stop_reason_description(self):
        """
        Get a description of the reason for the robot's current stop condition.

        This method reads the stop reason code from the robot controller and returns a human-readable description of the reason for the stop.

        :return: A string describing the reason for the stop.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        code = self.modbus_client.read_input_registers(266)[0]
        if code == 0:
            return "User (Teach pendant, CRI, Modbus, etc.)"
        if code == 1:
            return "PLC"
        if code == 2:
            return "Program (stop/pause instruction)"
        if code == 3:
            return "Replay Step (step operation)"
        if code == 4:
            return "Shoutdown (system shuts down)"
        if code == 100:
            return "Error"
        if code == 101:
            return "Path generator error 1"
        if code == 102:
            return "Path generator error 2"
        if code == 103:
            return "Error in state machine"
        else:
            return ""

    def get_operation_mode(self):
        """
        Get the operation mode description.

        This method reads the operation mode code from the robot controller and returns a human-readable description of the mode.

        :return: A string describing the operation mode.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        code = self.modbus_client.read_input_registers(96)[0]
        if code == 0:
            return "Standard - normal operation"
        if code == 1:
            return "Serious error, control must be restarted"
        if code == 2:
            return "CAN-Bridge (CRI, e.g. retrieve firmware parameters)"
        else:
            return ""

    
    def print_list_of_programs(self):
        """
        Print a list of available robot programs.

        This method retrieves a list of robot programs and prints them to the console.
        If the robot is not connected, it will return without performing any action.

        :return: None
        """
        if not self.is_connected:
            return
        list = self.get_list_of_porgrams()
        for count, i in enumerate(list):
            print(count, i)

   
    def change_table_hight(self, direction: int = 0, movement_time: int = 0, signal: int = 6):
        if not self.is_connected:
            return False
        self.set_number_variables(13, direction)
        self.set_number_variables(14, movement_time)
        self.set_global_signal(signal, True)
        sleep(0.2)
        self.set_global_signal(signal, False)
        return True



   