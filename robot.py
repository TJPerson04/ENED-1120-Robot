### TODO ###
# Optimize how the robot decides to turn (clockwise or counter-clockwise) when given an angle
# Optimize how the robot decides to move (forward or backward) when given an endpoint
# Make the turning correction cleaner
# Make sure self.dir is always between 0-359

### NOTES ###
# Most of the time, the robot can move in the x-direction first, then the y-direction. Only when it is between shelves can it not do this
# Any more complicated movements should be a series of multiple movements
#    Maybe refactor this to make it better?
#    def make better, need to for model
#    Still prob just use a combination of how it moves now tho

# Libraries
from ev3dev2.motor import Motor, MoveTank, SpeedRPM
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.display import Display
from time import sleep
from math import sin, cos, pi

class Robot:
    def __init__(self, leftMotorAddr: str, rightMotorAddr: str, cm_per_rotation: float = 17.5):
        '''Creates an object representing the robot'''
        self.leftMotorAddr = leftMotorAddr
        self.rightMotorAddr = rightMotorAddr
        self.cm_per_rotation = cm_per_rotation
        self.in_per_rotation = self.cm_per_rotation * 0.393701

        self.x = 6  # The coordinates of the robot (in in)
        self.y = -6
        self.dir = 90  # The direction the robot is facing (in degrees)
        # 0 degrees is straight to the right in the positive y-direction
        # This should always be between 0-359 (I don't think there is anything checking this rn)

        # These are like their normal counterparts, but are specifically for keeping track of the robot's direction and location when calculating uncertainty
        # The program needs to plan where it will be before it actually moves there
        self.x_plan = self.x
        self.y_plan = self.y
        self.dir_plan = self.dir

        self.leftMotor = Motor(leftMotorAddr)
        self.rightMotor = Motor(rightMotorAddr)
        self.motors = MoveTank(leftMotorAddr, rightMotorAddr)
        self.gyroSensor = GyroSensor()
        self.disp = Display()

        # Uncertainty
        self.uncPerInX = 0
        self.uncPerInY = 0
        self.uncPerInX_turn = 0
        self.uncPerInY_turn = 0
        self.uncX = 0
        self.uncY = 0

        # Aisles
        self.vert_aisles = [6, 54, 102]  # These are the x-values for the veritcal aisles
        self.horiz_aisles = [6, 30, 54, 78, 102]  # These are the y-values for the horizontal aisles
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
    
    def getNearestVertAisle(self, x):
        min = self.vert_aisles[0]
        for val in self.vert_aisles:
            if (abs(val - x) < min):
                min = val
        
        return min
    
    def getNearestHorizAisle(self, y):
        min = self.horiz_aisles[0]
        for val in self.horiz_aisles:
            if (abs(val - y) < min):
                min = val

        return min
    
    def moveToX(self, end = 0, speed = SpeedRPM(40), unit = 'in'):
        '''
        Moves the robot to a given x-coordinate\n
        If the end == robot.x, this will do nothing
        '''
        # Converts the coordinates to inches if they are given in centimeters
        if (unit == 'cm'):
            end[0] /= 2.54
            end[1] /= 2.54

        if (end > self.x):
            self.turnTo(0)
            self.moveForward(end - self.x, speed, unit)
        elif (end < self.x):
            self.turnTo(180)
            self.moveForward(self.x - end, speed, unit)
        self.x = end
        
        return self.x
    
    def moveToY(self, end = 0, speed = SpeedRPM(40), unit = 'in'):
        '''
        Moves the robot to a given y-coordinate\n
        If the end == robot.y, this will do nothing
        '''
        # Converts the coordinates to inches if they are given in centimeters
        if (unit == 'cm'):
            end[0] /= 2.54
            end[1] /= 2.54

        if (end > self.y):
            self.turnTo(90)
            self.moveForward(end - self.y, speed, unit)
        elif (end < self.y):
            self.turnTo(270)
            self.moveForward(self.y - end, speed, unit)
        self.y = end

        return self.y

    ### UNTESTED ###
    def moveTo(self, end = [0, 0], speed = SpeedRPM(40), unit = 'in'):
        '''
        -----UNTESTED-----\n
        Moves the robot to a location on a coordinate grid\n
        The default unit is inches, but it can also be set to centimeters (unit = 'cm')\n
        It will move in the x-direction first, then the y-direction, the stop
        '''
        
        if (end == [self.x, self.y]): 
            return [self.x, self.y]
        
        # Pathing algorithm
        self.moveToY(self.getNearestHorizAisle(self.y), speed, unit)
        if (self.getNearestHorizAisle(end[1]) != self.getNearestHorizAisle(self.y)):
            # Checks if there is an aisle between the robot and the end point
            # Only checking middle aisle b/c that's the only aisle that could be between two points
            isAisleBetween = (self.x <= self.vert_aisles[1] and end[0] >= self.vert_aisles[1]) or (self.x >= self.vert_aisles[1] and end[0] <= self.vert_aisles[1])
            if (isAisleBetween):
                self.moveToX(self.vert_aisles[1], speed, unit)
            else:
                self.moveTo(self.getNearestVertAisle(self.x), speed, unit)
            self.moveToY(self.getNearestHorizAisle(end[1]), speed, unit)
            offset = self.getUncertainty(end)
        self.moveToX(end[0] + offset[0], speed, unit)
        self.moveToX(end[1] + offset[1], speed, unit)

        
        return [self.x, self.y]

    
    # Prob a better way to do this
    def getDirNeedTurn(self, end = 0, axis = 'x', start = None, dir = None):
        '''
        Given an end point and the axis ('x' or 'y'), will return the direction the robot needs to turn to get there (None, 'l', or 'r')
        '''
        if (start == None):
            if (axis == 'x'):
                start = self.x_plan
            else:
                start = self.y_plan
        if (dir == None):
            dir = self.dir_plan

        if (axis == 'x'):
            if (end == start):
                return None
            
            if (end > start):
                if (dir == 0):
                    return None
                elif (0 - dir < 0):  # I know that this is redundant, I'm keeping it for now b/c it mirrors the structure of the next part
                    return 'l'
                else:
                    return 'r'
            else:
                if (dir == 180):
                    return None
                elif (180 - dir < 0):
                    return 'l'
                else:
                    return 'r'
        else:
            if (end == start):
                return None
            
            if (end > start):
                if (dir == 90):
                    return None
                elif (90 - dir < 0):
                    return 'l'
                else:
                    return 'r'
            else:
                if (dir == 270):
                    return None
                elif (270 - dir < 0):
                    return 'l'
                else:
                    return 'r'
    
    def getUncFromDist(self, dist, dir, dirTurning = 'r', unit = 'in'):
        '''
        dir is the direction the robot will be facing\n
        dirTurning is 'l', 'r', or None
        '''
        if (dist == 0):
            return [0, 0]
        
        # Converts the distance to inches if it is given in centimeters
        if (unit == 'cm'):
            dist /= 2.54
        
        xUncRel = 0
        yUncRel = 0
        # These equations were determined in our test plan excel
        # These are also relative to the robot (+x is forward and +y is to the right)
        if (dirTurning == 'r'):
            xUncRel = -0.0205 * dist - 0.019
            yUncRel = 0.0023 * dist - 0.1168
        elif (dirTurning == 'l'):
            xUncRel = -0.0199 * dist + 0.419
            yUncRel = -0.0156 * dist + 1.6875
        else:  # This is if the robot does not need to turn
            xUncRel = -0.0137 * dist - 0.0584
            yUncRel = 0.0238 * dist - 0.1775
        
        # Convert from x,y relative to the robot to x,y in the coord grid
        dirRad = dir * (pi / 180)
        xUnc = xUncRel * cos(dirRad) + yUncRel * cos(dirRad - pi / 2)
        yUnc = xUncRel * sin(dirRad) + yUncRel * sin(dirRad - pi / 2)

        return [xUnc, yUnc]
    
    def moveToXPlan(self, end = 0, unit = 'in'):
        '''
        Moves the robot to a given x-coordinate\n
        If the end == robot.x, this will do nothing
        '''
        # Converts the coordinates to inches if they are given in centimeters
        if (unit == 'cm'):
            end[0] /= 2.54
            end[1] /= 2.54

        if (end > self.x_plan):
            self.dir_plan = 0
        elif (end < self.x_plan):
            self.dir_plan = 180
        self.x_plan = end
        
        return self.x_plan
    
    def moveToYPlan(self, end = 0, unit = 'in'):
        '''
        Plans to move the robot to a given y-coordinate\n
        Doesn't actually move the robot, just updates self.y_plan and self.dir_plan\n
        If the end == robot.y, this will do nothing
        '''
        # Converts the coordinates to inches if they are given in centimeters
        if (unit == 'cm'):
            end[0] /= 2.54
            end[1] /= 2.54

        if (end > self.y_plan):
            self.dir_plan = 90
        elif (end < self.y_plan):
            self.dir_plan = 270
        self.y_plan = end

        return self.y_plan
    
    def updateUnc(self, end, axis = 'x'):
        dist = 0
        if (axis == 'x'):
            dist = abs(self.x_plan - end)
            self.moveToXPlan(end)
        else:
            dist = abs(self.y_plan - end)
            self.moveToYPlan(end)
        unc = self.getUncFromDist(dist, self.dir_plan, self.getDirNeedTurn(end, axis))
        self.uncX += unc[0]
        self.uncY += unc[1]

        return unc
    
    def getUncertainty(self, end = [0, 0]):  # Kind of a mirror of moveTo, but using the pathing algorithm to calculate uncertainty, instead of actually moving
        '''
        Returns the range of error for the robot to move from where it is to end\n
        end is a coordinate in the form [x, y]
        '''

        if (end == [self.x, self.y]):
            return [0, 0]

        # Pathing Algorithm
        # Only simulates moving the robot so it can calculate uncertainty
        self.updateUnc(self.getNearestHorizAisle(self.y_plan), 'y')
        if (self.getNearestHorizAisle(end[1]) != self.getNearestHorizAisle(self.y_plan)):
            # Checks if there is an aisle between the robot and the end point
            # Only checking middle aisle b/c that's the only aisle that could be between two points
            isAisleBetween = (self.x_plan <= self.vert_aisles[1] and end[0] >= self.vert_aisles[1]) or (self.x_plan >= self.vert_aisles[1] and end[0] <= self.vert_aisles[1])
            if (isAisleBetween):
                self.updateUnc(self.vert_aisles[1], 'x')
            else:
                self.updateUnc(self.getNearestVertAisle(self.x_plan), 'x')
            self.updateUnc(self.getNearestHorizAisle(end[1]), 'y')
        self.updateUnc(end[0], 'x')
        self.updateUnc(end[1], 'y')

        return [self.uncX, self.uncY]
    

    def displayText(self, text: str, x: int = 0, y: int = 0):
        '''Displays the given text at the given x, y location - UNDER CONSTRUCTION'''
        self.disp.text_grid(text, x=x, y=y)
        self.disp.update()