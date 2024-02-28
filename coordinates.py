#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire
#from ev3dev2.sensor import Sensor, lego
import ev3dev2.sensor.lego
from better_turn_to_angle import turn

gyro = ev3dev2.sensor.lego.GyroSensor('in3')

STUD_MM = 8
# test with a robot that:
# - uses the standard wheels known as EV3Tire
# - wheels are 22 studs apart
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_A, EV3EducationSetTire, 30 * STUD_MM)

# Enable odometry
mdiff.odometry_start()

# Use odometry to drive to specific coordinates
#mdiff.on_to_coordinates(SpeedRPM(40), 0, 300)

# Use odometry to go back to where we started
#mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)

gyro.reset()
mdiff.gyro = gyro
#mdiff.gyro.reset()
#gyro.reset()

print('1 -', gyro.angle)


# Use odometry to rotate in place to 90 degrees
#mdiff.turn_to_angle(SpeedRPM(40), -90, use_gyro=True)
turn(40, OUTPUT_B, OUTPUT_A, 90, gyro)
turn(40, OUTPUT_B, OUTPUT_A, 359, gyro)

print('2 -', gyro.angle)

# Disable odometry
mdiff.odometry_stop()