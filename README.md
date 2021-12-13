# MultiplyLabsChallenge
Software Tech Challenge for Multiply Labs

The MultiplyLabsChallenge.py file acts as a software driver to interface with the Multiply Labs robot and communicate via the Telnet protocol in python. The code incorporates a Robot class with several member functions that provide functionality for various commands, such as connecting to the robot, movement to any station, returning the current position of the robot, teaching the robot new pick/place points, loading prior station data, saving station data for later use, moving the robot via joint angles or cartesian coordinates, and more. The TCP Command Server User's Guide and PARobot Plug-In for TCS were heavily utilized in the creation of this driver. For ease of use and primarily for repeatability, all the aforementioned functions have been stored within the Robot class to ensure any number of robot objects can be instantiated and run without conflict, as long as each robot is connected via a different port (see TCP Command Server User's Guide page 2 for port naming conventions). Additionally, if one already has a set of sample positions they'd want the robot to move to and be taught, there exists functionality within the driver for such a task via the loadPos and teachPlatePos member functions. A sample sequence to test the driver has been provided below and at the bottom of MultiplyLabsChallenge.py.


<!-- SAMPLE SEQUENCE:

rob1.loadStationLoc("PreviousStations.gpo")
rob1.goToStation(1,5)
currCartCoords = rob1.getCurrPosCart()

print("Current Cartesian Coordinates")
for x in currCartCoords:
    print(x)

rob1.goToStation(3,5)
rob1.goToStation(4,5)

rob1.pickTray(4, 1, 20, False, 10)
rob1.placeTray(8, 1, 20, 20, 10, True, 10)
goalCartCoords = rob1.getGoalPosCart


rob1.goToStation(3,5)
rob1.teachPlatePos(3, 20) -->
