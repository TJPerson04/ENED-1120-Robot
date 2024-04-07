#!/usr/bin/env python3

#Libraries
from robot import Robot
from track import Track
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4
from time import sleep

# Initialize robot
robot = Robot(OUTPUT_D, OUTPUT_B, OUTPUT_C, INPUT_2, INPUT_4)

temp = input("Press Enter To Continue")

# Run any commands to the robot here

### Reading Barcode ###
# POSSIBLE_BARCODES = [
#     [[1, 'B'], [3, 'W']], 
#     [[1, 'B'], [1, 'W'], [1, 'B'], [1, 'W']], 
#     [[2, 'B'], [2, 'W']],
#     [[1, 'B'], [2, 'W'], [1, 'B']]
# ]
# test = robot.readBarcode()

# i = 0
# for code in POSSIBLE_BARCODES:
#     i += 1
#     print("Box Type", i, "-", robot.compareBarcodes(test, code))

# ## Moving Test ###
# track = Track()
# print(track.BOX_COORDS)

# endpoint = input('Enter the end point: ')
# try:
#     robot.moveTo(track.BOX_COORDS[endpoint])
#     robot.turnTo(90)
#     robot.putDown()
#     robot.moveForward(2)
#     robot.pickUp()
#     sleep(5)
# except:
#     print('Error: Invalid input')