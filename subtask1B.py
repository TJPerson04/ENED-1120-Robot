#!/usr/bin/env python3

# Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from time import sleep

robot = Robot(OUTPUT_D, OUTPUT_A)

# Inputs
n = int(input('Enter the number of laps: '))
y = int(input('Enter the length of each lap (cm): '))
delay = int(input('Enter the delay time: '))

sleep(delay)

# Move the robot
for i in range(2 * n):
    robot.moveForward(y)
    robot.turn(180)