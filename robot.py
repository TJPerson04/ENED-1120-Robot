### TODO ###
# Let the robot turn counter-clockwise
# Optimize how the robot decides to turn (clockwise or counter-clockwise) when given an angle
# Optimize how the robot decides to move (forward or backward) when given an endpoint

# Libraries
from ev3dev2.motor import Motor, MoveTank, SpeedRPM
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.display import Display

class Robot:
    def __init__(self, leftMotorAddr: str, rightMotorAddr: str, gyroSensorAddr: str|None = None, cm_per_rotation: float = 17.5):
        '''Creates an object representing the robot'''
        self.leftMotorAddr = leftMotorAddr
        self.rightMotorAddr = rightMotorAddr
        self.gyroSensorAddr = gyroSensorAddr
        self.cm_per_rotation = cm_per_rotation

        self.x = 0  # The coordinates of the robot (in cm)
        self.y = 0
        self.dir = 0  # The direction the robot is facing (in degrees)

        self.leftMotor = Motor(leftMotorAddr)
        self.rightMotor = Motor(rightMotorAddr)
        self.motors = MoveTank(leftMotorAddr, rightMotorAddr)
        self.gyroSensor = GyroSensor(gyroSensorAddr)
        self.disp = Display()
        return
        
        

    def turn(self, angle: int, speed = SpeedRPM(40)):
        '''Turn the robot the specified number of degrees clockwise'''
        # Zeros the gyro sensor
        self.gyroSensor.reset()

        # Turns clockwise until the angle is met
        while (self.gyroSensor.angle <= angle % 360):
            # speed = abs(gyroSensor.angle - (angleDeg % 360) / 3.6)
            # if (abs(speed) > 40):
            #     speed = 40
            self.leftMotor.on(speed)
            self.rightMotor.on(-1 * speed)
        
        ### UNTESTED ###
        # The robot will correct itself if it turns too far
        # while (self.gyroSensor.angle > angle % 360):
        #     self.leftMotor.on(-1 * speed)
        #     self.rightMotor.on(speed)
    
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
    

    
    def moveForward(self, cm: float, speed = SpeedRPM(40)):
        '''Moves the robot forward the specified distance in centimeters'''
        self.motors.on_for_rotations(speed, speed, cm / self.cm_per_rotation, True)
        return True
    
    def moveBackward(self, cm: float, speed = SpeedRPM(40)):
        '''Moves the robot backwards the specified distance in centimeters'''
        self.moveForward(self, cm, -1 * speed)
        return True
    
    ### UNTESTED ###
    def moveTo(self, end: list[int] = [0, 0], speed = SpeedRPM(40)):
        '''Moves the robot to a location on a coordinate grid - UNTESTED'''
        # Move in x-direction
        if (end[0] > self.x):
            self.turnTo(90)
            self.moveForward(end[0] - self.x, speed)
        elif (end[0] < self.x):
            self.turnTo(270)
            self.moveForward(self.x - end[0], speed)
        self.x = end[0]
        
        # Move in y-direction
        if (end[1] > self.y):
            self.turnTo(0)
            self.moveForward(end[1] - self.y, speed)
        elif (end[0] < self.x):
            self.turnTo(180)
            self.moveForward(self.y - end[1], speed)
        self.y = end[1]
        
        return [self.x, self.y]
    

    def displayText(self, text: str, x: int = 0, y: int = 0):
        '''Displays the given text at the given x, y location - UNDER CONSTRUCTION'''
        self.disp.text_grid(text, x=x, y=y)
        self.disp.update()