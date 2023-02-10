# Aidan McEnaney
# February 9th, 2023
# Code to recreate model from the following paper:
## https://www.sciencedirect.com/science/article/abs/pii/0378475486900510

import numpy as np

def shift(arr, num, fill_value=np.nan): # Shifts array, not in paper
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result

def movement(roads, speedingMove, regMove, speedingProb, light = 0): # Exactly as described in Paper
    for i in range(len(roads)):
        dispersionFaster = np.random.choice([0, 1], size=(roadSize,), p=[1-speedingProb, speedingProb])
        tmpAnd = 1*(np.logical_and(roads[i], dispersionFaster)) # Isolates cars that have been selected to move faster
        tmpShift = shift(tmpAnd, speedingMove, 0) # Moves all cars baseMove steps to the right
        tmpInv = 1 - roads[i] # Changes 1s and 0s to 0s and 1s
        tmpAnd = 1*(np.logical_and(tmpInv, tmpShift))
        newShift = shift(tmpAnd, -1, 0)
        tmpXor = 1*(np.logical_xor(roads[i], newShift))
        newPat = 1*(np.logical_or(tmpXor, tmpAnd)) # Now we have moved any cars that got extra movement
        roads[i] = shift(newPat, regMove, 0)

    return roads

def lane_change(roads, changeProb): # Exactly as defined in paper
    for i in range(len(roads)):
        laneChange1 = np.random.choice([0, 1], size=(roadSize,), p=[1-changeProb, changeProb]) # Ones here indicate car in that spot in road will move faster
        moveCand = 1*(np.logical_and(roads[i], laneChange1))
        tmpShift = shift(moveCand, 1, 0)
        zeroByte = 1*(np.logical_and(roads[i], tmpShift))
        if np.sum(zeroByte == 0):
            hatchCheck = 1*(np.logical_and(roads[i%2], tmpShift))
            laneChange = 1*(np.logical_xor(tmpShift, hatchCheck))
            newShift = shift(laneChange, -1, 0)
            freeCheck = 1*(np.logical_and(roads[i%2], newShift))
            if np.sum(freeCheck == 0):
                roads[i%2] = 1*(np.logical_or(roads[i%2], laneChange))
                roads[i] = 1*(np.logical_xor(roads[i], newShift))
    return roads

def lights(roads, i): # Was not explained in paper, made up my own routine here
    copies = []
    if np.amax(np.asarray(roads[i]>0).nonzero()) == (len(roads[i])  - 1):
        copies[i] = np.array(roads[i], copy=True) 
        roads[i] = roads[i][0: np.amax(np.asarray(roads[i]==0).nonzero())]
        #np.amax(np.asarray(roads[i]>0).nonzero())
    elif (np.amax(np.asarray(roads[i]>0).nonzero()) - (len(roads[i]) - 1) > (regMove * 2)):
        copies[i] = np.array(roads[i], copy=True) 

def turning(roads): # Likely deviates from paper, as this part was not covered in depth, or really at all
    # Only called if we have a car at the end of road
    # If three or more cars are waiting, light turns green

    return 0

# Initialization step

roads = []
roadSize = 30
baseMove = 1 # This the additional movement that cars driving faster make
regMove = 4 # This is the movement all cars make
roadAmt = 2

for i in range(roadAmt): # Initializes the roads
    roads.append(np.random.choice([0, 1], size=(roadSize,), p=[4./5, 1./5]))

print(roads[0])

roads = movement(roads, baseMove, regMove, 1/3) # Calls Movement function
roads = lane_change(roads, 1/4) # Calls Lane Change function


while(False):
    roads = movement([initRoad1, initRoad2], baseMove, regMove, 1/3)
    #initRoad1 = roads[0]
    #initRoad2 = roads[1]

    roads = lane_change(roads, 1/4)
    #initRoad1 = roads[0]
    #initRoad2 = roads[1]
    break

print(roads[0])