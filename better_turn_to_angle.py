#!/usr/bin/env python3

# Libraries
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, Motor
from ev3dev2.sensor.lego import GyroSensor


def turn(speed, leftMotorAddr, rightMotorAddr, angleDeg, gyroSensor):
    gyroSensor.reset()

    leftMotor = Motor(leftMotorAddr)
    rightMotor = Motor(rightMotorAddr)

    while (gyroSensor.angle <= angleDeg % 360):
        # speed = abs(gyroSensor.angle - (angleDeg % 360) / 3.6)
        # if (abs(speed) > 40):
        #     speed = 40
        leftMotor.on(speed)
        rightMotor.on(-1 * speed)
    
    leftMotor.stop()
    rightMotor.stop()

    return True