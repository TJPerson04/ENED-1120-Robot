#!/usr/bin/env python3

#Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4

# Initialize robot
robot = Robot(OUTPUT_D, OUTPUT_B, OUTPUT_C, INPUT_1, INPUT_4)

# Run any commands to the robot here
POSSIBLE_BARCODES = [
    [[3, 'W'], [1, 'B']], 
    [[1, 'W'], [1, 'B'], [1, 'W'], [1, 'B']], 
    [[2, 'W'], [2, 'B']],
    [[1, 'B'], [2, 'W'], [1, 'B']]
]
test = robot.readBarcode()

for code in POSSIBLE_BARCODES:
    print(robot.compareBarcodes(test, code))