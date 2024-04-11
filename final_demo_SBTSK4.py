#!/usr/bin/env python3
### FINAL DEMO SUBTASK 4 ###

#Libraries
from robot import Robot
from box import Box
from track import Track
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_2, INPUT_4
from time import sleep

# Initialize robot and track
robot = Robot(OUTPUT_D, OUTPUT_B, OUTPUT_C, INPUT_2, INPUT_4)
track = Track()

temp = input("Press Enter to Continue")

# Run any commands to the robot here
robot.turnTo(90)
robot.moveForward(3, stopWhenObj=False)
robot.pickUp()
robot.moveBackward(3)
robot.turnTo(0)
robot.moveForward(21)