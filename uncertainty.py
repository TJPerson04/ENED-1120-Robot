### Libraries ###
from math import pi, sin, cos

### Variables ###
# In practice this is all defined in a robot class, 
# but for singular testing purposes it is in its own file.
# As a result, all the properties of the class have been changed
# to values in an object (r)
r = {}

# Location and direction facing
r['x'] = 30  # The current x-coordinate of the robot
r['y'] = 54  # The current y-coordinate of the robot
r['dir'] = 90  # 90 is the y-axis, 0 is the x-axis

# Also location and direction, but specifically for simulating movement, not actually where the robot is
# These are exclusively used to calculate uncertainty
r['x_plan'] = r['x']
r['y_plan'] = r['y']
r['dir_plan'] = r['dir']

# Uncertainty trackers
r['uncX'] = 0
r['uncY'] = 0

# Aisles
r['vert_aisles'] = [6, 54, 102]  # These are the x-values for the veritcal aisles
r['horiz_aisles'] = [6, 30, 54, 78, 102]  # These are the y-values for the horizontal aisles


### Functions ###
def getNearestVertAisle(x: int):
    '''Returns the x-position of the vertical aisle closest to a given x-value'''
    global r  # This is so the function can use the global object r, usually they would just use self. but that doesn't work in this independent file
    aisle = r['vert_aisles'][0]
    min = abs(r['vert_aisles'][0] - x)
    for val in r['vert_aisles']:
        if (abs(val - x) < min):
            aisle = val
            min = abs(aisle - x)
    
    return aisle
    
def getNearestHorizAisle(y: int):
    '''Returns the y-position of the horizontal aisle closest to a given y-value'''
    global r
    aisle = r['horiz_aisles'][0]
    min = abs(r['horiz_aisles'][0] - y)
    for val in r['horiz_aisles']:
        if (abs(val - y) < min):
            aisle = val
            min = abs(aisle - y)

    return aisle


def getDirNeedTurn(end: int, axis = 'x', start = None, dir = None):
    '''
    Given an end point and the axis ('x' or 'y'), will return the direction the robot needs to turn to get there (None, 'l', or 'r')\n
    start is the starting coordinate of the robot on the given axis\n
    dir is the direction the robot is facing\n
    By default this function will assume that it is following the simulated movement (x_plan, y_plan, dir_plan)
    '''
    global r
    if (start == None):
        if (axis == 'x'):
            start = r['x_plan']
        else:
            start = r['y_plan']
    if (dir == None):
        dir = r['dir_plan']

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

def moveToXPlan(end = 0, unit = 'in'):
    '''
    Plans to move the robot to a given x-coordinate\n
    Doesn't actually move the robot, just updates r_x_plan and r_dir_plan\n
    If the end == robot.x, this will do nothing
    '''
    global r
    # Converts the coordinates to inches if they are given in centimeters
    if (unit == 'cm'):
        end[0] /= 2.54
        end[1] /= 2.54

    # Determines what direction the robot needs to face to reach end
    if (end > r['x_plan']):
        r['dir_plan'] = 0
    elif (end < r['x_plan']):
        r['dir_plan'] = 180
    
    # Updates simulated location
    r['x_plan'] = end
    
    return r['x_plan']

def moveToYPlan(end = 0, unit = 'in'):
    '''
    Plans to move the robot to a given y-coordinate\n
    Doesn't actually move the robot, just updates r_y_plan and r_dir_plan\n
    If the end == robot.y, this will do nothing
    '''
    global r
    # Converts the coordinates to inches if they are given in centimeters
    if (unit == 'cm'):
        end[0] /= 2.54
        end[1] /= 2.54

    # Determines what direction the robot needs to face to reach end
    if (end > r['y_plan']):
        r['dir_plan'] = 90
    elif (end < r['y_plan']):
        r['dir_plan'] = 270
    
    # Updates simulated location
    r['y_plan'] = end

    return r['y_plan']

