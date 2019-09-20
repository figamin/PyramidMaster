import serial
import ropcodes
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
            and (radius <= 2000 or radius >= 2000 or radius == ropcodes.DRIVE_STRAIGHT_VALUE):
        velocity_1, velocity_2 = int_to_twos_complement(velocity)
        radius_1, radius_2 = int_to_twos_complement(radius)
        send_commands(ropcodes.DRIVE + " " + velocity_1 + " " + velocity_2 + " " + radius_1 + " " + radius_2)


"""Drives the roomba using given right and left wheel velocities"""
def drive_direct_command(right_velocity, left_velocity):
    if 500 >= (right_velocity and left_velocity) >= -500:
        right_1, right_2 = int_to_twos_complement(right_velocity)
        left_1, left_2 = int_to_twos_complement(left_velocity)
        send_commands(ropcodes.DRIVE_DIRECT + " " + right_1 + " " + right_2 + " " + left_1 + " " + left_2)


def wall_or_cliff_seen():
    send_commands(ropcodes.QUERY_LIST + " 5 " + ropcodes.WALL + " "
    + ropcodes.CLIFF_LEFT + " " + ropcodes.CLIFF_FRONT_LEFT + " "
    + ropcodes.CLIFF_FRONT_RIGHT + " " + ropcodes.CLIFF_RIGHT)
    wall_status = connect.read(1)
    if wall_status is 0:
        return False
    else:
        return True

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

