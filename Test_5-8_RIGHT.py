#!/usr/bin/env python3

# Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from time import sleep

robot = Robot(OUTPUT_D, OUTPUT_A)

# Inputs
y = int(input('Input the distance to travel after turning RIGHT (in): '))


while True:
    temp = input('Press enter to continue')
    robot.moveForward(12, unit='in')
    robot.turn(90)
    robot.moveForward(y, unit='in')
