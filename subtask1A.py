#!/usr/bin/env python3

# Libraries
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedRPM, MoveTank
from time import sleep

# Inputs
n = int(input('Input the number of laps: '))
y = int(input('Input the length of each lap (cm): '))
delay = int(input('Input the delay: '))

sleep(delay)

# Conversion
CM_PER_ROTATION = 17.5  # Maybe change to 17.45 or something, it's ever so slightly off

# Move the motors
motors = MoveTank(OUTPUT_D, OUTPUT_A)

for i in range(n):
    motors.on_for_rotations(SpeedRPM(40), SpeedRPM(40), y / CM_PER_ROTATION, True)

    motors.on_for_rotations(SpeedRPM(-40), SpeedRPM(-40), y / CM_PER_ROTATION, True)
