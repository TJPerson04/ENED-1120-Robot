### FINAL DEMO SUBTASK 1 ###
#!/usr/bin/env python3

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

# Run any commands to the robot here
label = input("Please enter the label of the box: ")
box = Box(1, label)

robot.moveTo(box.location)
sleep(5)
robot.moveTo(track.homeB)

### SUBTASK 2 ###
isCont = input("Are you continuing to subtask 2 (y/n)? ")
if (isCont == "y"):
    robot.moveTo(track.homeA)