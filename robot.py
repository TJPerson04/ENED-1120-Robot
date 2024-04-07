### TODO ###
# Optimize how the robot decides to turn (clockwise or counter-clockwise) when given an angle
# Optimize how the robot decides to move (forward or backward) when given an endpoint
# Make the turning correction cleaner
# Make sure self.dir is always between 0-359

### IDEAS ###
# Use ultrasonice sensor to determine how close the box is when picking up

# Libraries
from ev3dev2.motor import Motor, MoveTank, SpeedRPM
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor, ColorSensor
from ev3dev2.display import Display
from time import sleep
from math import sin, cos, pi
from box import Box

class Robot:
    def __init__(self, leftMotorAddr: str, rightMotorAddr: str, pickUpMotorAddr: str, colorSensor1Addr: str, colorSensor2Addr: str, cm_per_rotation: float = 17.5):
        '''Creates an object representing the robot'''
        self.leftMotorAddr = leftMotorAddr
        self.rightMotorAddr = rightMotorAddr
        self.pickUpMotorAddr = pickUpMotorAddr
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

        try: 
            self.leftMotor = Motor(leftMotorAddr)
            print("Left Motor Connected")
            self.rightMotor = Motor(rightMotorAddr)
            print("Right Motor Connected")
            self.pickUpMotor = Motor(pickUpMotorAddr)
            print("Pickup Motor Connected")
            self.motors = MoveTank(leftMotorAddr, rightMotorAddr)
            self.gyroSensor = GyroSensor()
            print("Gyro Sensor Connected")
        except:
            self.leftMotor = None
            self.rightMotor = None
            self.pickUpMotor = None
            self.motors = None
            self.gyroSensor = None
        self.disp = Display()
        try:
            self.ultraSonicSensor = UltrasonicSensor()
            print("Ultrasonic Sensor Connected")
        except:
            self.ultraSonicSensor = None
        try:
            self.colorSensor1 = ColorSensor(colorSensor1Addr)
            print("Color Sensor 1 Connected")
            self.colorSensor2 = ColorSensor(colorSensor2Addr)
            print("Color Sensor 2 Connected")
        except:
            self.colorSensor1 = None
            self.colorSensor2 = None

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
        
        

    def turn(self, angle: int, speed = SpeedRPM(20)):
        speed = SpeedRPM(10)
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
        
        self.turn(self.dir - angle, speed)
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

        # distGone = 0

        # while (distGone < dist):
        #     self.motors.on_for_rotations(speed, speed, 0.1, True)
        #     distGone += 0.1
        #     if (self.ultraSonicSensor.distance_inches <= 3):
        #         self.avoidObject()
        return True
    
    def moveBackward(self, dist: float, speed = SpeedRPM(40), unit = 'in'):
        '''
        Moves the robot backwards the specified distance\n
        The default unit is inches, but it can also be set to centimeters (unit = 'cm')
        '''
        
        self.moveForward(dist, -1 * speed, unit)
        return True
    
    def getNearestVertAisle(self, x: int):
        '''Returns the x-position of the vertical aisle closest to a given x-value'''
        aisle = self.vert_aisles[0]
        min = abs(self.vert_aisles[0] - x)
        for val in self.vert_aisles:
            if (abs(val - x) < min):
                aisle = val
                min = abs(aisle - x)
    
        return aisle
    
    def getNearestHorizAisle(self, y: int):
        '''Returns the y-position of the horizontal aisle closest to a given y-value'''
        aisle = self.horiz_aisles[0]
        min = abs(self.horiz_aisles[0] - y)
        for val in self.horiz_aisles:
            if (abs(val - y) < min):
                aisle = val
                min = abs(aisle - y)

        return aisle
    
    def moveToX(self, end: int, speed = SpeedRPM(40), unit = 'in'):
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
    
    def moveToY(self, end: int, speed = SpeedRPM(40), unit = 'in'):
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
        
        offset = self.getUncertainty(end)

        ### Pathing algorithm ###
        if (self.getNearestHorizAisle(end[1]) != self.getNearestHorizAisle(self.y) and self.getNearestVertAisle(end[0]) != self.getNearestVertAisle(self.x_plan)):
            print(1)
            self.moveToY(self.getNearestHorizAisle(self.y), speed, unit)
            # Checks if there is an aisle between the robot and the end point
            # Only checking middle aisle b/c that's the only aisle that could be between two points
            isAisleBetween = (self.x <= self.vert_aisles[1] and end[0] >= self.vert_aisles[1]) or (self.x >= self.vert_aisles[1] and end[0] <= self.vert_aisles[1])
            if (isAisleBetween):
                print(2)
                self.moveToX(self.vert_aisles[1], speed, unit)
            else:
                print(3)
                self.moveTo(self.getNearestVertAisle(self.x), speed, unit)
            print(4)
            self.moveToY(self.getNearestHorizAisle(end[1]), speed, unit)
        elif (self.getNearestHorizAisle(end[1]) == self.getNearestHorizAisle(self.y)):
            print(5)
            self.moveToY(self.getNearestHorizAisle(self.y), speed, unit)
        elif (self.getNearestVertAisle(end[0]) == self.getNearestVertAisle(self.x)):
            self.moveToX(self.getNearestVertAisle(self.x), speed, unit)
            self.moveToY(end[1] + offset[1], speed, unit)  # This is to make sure that the robot always alternates which direction it is moving (x, then y, then x, etc)
        print(self.getNearestVertAisle(end[0]))
        print(self.getNearestVertAisle(self.x))
        self.moveToY(end[1] + offset[1], speed, unit)
        self.moveToX(end[0] + offset[0], speed, unit)

        
        return [self.x, self.y]
    
    def avoidObject(self, speed = SpeedRPM(40), unit = 'in'):
        '''
        -----UNTESTED-----\n
        VERY rudimentary object avoidance\n
        Will just kinda vaugley go around the object, regardless of the object's size
        '''
        self.moveTo([self.x + 15, self.y], speed, unit)
        self.moveTo([self.x, self.y + 15], speed, unit)
        self.moveTo([self.x - 15, self.y], speed, unit)

        return [self.x, self.y]


    
    # Prob a better way to do this
    def getDirNeedTurn(self, end: int, axis = 'x', start = None, dir = None):
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
                elif (dir - 0 < 0):  # I know that this is redundant, I'm keeping it for now b/c it mirrors the structure of the next part
                    return 'l'
                else:
                    return 'r'
            else:
                if (dir == 180):
                    return None
                elif (dir - 180 < 0):
                    return 'l'
                else:
                    return 'r'
        else:
            if (end == start):
                return None
            
            if (end > start):
                if (dir == 90):
                    return None
                elif (dir - 90 < 0):
                    return 'l'
                else:
                    return 'r'
            else:
                if (dir == 270):
                    return None
                elif (dir - 270 < 0):
                    return 'l'
                else:
                    return 'r'
    
    def moveToXPlan(self, end: int, unit = 'in'):
        '''
        Simulates moving the robot to a given x-coordinate\n
        Doesn't actually move the robot, just updates self.y_plan and self.dir_plan\n
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
    
    def moveToYPlan(self, end: int, unit = 'in'):
        '''
        Simulates moving the robot to a given y-coordinate\n
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
    
    def getUncFromDist(self, dist: int, dir: int, dirTurning = 'r', unit = 'in'):
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
    
    def updateUnc(self, end: int, axis = 'x'):
        '''
        Updates the necessary values to simulate the robot moving\n
        Also updates the uncertainty predictions
        '''
        dist = 0
        dir = self.getDirNeedTurn(end, axis)
        if (axis == 'x'):
            dist = abs(self.x_plan - end)
            self.moveToXPlan(end)
        else:
            dist = abs(self.y_plan - end)
            self.moveToYPlan(end)
        if (dist == 0):
            return 0
        unc = self.getUncFromDist(dist, self.dir_plan, dir)
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
        
        # Resets values, just in case they don't already match up
        # (Like if someone calls just this function and not moveTo)
        self.y_plan = self.y
        self.x_plan = self.x
        self.dir_plan = self.dir

        ### Pathing Algorithm ###
        # Only simulates moving the robot so it can calculate uncertainty
        # Checks if the robot can just go straight to the end or not
        if (self.getNearestHorizAisle(end[1]) != self.getNearestHorizAisle(self.y_plan) and self.getNearestVertAisle(end[0]) != self.getNearestVertAisle(self.x_plan)):
            self.updateUnc(self.getNearestHorizAisle(self.y_plan), 'y')
            # Checks if there is an aisle between the robot and the end point
            # Only checking middle aisle b/c that's the only aisle that could be between two points
            isAisleBetween = (self.x_plan <= self.vert_aisles[1] and end[0] >= self.vert_aisles[1]) or (self.x_plan >= self.vert_aisles[1] and end[0] <= self.vert_aisles[1])
            if (isAisleBetween):
                self.updateUnc(self.vert_aisles[1], 'x')
            else:
                self.updateUnc(self.getNearestVertAisle(self.x_plan), 'x')
            self.updateUnc(self.getNearestHorizAisle(end[1]), 'y')
        elif (self.getNearestHorizAisle(end[1]) == self.getNearestHorizAisle(self.y_plan)):
            self.updateUnc(self.getNearestHorizAisle(self.y_plan), 'y')
        elif (self.getNearestVertAisle(end[0]) == self.getNearestVertAisle(self.x_plan)):
            self.updateUnc(self.getNearestVertAisle(self.x_plan), 'x')
            self.updateUnc(end[1], 'y')  # This is to make sure that the robot always alternates which direction it is moving (x, then y, then x, etc)

        self.updateUnc(end[0], 'x')
        self.updateUnc(end[1], 'y')

        return [self.uncX, self.uncY]
    

    def pickUp(self, speed = SpeedRPM(40)):
        self.pickUpMotor.on_for_rotations(100, 0.25)  # Prob change how long it's on for
        return True
    
    def putDown(self, speed = SpeedRPM(40)):
        self.pickUpMotor.on_for_rotations(-100, 5)  # Prob change how long it's on for
        return True
    

    def readBarcode(self):
        '''
        Constantly read the values from the color sensor and determine what barcode it is based on how many times the reading rapidly changes (moving vertically so will include the first 2 boxes of the horizontal hopefully)\n
        Might need to come up w/ dif idea for reading horizontal barcode\n
        RECONFIGURE USING ACTUAL TEST BOX\n
        I think there is an issue with my testing cardboard color being too close to white
        '''
        values = []
        colors = []
        output = ""
        sum = 0
        for i in range(5):
            sum += self.colorSensor2.reflected_light_intensity
        base = sum / 5  # Average
        self.moveBackward(4, SpeedRPM(20))
        for i in range(40):
            self.moveForward(0.1)
            values.append(self.colorSensor2.reflected_light_intensity)
            print(values[i])
            if values[i] < base / 2 and values[i] != 0:
                colors.append("B")
                output += "_"
            elif values[i] < base:  # This feels like it should be values[i] > base, might be b/c of paper I used for testing
                colors.append("W")
                output += "-"
            else:
                colors.append("Brown")
                output += "?"
        
        order = []
        for i in range(len(colors)):
            if (i == 0):
                continue

            if (colors[i] == colors[i - 1] and len(order) != 0 and colors[i]):
                order[len(order) - 1][0] += 1
            elif (colors[i] != "Brown"):
                order.append([1, colors[i]])
        # print(base)
        # print(values)
        # print(colors)
        print(output)
        # print(order)

        return order
    
    ### This code is gross, pls fix ###
    def compareBarcodes(self, reading: list, barcode: list):
        ROE = 2.5  # Range of error
        LOS = 5  # Length of a section
        isMatch = []
        test = False
        for i in range(len(reading)):
            section = reading[i]
            if (section[1] == barcode[0][1] and len(reading) - i >= len(barcode)):
                for j in range(len(barcode)):
                    isMatch.append(
                        reading[i + j][1] == barcode[j][1] and  # Colors are the same
                        reading[i + j][0] < (LOS + ROE) * barcode[j][0] and reading[i + j][0] > (LOS - ROE) * barcode[j][0]  # Numbers are within range
                        )
                test = True
                for val in isMatch:
                    if (not val):
                        test = False
                        break
                if (test):
                    break
        
        return test
    
    def getBoxType(self):
        POSSIBLE_BARCODES = [
            [[1, 'B'], [3, 'W']], 
            [[1, 'B'], [1, 'W'], [1, 'B'], [1, 'W']],
            [[2, 'B'], [2, 'W']],
            [[1, 'B'], [2, 'W'], [1, 'B']]
        ]
        test = self.readBarcode()

        i = 0
        results = []
        for code in POSSIBLE_BARCODES:
            results.append(self.compareBarcodes(test, code))
        
        if (not True in results):
            return -1
        
        boxType = 1
        for i in range(len(results)):
            if (results[i] and len(POSSIBLE_BARCODES[i]) > len(POSSIBLE_BARCODES[boxType - 1])):
                boxType = i + 1
        
        return boxType


    def displayText(self, text: str, x: int = 0, y: int = 0):
        '''Displays the given text at the given x, y location - UNDER CONSTRUCTION'''
        self.disp.text_grid(text, x=x, y=y)
        self.disp.update()