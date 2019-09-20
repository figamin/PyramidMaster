import serial
# opcode constants
# MODES
SAFE_MODE = "131"
FULL_MODE = "132"
# CLEANING
CLEAN = "135"
MAX = "136"
SPOT = "134"
SEEK_DOCK = "143"
POWER_OFF = "133"
# ACTUATOR
DRIVE = "137"
DRIVE_DIRECT = "145"
MOTORS = "138"
LED = "139"
SONG = "140"
# SPECIAL DRIVE VALUES
DRIVE_STRAIGHT_VALUE = 32768
DRIVE_CLOCKWISE_VALUE = -1
DRIVE_COUNTERCLOCKWISE_VALUE = 1
# SPECIAL MOTOR VALUES
SIDEBRUSH_COUNTERCLOCKWISE_VALUE = 0
SIDEBRUSH_CLOCKWISE_VALUE = 3
MAINBRUSH_INWARD_VALUE = 2
MAINBRUSH_OUTWARD_VALUE = 4
VACUUM_VALUE = 1
# INPUT COMMANDS
SENSORS = "142"
QUERY_LIST = "149"
STREAM = "148"
PAUSE_RESUME_STREAM = "150"
# PACKET ID LIST
BUMPS_AND_WHEEL_DROPS = "7"
WALL = "8"
CLIFF_LEFT = "9"
CLIFF_FRONT_LEFT = "10"
CLIFF_FRONT_RIGHT = "11"
CLIFF_RIGHT = "12"
VIRTUAL_WALL = "13"
WHEEL_OVERCURRENTS = "14"
DIRT_DETECT = "15"
INFARED_CHAR_OMNI = "17"
INFARED_CHAR_LEFT = "52"
INFARED_CHAR_RIGHT = "53"
DISTANCE_TRAVELLED = "19"
DEGREES_TURNED = "20"
BATTERY_VOLTAGE_MV = "22"
BATTERY_CURRENT_MA = "23"
BATTERY_TEMPERATURE_CELSIUS = "24"
BATTERY_CHARGE_MAH = "25"
BATTERY_CAPACITY_MAH = "26"
connect = None


"""Converts given integer into a tuple of the corresponding two's compliment."""
def int_to_twos_complement(num):
    if num < 0:
        hex_num = hex((1 << 16) + num)[2:]
    else:
        hex_num = hex(num)[2:]
    if len(hex_num) > 2:
        hex_num_1 = hex_num[:-2]
        hex_num_2 = hex_num[-2:]
    else:
        hex_num_1 = "0"
        hex_num_2 = hex_num
    int_num_1 = int(hex_num_1, 16)
    int_num_2 = int(hex_num_2, 16)
    return str(int_num_1), str(int_num_2)


"""Drives the Roomba using given velocity and turning radius."""
def drive_command(velocity, radius):
    if (velocity <= 500 or velocity >= -500)\
            and (radius <= 2000 or radius >= 2000 or radius == DRIVE_STRAIGHT_VALUE):
        velocity_1, velocity_2 = int_to_twos_complement(velocity)
        radius_1, radius_2 = int_to_twos_complement(radius)
        send_commands(DRIVE + " " + velocity_1 + " " + velocity_2 + " " + radius_1 + " " + radius_2)


"""Drives the roomba using given right and left wheel velocities"""
def drive_direct_command(right_velocity, left_velocity):
    if 500 >= (right_velocity and left_velocity) >= -500:
        right_1, right_2 = int_to_twos_complement(right_velocity)
        left_1, left_2 = int_to_twos_complement(left_velocity)
        send_commands(DRIVE_DIRECT + " " + right_1 + " " + right_2 + " " + left_1 + " " + left_2)


# def motors_command(selected_motor, power_state)
"""Sends given commands to the Roomba."""
def send_commands(commands):
    print(commands)
    full_command = ""
    for i in commands.split():
        full_command += chr(int(i))
    connect.write(full_command)



try:
    connect = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
    print("Connection Successful!\n")

except serial.SerialException:
    print("Connection Failed.\n")

drive_command(-200, 500)

