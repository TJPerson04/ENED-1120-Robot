#!/usr/bin/env python3

from robot import Robot
from ev3dev2.motor import OUTPUT_A, OUTPUT_D

robot = Robot(OUTPUT_D, OUTPUT_A)

robot.turn(90)