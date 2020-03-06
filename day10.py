import numpy as np
import math

def getAsteroids(grid):
    # get coordinates of asteroids
    hashes = np.nonzero(grid.find(b'.'))
    asteroids = [(t2, t1) for t1, t2 in zip(hashes[0], hashes[1])] 
    return asteroids


def computeAnglesDistances(asteroids):
    # get angles and distances between asteroids
    angles = np.zeros((len(asteroids), len(asteroids)))
    distances = np.zeros((len(asteroids), len(asteroids)))
    
    for i, astr1 in enumerate(asteroids):
        for j, astr2 in enumerate(asteroids):
            if astr1 == astr2:
                angles[i][j] = None
                continue
            distances[i][j] = abs(astr1[0] - astr2[0]) + abs(astr1[1] - astr2[1])
            # use arctan to find angles
            angles[i][j] = math.atan2(astr1[0] - astr2[0], astr1[1] - astr2[1])
            
    return angles, distances


def findStationLocation(grid):
    asteroids = getAsteroids(grid)    
    angles, _ = computeAnglesDistances(asteroids)  

    # for each asteroid find number of detected asteroids (without Nan)
    detected = [len(np.unique(angle)) - 1 for angle in angles]

    # find the index of the max value
    index = detected.index(max(detected))

    return index, max(detected)


def reversedDictionary(station_angles):
    dictionary, flipped = {}, {}
    # create dictionary that holds indices (keys) and their angles (values)
    for i, angle in enumerate(station_angles):
        dictionary[i] = angle
    
    # reverse dictionary that holds angles (keys) and their indices (values) - to check for duplicates
    for key, value in dictionary.items(): 
        if value not in flipped: 
            flipped[value] = [key] 
        else: 
            flipped[value].append(key)
    
    return flipped


def destroyAsteroids(grid):    
    asteroids = getAsteroids(grid)
    angles, distances = computeAnglesDistances(asteroids)

    # get monitoring station and its angles and distances towards other asteroids
    station_angles = angles[findStationLocation(grid)[0]]
    station_distances = distances[findStationLocation(grid)[0]]

    flipped = reversedDictionary(station_angles)
    destroid_asteroids = []

    while len(flipped) > 0:
        closest_angles_indices = []
        # find which asteroids are closest to the station
        for _, value in flipped.items():
            if len(value) == 1:
                closest_angles_indices.append(value[0])
                del value[0]
            elif len(value) > 1:
                index = np.argmin(station_distances[value])
                closest_angles_indices.append(value[index])
                del value[index]        

        # delete keys if values are empty (i.e. asteroids are destroid)
        filtered = {k: v for k, v in flipped.items() if len(v) > 0}
        flipped.clear()
        flipped.update(filtered)

        closest_angles_indices.sort()

        for i in range(len(station_angles)):
            if i not in closest_angles_indices:
                closest_angles_indices.insert(i, False)

        def selectQuadrant(interval1, interval2):
            # select only indices that fall in between the intervals and are not duplicate
            indices = np.where(np.logical_and(station_angles <= interval1,
                                    station_angles > interval2) * closest_angles_indices)
            indices = list(filter(lambda x: x in closest_angles_indices, indices[0]))   

            # sort descending (clockwise)
            sorted_indices = station_angles[indices].argsort()[::-1]

            # determine order of asteroid destruction
            asteroid_indices = [indices[index] for index in sorted_indices]
            
            return asteroid_indices


        # find all angles in first/fourth/third/second quadrant 
        first_indices = selectQuadrant(0,-math.pi/2)
        fourth_indices = selectQuadrant(-math.pi/2,-math.pi)
        third_indices = selectQuadrant(math.pi,math.pi/2)
        second_indices = selectQuadrant(math.pi/2,0)

        # add the indeces in order of destruction
        destroid_asteroids.extend(first_indices)
        destroid_asteroids.extend(fourth_indices)
        destroid_asteroids.extend(third_indices)
        destroid_asteroids.extend(second_indices)

    return destroid_asteroids


def findCoordinates(grid):
    asteroids = getAsteroids(grid)
    destroid_asteroids = destroyAsteroids(grid)

    return asteroids[destroid_asteroids[199]]

#-----------------------------------------------------------------------------------------------------------#

f = open('day10_input.txt').read().strip().split('\n')
grid = np.chararray((len(f), len(f[0])))

for i in range(grid.shape[0]):                  # pylint: disable=E1136  # pylint/issues/3139
    for j in range(grid.shape[1]):              # pylint: disable=E1136  # pylint/issues/3139
        grid[i][j] = f[i][j]

coordinates = findCoordinates(grid)
print(coordinates[0] * 100 + coordinates[1])