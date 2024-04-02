#!/usr/bin/env python3

#Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4

# Initialize robot
robot = Robot(OUTPUT_D, OUTPUT_B, OUTPUT_C, INPUT_1, INPUT_4)

# Run any commands to the robot here
robot.readBarcode()