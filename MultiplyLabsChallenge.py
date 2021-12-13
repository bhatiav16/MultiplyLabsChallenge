#Multiply Labs Tech Challenge


#!/usr/bin/env python3
import numpy as np
from telnetlib import Telnet
import csv




# Robot Class
class Robot:

    # Initialization parameters for any robot object created
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.tn = Telnet(HOST, PORT)



    # Loads previously saved station and position data
    # Arguments:
    #   a) stationLocs: Name of the file to load. Erases all previous location and profile data
    #
    # Returns:
    #   No values returned; station and position data stored from loaded file
    def loadStationLoc(self, stationLocs):
        self.tn.write("LoadFile " + stationLocs)




    # Saves current state of station and position data
    # Arguments:
    #   a) stationLocs: Name of the file to save current data to. Erases all previous location and profile data
    #
    # Returns:
    #   No values returned; station and position data saved
    def saveStationLoc(self, stationLocs):
        self.tn.write("StoreFile " + stationLocs)
    



    # Load positions from CSV File
    # Arguments:
    #   a) posData: Name of the CSV file to load which must contain rows of position data in the format below.
    #               The first element of each row contains a 'C' or 'J', which represents whether the row contains Cartesian or Joint data.
    #               Sample Row: 'C', 0.0, 0.0. 0.0, 0.0, 0.0, 0.0
    #
    # Returns:
    #   a) positionsCart: A list of all positions saved as Cartesian coordinates (X,Y,Z, Yaw, Pitch, Roll)
    #   b) positionsJoints: A list of all positions saved as Joint Angles, where each angle corresponds to each joint starting from the base joint 
    def loadPos(self, posData):

        positionsCart = []
        positionsJoints = []

        with open(posData, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader) #skip the header row

            for loc in csvreader:
                if loc[0] == 'C':
                    pos = loc[1:end]
                    positionsCart.append(pos)
                elif loc[0] == 'J':
                    pos = loc[1:end]
                    positionsJoints.append(pos)

        return positionsCart, positionsJoints




    # Teach plate positions to robot arm
    # Arguments:
    #   a) stationInd: Station number containing plate; indices for stations go from 1 to max number of stations stored
    #   b) zClearance: Clearance value in z-direction; must be large enough to withdraw gripper 
    def teachPlatePos(self, stationInd, zClearance):

        if zClearance <= 0:
            self.tn.write("TeachPlate " + str(stationInd))
        else:
            self.tn.write("TeachPlate " + str(stationInd) + " " + str(zClearance))




    # Command robot to go to specific station
    # Arguments:
    #   a) stationInd: Station number robot should move to; indices for stations go from 1 to max number of stations stored
    #   b) profileInd: Stored profile value containing information regarding speed, acceleration, deceleration, etc. 
    def goToStation(self, stationInd, profileInd):
        self.tn.write("Move " + str(stationInd) + " " + str(profileInd))




    # Move robot to specific position input provided as cartesian coordinates
    # Arguments:
    #   a) profileInd: Stored profile value containing information regarding speed, acceleration, deceleration, etc. 
    #   b) pos: position values stored as list containing X,Y,Z, Yaw, Pitch, Roll values
    def moveCart(self, profileInd, pos):
        self.tn.write("MoveC " + str(profileInd) + " " + str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) \
                                                 + " " + str(pos[3]) + " " + str(pos[4]) + " " + str(pos[5]))




    # Move robot to specific position input provided as joint angle configurations
    # Arguments:
    #   a) profileInd: Stored profile value containing information regarding speed, acceleration, deceleration, etc. 
    #   b) pos: position values stored as list containing joint angles for each joint of robot - this example is for 6-joint robot
    def moveJoints(self, profileInd, pos):
        self.tn.write("MoveJ " + str(profileInd) + " " + str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) \
                                                 + " " + str(pos[3]) + " " + str(pos[4]) + " " + str(pos[5]))




    # Report robot's current position in cartesian coordinates
    # Arguments:
    #   self
    #
    # Returns:
    #   a) data: Current position of robot returned in cartesian coordinates (X, Y, Z, Yaw, Pitch, Roll)
    def getCurrPosCart(self):
        reply, data = self.tn.write("wherec")
        return data




    # Report robot's current position in joint angles
    # Arguments:
    #   self
    #
    # Returns:
    #   a) data: Current position of robot returned in joint angles 
    def getCurrPosJoints(self):
        reply, data = self.tn.write("wherej")
        return data




    # Report robot's goal position in cartesian coordinates
    # Arguments:
    #   self
    #
    # Returns:
    #   a) data: Goal position of robot returned in cartesian coordinates or current pos. if robot not moving (X, Y, Z, Yaw, Pitch, Roll)
    def getGoalPosCart(self):
        reply, data = self.tn.write("DestC")
        return data




    # Report robot's goal position in desired joint angles
    # Arguments:
    #   self
    #
    # Returns:
    #   a) data: Goal position of robot returned in joint angles or current joint angles if robot not moving
    def getGoalPosJoints(self):
        reply, data = self.tn.write("DestJ")
        return data




    # Pick up tray from given position
    # Arguments:
    #   a) stationInd: Station number containing plate; indices for stations go from 1 to max number of stations stored
    #   b) enableCompl: If value=1, horizontal compliance enabled while closing gripper. If not needed, put 0.
    #   c) percentTorque: % of original horizontal torque to be used
    #   d) teachPlate: Boolean indicating whether this position is to be taught to robot (if yes, true)
    #   e) zClearance: Clearance value in z-direction; must be large enough to withdraw gripper 
    def pickTray(self, stationInd, enableCompl, percentTorque, teachPlate, zClearance):
        graspSuccess = self.tn.write("PickPlate " + str(stationInd) + " " + enableCompl + " " + str(percentTorque)) #uses GraspPlate in backend
        if graspSuccess == -1:
            print("Successfully grasped plate!")
        else:
            print("No plate detected!")

        if teachPlate == True:
            self.teachPlatePos(stationInd, zClearance)




    # Place tray at another location; *PlacePlate ends with gripper still closed on plate, so ReleasePlate is called at the end
    # Arguments:
    #   a) stationInd: Station number containing plate; indices for stations go from 1 to max number of stations stored
    #   b) enableCompl: If value=1, horizontal compliance enabled while placing plate. If not needed, put 0.
    #   c) percentTorque: % of original horizontal torque to be used
    #   d) openWidth: How much to open gripper by to release plate (mm)
    #   e) percentSpeed: Speed at which to open gripper fingers (1 - 100)
    #   f) teachPlate: Boolean indicating whether this position is to be taught to robot (if yes, true)
    #   g) zClearance: Clearance value in z-direction; must be large enough to withdraw gripper 
    def placeTray(self, stationInd, enableCompl, percentTorque, openWidth, percentSpeed, teachPlate, zClearance):
        self.tn.write("PlacePlate " + str(stationInd) + " " + enableCompl + " " + str(percentTorque))

        if teachPlate == True:
            self.teachPlatePos(stationInd, zClearance)

        #Now need to release the plate, since above command ends with plate still gripped, and before next movement, want to release plate
        self.tn.write("ReleasePlate " + str(openWidth) + " " + str(percentSpeed))




    # Close connection to the robot over Telnet
    def closeConnection():
        self.tn.close()





# Connect to robot IP address over specific port
HOST = '192.168.0.1' # Host would be robot IP and port is 10100 for robot 1 assuming only one robot listed
PORT = 10100
rob1 = Robot(HOST, PORT) #constructor will establish connection, so don't need to use open explicitly otherwise reopening connection




# SAMPLE SEQUENCE:

# rob1.loadStationLoc("PreviousStations.gpo")
# rob1.goToStation(1,5)
# currCartCoords = rob1.getCurrPosCart()

# print("Current Cartesian Coordinates")
# for x in currCartCoords:
#     print(x)

# rob1.goToStation(3,5)
# rob1.goToStation(4,5)

# rob1.pickTray(4, 1, 20, False, 10)
# rob1.placeTray(8, 1, 20, 20, 10, True, 10)
# goalCartCoords = rob1.getGoalPosCart


# rob1.goToStation(3,5)
# rob1.teachPlatePos(3, 20)






