### TODO ###
# Optimize how the robot decides to turn (clockwise or counter-clockwise) when given an angle
# Optimize how the robot decides to move (forward or backward) when given an endpoint
# Make the turning correction cleaner

# Libraries
from ev3dev2.motor import Motor, MoveTank, SpeedRPM
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.display import Display
from time import sleep

class Robot:
    def __init__(self, leftMotorAddr: str, rightMotorAddr: str, cm_per_rotation: float = 17.5):
        '''Creates an object representing the robot'''
        self.leftMotorAddr = leftMotorAddr
        self.rightMotorAddr = rightMotorAddr
        self.cm_per_rotation = cm_per_rotation

        self.x = 0  # The coordinates of the robot (in cm)
        self.y = 0
        self.dir = 0  # The direction the robot is facing (in degrees)

        self.leftMotor = Motor(leftMotorAddr)
        self.rightMotor = Motor(rightMotorAddr)
        self.motors = MoveTank(leftMotorAddr, rightMotorAddr)
        self.gyroSensor = GyroSensor()
        self.disp = Display()
        return
        
        

    def turn(self, angle: int, speed = SpeedRPM(40)):
        '''Turn the robot the specified number of degrees clockwise'''
        # Zeros the gyro sensor
        self.gyroSensor.reset()

        if (angle == 0):
            return True
        elif (angle > 0):
            # Turns clockwise until the angle is met
            while (self.gyroSensor.angle <= angle):  # Might need angle % 360, not sure?
                # speed = abs(gyroSensor.angle - (angleDeg % 360) / 3.6)
                # if (abs(speed) > 40):
                #     speed = 40
                self.leftMotor.on(speed)
                self.rightMotor.on(-1 * speed)
        
            # The robot will correct itself if it turns too far
            while (self.gyroSensor.angle > angle):
                self.leftMotor.on(-5)
                self.rightMotor.on(5)
            sleep(0.5)
            while (self.gyroSensor.angle <= angle + 1):  # Idk why but the +1 helps
                self.leftMotor.on(3)
                self.rightMotor.on(-3)
        else:
            # Turns counter-clockwise if the angle is negative
            while (self.gyroSensor.angle >= angle):
                self.leftMotor.on(-1 * speed)
                self.rightMotor.on(speed)

            # The robot will correct itself if it turns too far
            while (self.gyroSensor.angle < angle):
                self.leftMotor.on(5)
                self.rightMotor.on(-5)
            sleep(0.5)
            while (self.gyroSensor.angle >= angle - 1):  # Idk why but the -1 helps
                self.leftMotor.on(-3)
                self.rightMotor.on(3)
    
        # Stops the motors
        self.leftMotor.stop()
        self.rightMotor.stop()

        return True
    
    ### UNTESTED ###
    def turnTo(self, angle, speed = SpeedRPM(40)):
        '''Turns the robot clockwise to a specified angle - UNTESTED'''
        # Stops the function if the robot is already facing the right way
        if (self.dir == angle):
            return self.dir
        
        self.turn(angle - self.dir, speed)
        self.dir = angle  # Might be better to set self.dir to gyroSensor.angle and not reset the gyro sensor in self.turn, idk
        return self.dir
    

    
    def moveForward(self, cm: float, speed = SpeedRPM(40), unit = 'cm'):
        '''
        Moves the robot forward the specified distance\n
        The default unit is centimeters, but it can also be set to inches (unit = 'in')
        '''

        dist = cm / self.cm_per_rotation
        if (unit == 'in'):
            dist = (cm * 2.54) / self.cm_per_rotation
        
        self.motors.on_for_rotations(speed, speed, dist, True)
        return True
    
    def moveBackward(self, cm: float, speed = SpeedRPM(40), unit = 'cm'):
        '''
        Moves the robot backwards the specified distance\n
        The default unit is centimeters, but it can also be set to inches (unit = 'in')
        '''
        
        self.moveForward(cm, speed, unit)
        return True
    
    ### UNTESTED ###
    def moveTo(self, end = [0, 0], speed = SpeedRPM(40), unit = 'cm'):
        '''
        -----UNTESTED-----\n
        Moves the robot to a location on a coordinate grid\n
        The default unit is centimeters, but it can also be set to inches (unit = 'in')
        '''
        # Converts the coordinates to centimeters if they are given in inches
        if (unit == 'in'):
            end[0] /= 2.54
            end[1] /= 2.54
        
        # Move in x-direction
        if (end[0] > self.x):
            self.turnTo(90)
            self.moveForward(end[0] - self.x, speed, unit)
        elif (end[0] < self.x):
            self.turnTo(270)
            self.moveForward(self.x - end[0], speed, unit)
        self.x = end[0]
        
        # Move in y-direction
        if (end[1] > self.y):
            self.turnTo(0)
            self.moveForward(end[1] - self.y, speed, unit)
        elif (end[0] < self.x):
            self.turnTo(180)
            self.moveForward(self.y - end[1], speed, unit)
        self.y = end[1]
        
        return [self.x, self.y]
    

    def displayText(self, text: str, x: int = 0, y: int = 0):
        '''Displays the given text at the given x, y location - UNDER CONSTRUCTION'''
        self.disp.text_grid(text, x=x, y=y)
        self.disp.update()