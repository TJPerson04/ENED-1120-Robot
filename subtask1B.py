#!/usr/bin/env python3

# Libraries
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedRPM, MoveTank
from ev3dev2.sensor.lego import GyroSensor
from better_turn_to_angle import turn
from time import sleep

# Sensors/Motors
gyro = GyroSensor()
motors = MoveTank(OUTPUT_D, OUTPUT_A)

# Conversion
CM_PER_ROTATION = 17.5  # Maybe change to 17.45 or something, it's ever so slightly off

# Inputs
n = int(input('Enter the number of laps: '))
y = int(input('Enter the length of each lap (cm): '))
delay = int(input('Enter the delay time: '))

sleep(delay)

# Move the robot
for i in range(2 * n):
    motors.on_for_rotations(SpeedRPM(40), SpeedRPM(40), y / CM_PER_ROTATION, True)
    turn(20, OUTPUT_D, OUTPUT_A, 180, gyro)