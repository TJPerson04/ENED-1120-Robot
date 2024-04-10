#!/usr/bin/env python3

#Libraries
from robot import Robot
from track import Track
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4
from time import sleep
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from ev3dev2.sound import Sound

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
disp = Display()
# disp.text_grid("Box Type: " + str(1) + " - MATCH", font=, text_color='green')
# disp.draw.text((10, 10), "Box Type: " + str(1) + "\nMATCH", font=fonts.load('luBS24'))
disp.text_grid("Box Type: " + str(1) + "\nNOT A MATCH\nGiven:  " + str(2), text_color='red', font=fonts.load("luBS24"))

disp.update()

robot.pickUp()

spkr = Sound()
spkr.play_song((
    ('D4', 'e3'),      # intro anacrouse
    ('D4', 'e3'),
    ('D4', 'e3'),
    ('G4', 'h'),       # meas 1
    ('D5', 'h'),
    ('C5', 'e3'),      # meas 2
    ('B4', 'e3'),
    ('A4', 'e3'),
    ('G5', 'h'),
    ('D5', 'q'),
    ('C5', 'e3'),      # meas 3
    ('B4', 'e3'),
    ('A4', 'e3'),
    ('G5', 'h'),
    ('D5', 'q'),
    ('C5', 'e3'),      # meas 4
    ('B4', 'e3'),
    ('C5', 'e3'),
    ('A4', 'h.'),
), 200, 0.01)

robot.moveForward(12)
robot.putDown()
sleep(5)