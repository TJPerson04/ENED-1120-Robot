#!/usr/bin/env python3

# Libraries
from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from time import sleep

robot = Robot(OUTPUT_D, OUTPUT_A)

# Inputs
y = int(input('Input the distance to travel (in): '))
delay = int(input('Input the delay: '))

sleep(delay)

robot.moveForward(y, unit='in')
