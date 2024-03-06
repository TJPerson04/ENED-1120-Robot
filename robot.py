### TODO ###
# Optimize how the robot decides to turn (clockwise or counter-clockwise) when given an angle
# Optimize how the robot decides to move (forward or backward) when given an endpoint
# Make the turning correction cleaner
# Make sure self.dir is always between 0-359

### NOTES ###
# Most of the time, the robot can move in the x-direction first, then the y-direction. Only when it is between shelves can it not do this
# Any more complicated movements should be a series of multiple movements
#    Maybe refactor this to make it better?
#    Still prob just use a combination of how it moves now tho

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
        self.in_per_rotation = self.cm_per_rotation * 0.393701

        self.x = 0  # The coordinates of the robot (in cm)
        self.y = 0
        self.dir = 0  # The direction the robot is facing (in degrees)
        # 0 degrees is straight up in the positive y-direction
        # This should always be between 0-359 (I don't think there is anything checking this rn)

        self.leftMotor = Motor(leftMotorAddr)
        self.rightMotor = Motor(rightMotorAddr)
        self.motors = MoveTank(leftMotorAddr, rightMotorAddr)
        self.gyroSensor = GyroSensor()
        self.disp = Display()

        # Uncertainty
        self.uncPerCm = 0
        self.uncFromTurn = 0
        self.uncX = 0
        self.uncY = 0

        # Aisles
        self.y_aisles = []
        self.x_aisles = []
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
    

    
    def moveForward(self, dist: float, speed = SpeedRPM(40), unit = 'in'):
        '''
        Moves the robot forward the specified distance\n
        The default unit is centimeters, but it can also be set to inches (unit = 'in')
        '''

        if (unit == 'cm'):
            dist /= self.cm_per_rotation
        else:
            dist /= self.in_per_rotation
        
        self.motors.on_for_rotations(speed, speed, dist, True)
        return True
    
    def moveBackward(self, dist: float, speed = SpeedRPM(40), unit = 'in'):
        '''
        Moves the robot backwards the specified distance\n
        The default unit is centimeters, but it can also be set to inches (unit = 'in')
        '''
        
        self.moveForward(dist, speed, unit)
        return True
    
    ### UNTESTED ###
    def moveTo(self, end = [0, 0], speed = SpeedRPM(40), unit = 'in'):
        '''
        -----UNTESTED-----\n
        Moves the robot to a location on a coordinate grid\n
        The default unit is centimeters, but it can also be set to inches (unit = 'in')\n
        It will move in the x-direction first, then the y-direction, the stop
        '''
        # Converts the coordinates to inches if they are given in centimeters
        if (unit == 'cm'):
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

    
    def getcUncertainty(self, end = [0, 0]):
        '''
        Returns the range of error for the robot to move from where it is to end\n
        end is a coordinate in the form [x, y]
        '''
        uncXMult = 1

        # x-direction
        # Check if the robot has to turn
        if ((end[0] > self.x and self.dir != 90) or (end[0] < self.x and self.dir != 270)):
            uncXMult = self.uncFromTurn
        self.uncX += self.getUncStraightLine(abs(self.x - end[0])) * uncXMult

        # y-direction (will have to turn)
        self.uncY += self.getUncStraightLine(abs(self.y - end[1])) * self.uncFromTurn        


        ### DESIGN ###
        # X UNCERTAINTY
        # Check if the robot needs to turn to move in the x-direction
        #   If it does, add the turning uncertainty
        # Add the uncertainty for moving in a straight line for the given distance
        # 
        # Y UNCERTAINTY
        # Add the uncertainty for turning
        # Add the uncertainty for moving in a straight line for the given distance


    def getUncStraightLine(self, dist):
        return dist * self.uncPerCm
        