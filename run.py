'''
car model : [id, where come from, where to go]
forward(1),right(0),left(2)
intersec path[pos]:
            _|0   |_
                    3
           1_      _
             |   2|

in intercase :
    cars on case ordered by key
        key 0 is an actual car on it
        other keys are future cars
'''
import random as rand

inter1 = [
    [{}, {}],
    [{}, {}]
]

doStop = False
inQueue = [[],[],[],[]]
nbrCars = 7
for i in range(1, nbrCars+1):
    startPt = rand.randint(0, 3)
    inQueue[startPt].append([[i, startPt, rand.randint(0, 2)], -1])

outQueue = [[],[],[],[]]
path = ((0, 0), (1, 0), (1, 1), (0, 1))

while not doStop:

    # move by 1 every car
    for coord in path:
        x, y = coord[0], coord[1]
        newInterCase = {}
        if inter1[x][y] != {0: []}:
            for time, car in inter1[x][y].items():
                carDestination = (car[1] + car[2]) % 4
                if path[carDestination] == coord and time == 0:
                    outQueue[carDestination].append(car)            # move car to outqueue if reach destination
                elif time != 0:
                    newInterCase.update({time - 1: car})    # move by 1 on timeline in case
            inter1[x][y] = newInterCase                     # change the state of the case
    newInQueue = []
    for wayQueue in inQueue:                                # remove or reduce timer for cars in inqueue
        itemToKeep = []
        for i in range(0, len(wayQueue)):
            item = wayQueue[i]
            if item[1] != 0:
                if item[1] != -1:
                    item[1] -= 1
                itemToKeep.append(item)
        newInQueue.append(itemToKeep[:])
    inQueue = newInQueue[:]

    # take care of queue (add paths for cars)
    for way in range(0,4):
        for carIndex in range(0, len(inQueue[way])):
            if inQueue[way][carIndex][1] == -1:
                car = inQueue[way][carIndex][0]
                doNotPath = True
                markdown = 0
                while doNotPath:                # search for path
                    doNotPath = False
                    markdown += 1
                    for i in range(way, way+car[2]+1):
                        pos = i % 4
                        x, y = path[pos][0], path[pos][1]
                        doNotPath = doNotPath or (markdown + i - way) in inter1[x][y]
                for i in range(way, way + car[2] + 1):      # Add whole path at end timeline
                    pos = i % 4
                    x, y = path[pos][0], path[pos][1]
                    inter1[x][y].update({markdown + i - way: car})
                inQueue[way][carIndex][1] = markdown-1      # Add when car exit inQueue


    print "This move:"
    for i in range(0, 2):
        for j in range(0, 2):
            print "In case " + str(i) + ", " + str(j)
            list = []
            for key, item in inter1[i][j].items():
                list.append(str(key) + ": " + str(item[0]))
            print list
    print "       inQueue: " + str(inQueue)
    print "       outQueue: " + str(outQueue)
    if sum([len(way) for way in outQueue]) == nbrCars:
        doStop = True


