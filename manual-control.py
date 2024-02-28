### Run this file while connected via bluetooth to manually control the robot from your computer ###

#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedRPM, MoveTank
from ev3dev2.sensor.lego import GyroSensor
from better_turn_to_angle import turn
from robot import Robot

robot = Robot(OUTPUT_D, OUTPUT_A)

print('1 - Move To')
print('2 - Move Forward')
print('3 - Move Backward')
print('4 - Turn To')
print('5 - Turn')
print('6 - Exit')
val = input('Enter a command: ')

while (val != '6'):
    if (val == '1'):
        x = int(input('Enter the x position to move to: '))
        y = int(input('Enter the y position to move to: '))
        robot.moveTo([x, y])
    elif (val == '2'):
        dist = int(input('Enter the distance (cm): '))
        robot.moveForward(dist)
    elif (val == '3'):
        dist = int(input('Enter the distance (cm): '))
        robot.moveBackward(dist)
    elif (val == '4'):
        angle = int(input('Enter the angle (degrees): '))
        robot.turnTo(angle)
    elif (val == '5'):
        angle = int(input('Enter the angle (degrees): '))
        robot.turn(angle)
    
    print('1 - Move To')
    print('2 - Move Forward')
    print('3 - Move Backward')
    print('4 - Turn')
    print('5 - Turn To')
    print('6 - Exit')
    val = input('Enter a command: ')