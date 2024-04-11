#!/usr/bin/env python3
### FINAL DEMO SUBTASK 2 ###

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
robot.dir = 270
robot.dir_plan = 270
robot.x = track.homeB[0]
robot.x_plan = track.homeB[0]
robot.y = track.homeB[1]
robot.y_plan = track.homeB[1]

robot.moveTo(track.homeA)