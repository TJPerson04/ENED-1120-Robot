#!/usr/bin/env python3

#Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D

# Initialize robot
robot = Robot(OUTPUT_D, OUTPUT_A, OUTPUT_B)

# Run any commands to the robot here
# robot.moveForward(20)
# robot.moveBackward(20)
# robot.turn(90)