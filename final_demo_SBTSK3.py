#!/usr/bin/env python3
### FINAL DEMO SUBTASK 3 ###

#Libraries
from robot import Robot
from box import Box
from track import Track
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_2, INPUT_4
from ev3dev2.display import Display
from ev3dev2.sound import Sound
from ev3dev2 import fonts
from time import sleep

# Initialize robot and track
robot = Robot(OUTPUT_D, OUTPUT_B, OUTPUT_C, INPUT_2, INPUT_4)
disp = Display()
spkr = Sound()
track = Track()

givenBoxType = input("Please Enter the Box Type: ")

# Run any commands to the robot here
# robot.moveForward(15)  # TEST THIS
boxType = robot.getBoxType()
robot.dir = 0
robot.dir_plan = 0

for i in range(4):
    if (boxType == -1):
        robot.turnTo(0)
        robot.moveForward(1)
        boxType = robot.getBoxType()
    else:
        break

disp.text_grid("This box is type", boxType)

print("Box:", boxType)

if (str(boxType) == givenBoxType):
    disp.text_grid("Box Type: " + str(boxType) + "\nMATCH", text_color='green', font=fonts.load("luBS24"))
    disp.update()
    # robot.spkr.play_file('./code/icarly_cheers_ev3.wav', play_type=robot.spkr.PLAY_NO_WAIT_FOR_COMPLETE)
    robot.flashLight("Green")
else:
    disp.text_grid("Box Type: " + str(boxType) + "\nDOES NOT MATCH\nGiven:  " + str(givenBoxType), text_color='red', font=fonts.load("luBS24"))
    disp.update()
    # robot.spkr.play_file('./code/buzzer_ev3.wav', play_type=robot.spkr.PLAY_NO_WAIT_FOR_COMPLETE)
    robot.flashLight("red")

### SUBTASK 4 ###
isCont = input("Are you continuing to subtask 4 (y/n)? ")
if (isCont == "y"):
    robot.turnTo(90)
    robot.moveForward(3, stopWhenObj=False)
    robot.pickUp()
    robot.moveBackward(3)
    robot.turnTo(0)
    robot.moveForward(21)