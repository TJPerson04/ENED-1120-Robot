#!/usr/bin/env python3

# Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from time import sleep

robot = Robot(OUTPUT_D, OUTPUT_A)

# Inputs
n = int(input('Input the number of laps: '))
y = int(input('Input the length of each lap (cm): '))
delay = int(input('Input the delay: '))

sleep(delay)

for i in range(n):
    robot.moveForward(y)
    robot.moveBackward(y)