def getUncFromDist(dist, dir, dirTurning = 'r', unit = 'in'):
    '''
    Calculates the expected error of the robot's position given the distance it travels\n
    Also updates the global uncertainty trackers\n
    dir is the direction the robot will be facing\n
    dirTurning is 'l', 'r', or None
    '''
    global r
    if (dist == 0):
        return [0, 0]
    
    # Converts the distance to inches if it is given in centimeters
    if (unit == 'cm'):
        dist /= 2.54
    
    xUncRel = 0
    yUncRel = 0
    # These equations were determined in our test plan excel from testing results
    # These are also relative to the robot (+x is forward and +y is to the right)
    if (dirTurning == 'r'):
        xUncRel = -0.0205 * dist - 0.019
        yUncRel = 0.0023 * dist - 0.1168
    elif (dirTurning == 'l'):
        xUncRel = -0.0199 * dist + 0.419
        yUncRel = -0.0156 * dist + 1.6875
    else:  # This is if the robot does not need to turn (dirTurning == None)
        xUncRel = -0.0137 * dist - 0.0584
        yUncRel = 0.0238 * dist - 0.1775
    
    # Convert from x,y relative to the robot to x,y in the coord grid
    dirRad = dir * (pi / 180)
    xUnc = xUncRel * cos(dirRad) + yUncRel * cos(dirRad - pi / 2)
    yUnc = xUncRel * sin(dirRad) + yUncRel * sin(dirRad - pi / 2)

    return [xUnc, yUnc]

def updateUnc(end, axis = 'x'):
    '''
    Updates the necessary values to simulate the robot moving\n
    Also updates the uncertainty predictions
    '''
    global r
    dist = 0
    dir = getDirNeedTurn(end, axis)
    if (axis == 'x'):
        dist = abs(r['x_plan'] - end)
        moveToXPlan(end)
    else:
        dist = abs(r['y_plan'] - end)
        moveToYPlan(end)
    if (dist == 0):
        return 0
    unc = getUncFromDist(dist, r['dir_plan'], dir)
    
    r['uncX'] += unc[0]
    r['uncY'] += unc[1]
    
    return unc

def getUncertainty(end = [0, 0]):  # Kind of a mirror of movement function, but using the pathing algorithm to calculate uncertainty, instead of actually moving
    '''
    Returns the range of error for the robot to move from where it is to end\n
    end is a coordinate in the form [x, y]
    '''
    global r

    if (end == [r['x'], r['y']]):
        return [0, 0]

    ### Pathing Algorithm ###
    # Only simulates moving the robot to calculate uncertainty
    # Checks if the robot can just go straight to the end or not
    if (getNearestHorizAisle(end[1]) != getNearestHorizAisle(r['y_plan']) and getNearestVertAisle(end[0]) != getNearestVertAisle(r['x_plan'])):
        updateUnc(getNearestHorizAisle(r['y_plan']), 'y')
        # Checks if there is an aisle between the robot and the end point
        # Only checking middle aisle b/c that's the only aisle that could be between two points
        isAisleBetween = (r['x_plan'] <= r['vert_aisles'][1] and end[0] >= r['vert_aisles'][1]) or (r['x_plan'] >= r['vert_aisles'][1] and end[0] <= r['vert_aisles'][1])
        if (isAisleBetween):
            updateUnc(r['vert_aisles'][1], 'x')
        else:
            updateUnc(getNearestVertAisle(r['x_plan']), 'x')
        updateUnc(getNearestHorizAisle(end[1]), 'y')
    elif (getNearestHorizAisle(end[1]) == getNearestHorizAisle(r['y_plan'])):
        updateUnc(getNearestHorizAisle(r['y_plan']), 'y')
    elif (getNearestVertAisle(end[0]) == getNearestVertAisle(r['x_plan'])):
        updateUnc(getNearestVertAisle(r['x_plan']), 'x')
        updateUnc(end[1], 'y')  # This is to make sure that the robot always alternates which direction it is moving (x, then y, then x, etc)
    updateUnc(end[0], 'x')
    updateUnc(end[1], 'y')

    return [r['uncX'], r['uncY']]


# Main
end = []
end.append(float(input('Enter the end x-coordinate: ')))
end.append(float(input('Enter the end y-coordinate: ')))

getUncertainty(end)

print('The robot will be off by', r['uncX'], 'in the x direction, and', r['uncY'], 'in the y direction')