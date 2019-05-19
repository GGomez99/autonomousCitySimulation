import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.clock import Clock
from random import randint
from random import random
from functools import partial
from kivy.core.window import Window

global animDurRoad
global animDurInt
global mode

animDurInt = 0.3
animDurRoad = 0.3
mode = "Infinite"

class Car(Widget):
    angle = NumericProperty(0)
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

class VertRoad(Widget):
    '''
    vertroad queue pos:
            |0   |
            |    |
            |   1|
    '''

    global doNextAnim

    roadWidth = NumericProperty(0)
    roadLength = NumericProperty(0)
    xPos = NumericProperty(0)
    yPos = NumericProperty(0)

    def __init__(self, **kwargs):
        super(VertRoad, self).__init__(**kwargs)
        self._doNextMoveF = []
        self._pathAnim = [
            [
                [[]] * self.roadLength,
                [[]] * self.roadLength
            ],
            [
                [[]] * self.roadLength,
                [[]] * self.roadLength
            ]
        ]

    def calcPos(self):
        c = self.center
        o = [c[0] - 20, c[1] + self.height / 2 - 20, c[1] - self.height / 2 - 20]
        for i in range(0, len(self._pathAnim[0][0])):
            for way in range(0, 2):
                for j in range(0, 2):
                    self._pathAnim[way][j][i] = [
                        (1 - j) * (o[0] + (2 * way - 1) * 40 * 3) + j * (o[0] + (2 * way - 1) * 40),
                        o[2 - way] + (-2 * way + 1) * (i * 2 + 1) * 40,
                    ]

    def move(self, carData, futurePos, dur):
        car = carData[0][3]
        def onFinish(carData, anim, widget, *largs):
            doNextAnim.pop()
            carData[1] = "Waiting"

        anim = Animation(pos=futurePos, duration=dur)
        doNextAnim.append(False)
        anim.start(car)
        anim.bind(on_complete=partial(onFinish, carData))


    def roadProg(self):

        if loaded:
            if self._pathAnim[0][0][0] == []:
                self.calcPos()
            queue = currentMat[self.xPos][self.yPos]

            # check queue
            for direction in range(0, 2):
                for way in range(0, 2):
                    for i in range(1, roadLength-1):
                        carData = queue[direction][way][i]
                        nextCarData = queue[direction][way][i-1]
                        if carData != None:
                            if carData[1] == "Waiting" and nextCarData == None:
                                queue[direction][way][i] = None
                                queue[direction][way][i - 1] = carData
                                carData[1] = "Moving"
                                self.move(carData, self._pathAnim[direction][way][i-1], animDurRoad)

                    lastRoadQueue = queue[direction][way][roadLength-1]
                    carAtEndRoad = lastRoadQueue[0]
                    if queue[direction][way][roadLength-2] == None and carAtEndRoad != None:
                        lastRoadQueue[0] = None
                        queue[direction][way][roadLength - 2] = carAtEndRoad
                        carAtEndRoad[1] = "Moving"
                        self.move(carAtEndRoad, self._pathAnim[direction][way][roadLength - 2], animDurRoad)
                    if carAtEndRoad == None:
                        newRoadQueue = {0: None}
                        for key, car in lastRoadQueue.items():
                            if car!= None:
                                newRoadQueue[key-1] = car
                        queue[direction][way][roadLength - 1] = newRoadQueue



    def doTurn(self, *largs):
        self.roadProg()



class HorizRoad(Widget):
    '''
    horizRoad queue pos:
            ________
                    1
           0________
    '''

    global doNextAnim

    roadWidth = NumericProperty(0)
    roadLength = NumericProperty(0)
    xPos = NumericProperty(0)
    yPos = NumericProperty(0)

    def __init__(self, **kwargs):
        super(HorizRoad, self).__init__(**kwargs)
        self._doNextMoveF = []
        self._pathAnim = [
            [
                [[]] * self.roadLength,
                [[]] * self.roadLength
            ],
            [
                [[]] * self.roadLength,
                [[]] * self.roadLength
            ]
        ]

    def calcPos(self):
        c = self.center
        if self.xPos == 1:
            c[1] = ttLength - 160
        o = [c[0] + self.width / 2 - 20, c[0] - self.width / 2 - 20, c[1] - 20]
        for i in range(0, len(self._pathAnim[0][0])):
            for way in range(0, 2):
                for j in range(0, 2):
                    self._pathAnim[way][j][i] = [
                        o[way] + (2 * way - 1) * (i * 2 + 1) * 40,
                        (1 - j) * (o[2] + (2 * way - 1) * 40 * 3) + j * (o[2] + (2 * way - 1) * 40),
                    ]

    def move(self, carData, futurePos, dur):
        car = carData[0][3]
        def onFinish(carData, anim, widget, *largs):
            doNextAnim.pop()
            carData[1] = "Waiting"

        anim = Animation(pos=futurePos, duration=dur)
        doNextAnim.append(False)
        anim.start(car)
        anim.bind(on_complete=partial(onFinish, carData))


    def roadProg(self):

        if loaded:
            if self._pathAnim[0][0][0] == []:
                self.calcPos()
            queue = currentMat[self.xPos][self.yPos]
            # check queue
            for direction in range(0, 2):
                for way in range(0, 2):
                    for i in range(1, roadLength-1):
                        carData = queue[direction][way][i]
                        nextCarData = queue[direction][way][i-1]
                        if carData != None:
                            if carData[1] == "Waiting" and nextCarData == None:
                                queue[direction][way][i] = None
                                queue[direction][way][i - 1] = carData
                                carData[1] = "Moving"
                                self.move(carData, self._pathAnim[direction][way][i-1], animDurRoad)

                    lastRoadQueue = queue[direction][way][roadLength-1]
                    carAtEndRoad = lastRoadQueue[0]
                    if queue[direction][way][roadLength-2] == None and carAtEndRoad != None:
                        lastRoadQueue[0] = None
                        queue[direction][way][roadLength - 2] = carAtEndRoad
                        carAtEndRoad[1] = "Moving"
                        self.move(carAtEndRoad, self._pathAnim[direction][way][roadLength - 2], animDurRoad)
                    if carAtEndRoad == None:
                        newRoadQueue = {0: None}
                        for key, car in lastRoadQueue.items():
                            if car != None:
                                newRoadQueue[key-1] = car
                        queue[direction][way][roadLength - 1] = newRoadQueue

                #if self.xPos == 3 and self.yPos == 2 : print("state : " + str(queue))

        '''def addRandomCars(self, *largs):
            startPt = (randint(0, 3), randint(0, 1))
            destination = (randint(0, 2), randint(0, 1))
            coord = (randint(0, 1), randint(0, 1))
            car = Car(r=random() * 0.4 + 0.5, g=random() * 0.4 + 0.5, b=random() * 0.4 + 0.5)
            currentMat[self.xPos][self.yPos][coord[0]][coord[1]].append(
                [[0, startPt, destination, car],
                 -2])
            self.add_widget(car)
            self.move(car, self._pathAnim[coord[0]][coord[1]][-1], 0)
            print(inQueue[self.xPos][self.yPos])'''

    def doTurn(self, *largs):
        self.roadProg()

class Grass(Widget):
    pass

class Intersec(Widget):

    '''
    car model : [id, where come from, where to go]
    where to go: (turns, nbr way(0 or 1))
    turns: forward(1),right(0),left(2)
    intersec path[pos]:
                _|0   |_
                        3
               1_      _
                 |   2|
    '''

    global currentMat
    global roadLength
    global doNextAnim

    def __init__(self, **kwargs):
        super(Intersec, self).__init__(**kwargs)
        self._doNextMoveF = []
        self._doNextMoveR = []
    xPos = NumericProperty(0)
    yPos = NumericProperty(0)
    roadWidth = NumericProperty(0)

    def intersecProg(self):

        if loaded:
            inter = currentMat[self.xPos][self.yPos]
            inQueue = [currentMat[self.xPos - 1][self.yPos][0], currentMat[self.xPos][self.yPos - 1][0], currentMat[self.xPos + 1][self.yPos][1], currentMat[self.xPos][self.yPos + 1][1]]
            outQueue = [currentMat[self.xPos - 1][self.yPos][1], currentMat[self.xPos][self.yPos - 1][1], currentMat[self.xPos + 1][self.yPos][0], currentMat[self.xPos][self.yPos + 1][0]]

            c = self.center
            c = [c[0] - 20, c[1] - 20]
            nbrWays = 2
            roadAlign = 40
            dirToTake = ((1, 0), (0, 1), (-1, 0), (0, -1))
            startPos = (((0, 0), (0, 1)), ((3, 0), (2, 0)), ((3, 3), (3, 2)), ((0, 3), (1, 3)))
            endPos = (((0, 3), (0, 2)), ((0, 0), (1, 0)), ((3, 0), (3, 1)), ((3, 3), (2, 3)))

            pathAnim = [
                ((c[0] - roadAlign * 3, c[1] + roadAlign * 3), (c[0] - roadAlign, c[1] + roadAlign * 3), (c[0] + roadAlign, c[1] + roadAlign * 3), (c[0] + roadAlign * 3, c[1] + roadAlign * 3)),
                ((c[0] - roadAlign * 3, c[1] + roadAlign), (c[0] - roadAlign, c[1] + roadAlign), (c[0] + roadAlign, c[1] + roadAlign), (c[0] + roadAlign * 3, c[1] + roadAlign)),
                ((c[0] - roadAlign * 3, c[1] - roadAlign), (c[0] - roadAlign, c[1] - roadAlign), (c[0] + roadAlign, c[1] - roadAlign), (c[0] + roadAlign * 3, c[1] - roadAlign)),
                ((c[0] - roadAlign * 3, c[1] - roadAlign * 3), (c[0] - roadAlign, c[1] - roadAlign * 3), (c[0] + roadAlign, c[1] - roadAlign * 3), (c[0] + roadAlign * 3, c[1] - roadAlign * 3)),
            ]
            inQueueAnim = [
                ((c[0] - roadAlign * 3, c[1] + roadAlign * 5), (c[0] - roadAlign, c[1] + roadAlign * 5)),
                ((c[0] - roadAlign * 5, c[1] - roadAlign * 3), (c[0] - roadAlign * 5, c[1] - roadAlign)),
                ((c[0] + roadAlign * 3, c[1] - roadAlign * 5), (c[0] + roadAlign, c[1] - roadAlign * 5)),
                ((c[0] + roadAlign * 5, c[1] + roadAlign * 3), (c[0] + roadAlign * 5, c[1] + roadAlign))
            ]
            outQueueAnim = [
                ((c[0] + roadAlign * 3, c[1] + roadAlign * 5), (c[0] + roadAlign, c[1] + roadAlign * 5)),
                ((c[0] - roadAlign * 5, c[1] + roadAlign * 3), (c[0] - roadAlign * 5, c[1] + roadAlign)),
                ((c[0] - roadAlign * 3, c[1] - roadAlign * 5), (c[0] - roadAlign, c[1] - roadAlign * 5)),
                ((c[0] + roadAlign * 5, c[1] - roadAlign * 3), (c[0] + roadAlign * 5, c[1] - roadAlign))
            ]


            def moveCar(carData, futurePos, ttDur):
                car = carData[0]
                oldPos = car[3].pos[:]
                angle = car[3].angle
                movex, movey = futurePos[0] - oldPos[0], futurePos[1] - oldPos[1]
                if movex < 0:
                    correctAngle = 270
                    if angle == 0: correctAngle = -90
                elif movex > 0:
                    correctAngle = 90
                elif movey < 0:
                    correctAngle = 0
                    if angle == 270: correctAngle = 360
                else:
                    correctAngle = 180

                def forwardAnim(futurePos, dur, carData, *largs):
                    doNextAnim.pop()
                    anim = Animation(pos=futurePos, duration=ttDur-dur)
                    doNextAnim.append(False)
                    anim.start(largs[1])
                    anim.bind(on_complete=partial(onFinish, carData))

                dur = ttDur*0.1
                if correctAngle == angle: dur = 0
                doNextAnim.append(False)
                rotat = Animation(angle=correctAngle, duration=dur)
                rotat.start(car[3])
                rotat.bind(on_complete=partial(forwardAnim, futurePos, dur, carData))


            def checkPass(currentPos, posToGo, time):
                if time in inter[posToGo[0]][posToGo[1]]:
                    potBlocCar = inter[posToGo[0]][posToGo[1]][time][0]
                    if potBlocCar[2][0] == 1 and potBlocCar[1][1] != potBlocCar[2][1]:  # check if goes forward and changes way
                        if (time+1) in inter[currentPos[0]][currentPos[1]]:
                            if potBlocCar[0] == inter[currentPos[0]][currentPos[1]][time+1][0]: # check if that car goes where you are
                                return True
                if (time + 1) in inter[posToGo[0]][posToGo[1]]:
                    return True
                else:
                    return False

            def onFinish(carData, anim, widget, *largs):
                doNextAnim.pop()
                carData[1] = "Waiting"


            # move by 1 every car
            for x in range(0, nbrWays*2):
                for y in range(0, nbrWays * 2):
                    newInterCase = {}
                    if inter[x][y] != {0: []}:
                        for time, carData in inter[x][y].items():
                            car = carData[0]
                            carDest = ((car[1][0] + car[2][0][0] + 1) % 4, car[2][0][1])
                            if endPos[carDest[0]][carDest[1]] == (x, y) and time == 0:
                                car[1] = ((carDest[0] + 2) % 4, carDest[1])
                                car[2].pop(0)
                                if mode == "Infinite" and len(car[2]) == 0:
                                    car[2].append((randint(0, 2), randint(0, 1)))
                                #outQueue[carDest[0]][carDest[1]][roadLength-1][0] = [car, "Moving"]          # move car to outqueue if reach destination
                                moveCar([car, "Moving"], outQueueAnim[carDest[0]][carDest[1]], animDurInt)
                            elif time != 0:
                                state = "futurePos"
                                if time == 1: state = "Waiting"
                                newInterCase.update({time - 1: [car, state]})                    # move by 1 on timeline in case
                        inter[x][y] = newInterCase                                     # change the state of the case
                        if 0 in inter[x][y]:
                            newInterCase[0][1] = "Moving"
                            moveCar(newInterCase[0], pathAnim[x][y], animDurInt)

            for road in range(0, len(inQueue)):                         # remove cars inqueue when entering intersec
                for way in range(0, len(inQueue[road])):
                    if inQueue[road][way][0] != None:
                        firstCar = inQueue[road][way][0]
                        if firstCar[1] == 0:
                            inQueue[road][way][0] = None
                        elif isinstance(firstCar[1], int):
                            inQueue[road][way][0][1] -= 1


            # take care of queue (add paths for cars)
            for road in range(0, 4):
                for way in range(0, nbrWays):
                    if inQueue[road][way][0] != None and inQueue[road][way][0][1] == "Waiting":
                        car = inQueue[road][way][0][0]
                        dest = car[2][0]
                        carDest = ((car[1][0] + car[2][0][0] + 1) % 4, car[2][0][1])
                        doNotPath = True
                        markdown = 0
                        testPath = []
                        doAbort = False
                        while doNotPath:                                # search for path
                            doNotPath = False
                            markdown += 1
                            x, y = startPos[car[1][0]][car[1][1]]
                            doNotPath = doNotPath or markdown in inter[x][y]
                            testPath = [markdown]

                            if dest[0] != 1:                          # not forward
                                futurePath = [(x, y)]
                                for i in range(0, dest[0] + abs(dest[1] - int(dest[0]*(1/2)))):         # go straight until facing exit
                                    x, y = x + dirToTake[car[1][0]][0], y + dirToTake[car[1][0]][1]
                                    futurePath.append((x, y))
                                    doNotPath = doNotPath or checkPass(futurePath[-2], (x, y), markdown + i)
                                    testPath.append(markdown + i + 1)

                                x, y = futurePath[-1]
                                markDone = dest[0] + abs(dest[1] - int(dest[0]*(1/2)))
                                for i in range(0, dest[0] + abs(car[1][1] - int(dest[0]*(1/2)))):        # straight after the turn towards exit
                                    turnDir = (car[1][0]+dest[0]-1) % 4
                                    x, y = x + dirToTake[turnDir][0], y + dirToTake[turnDir][1]
                                    futurePath.append((x, y))
                                    doNotPath = doNotPath or checkPass(futurePath[-2], (x, y), markdown + i + markDone)
                                    testPath.append(markdown + i + markDone)


                            else:                                       # forward
                                futurePath = [(x, y)]
                                if car[1][1] != dest[1]:      # if have to change way
                                    indexChange = 0
                                    doNotPath = True
                                    while doNotPath and indexChange < nbrWays*2:
                                        doNotPath = False
                                        testPath = []

                                        x, y = startPos[car[1][0]][car[1][1]]
                                        futurePath = [(x, y)]
                                        doNotPath = doNotPath or markdown in inter[x][y]
                                        testPath.append(markdown)

                                        for i in range(0, nbrWays*2):
                                            if i == indexChange:
                                                changeMovX = startPos[car[1][0]][dest[1]][0] - startPos[car[1][0]][car[1][1]][0]
                                                changeMovY = startPos[car[1][0]][dest[1]][1] - startPos[car[1][0]][car[1][1]][1]
                                                x, y = x + changeMovX, y + changeMovY
                                                doNotPath = doNotPath or (markdown + i) in inter[x][y]
                                                testPath.append("front collide test: " + str(markdown + i))
                                            else:
                                                x, y = x + dirToTake[car[1][0]][0], y + dirToTake[car[1][0]][1]
                                            futurePath.append((x, y))
                                            doNotPath = doNotPath or checkPass(futurePath[-2], (x, y), markdown + i)

                                            testPath.append(markdown + i + 1)
                                        indexChange += 1

                                else:                           # if no change way
                                    for i in range(0, nbrWays * 2 - 1):
                                        x, y = x + dirToTake[car[1][0]][0], y + dirToTake[car[1][0]][1]
                                        futurePath.append((x, y))
                                        doNotPath = doNotPath or checkPass(futurePath[-2], (x, y), markdown + i)

                            #check if way blocked at dest
                            #determine when way is free if (road full of cars or will be full when car arrives)

                            if outQueue[carDest[0]][carDest[1]][0] != None:
                                carNextInter = outQueue[carDest[0]][carDest[1]][0]
                                if carNextInter[1] == "Waiting":
                                    doNotPath = False
                                    doAbort = True
                                elif isinstance(carNextInter[1], int):
                                    nbrOfCarArriving = 0
                                    nbrOfCarInRoad = 0
                                    for i in range(len(outQueue[carDest[0]][carDest[1]])-1):
                                        carDataInRoad = outQueue[carDest[0]][carDest[1]][i]
                                        if carDataInRoad != None:
                                            nbrOfCarInRoad += 1
                                    for key, carOutQueue in outQueue[carDest[0]][carDest[1]][roadLength-1].items():
                                        if key == 0: nbrOfCarInRoad += 1
                                        if key < len(futurePath) and carOutQueue != None and car[1] == "futurePos": nbrOfCarArriving += 1
                                    if nbrOfCarArriving >= nbrOfCarInRoad: blockingTime = carNextInter[1]
                                    else: blockingTime = 0
                                    doNotPath = doNotPath or (markdown + len(futurePath))<blockingTime or (markdown + len(futurePath)) in outQueue[carDest[0]][carDest[1]][roadLength-1]

                        if not(doAbort):
                            for i in range(0, len(futurePath)):             # Add whole path at end timeline
                                x, y = futurePath[i]
                                if (markdown + i) in inter[x][y]:
                                    print("Error duplicate time key " + str(markdown + i))
                                    print("Newkey from" + str(car[0]))
                                    print("    tested " + str(testPath))
                                    print("    adding from " + str(markdown) + " to " + str(markdown + len(futurePath) - 1))
                                    print("Oldkey from" + str(inter[x][y][markdown + i][0]))
                                inter[x][y].update({markdown + i: [car, "futurePos"]})
                            outQueue[carDest[0]][carDest[1]][roadLength - 1][markdown + len(futurePath)] = [car, "futurePos"]

                            '''for i in range(0, 4):
                                for j in range(0, 4):
                                    print("In case " + str(i) + ", " + str(j))
                                    list = []
                                    for key, item in inter[i][j].items():
                                        list.append(str(key) + ": " + str(item[0]))
                                    print(list)'''

                            inQueue[road][way][0][1] = markdown - 1  # Add when car exit inQueue

            '''print("This move:")
            for i in range(0, 4):
                for j in range(0, 4):
                    print("In case " + str(i) + ", " + str(j))
                    list = []
                    for key, item in inter[i][j].items():
                        list.append(str(key)+": "+str(item[0]))
                    print(list)'''

    def doTurn(self, *largs):
        self.intersecProg()


class CityApp(App):

    global citySize
    global ttLength
    global roadWidth
    global roadLength
    global currentMat
    global loaded
    global caseClasses
    global timeC
    global doNextAnim
    global spawnCoord
    global carId

    loaded = False
    citySize = 11
    roadWidth = 320
    roadLength = 20
    ttLength = (int(citySize / 2) + citySize % 2) * roadWidth + int(citySize / 2) * roadLength * 40 * 2
    currentMat = []
    caseClasses = [[[] for j in range(citySize)] for i in range(citySize)]
    timeC = 0
    doNextAnim = []
    spawnCoord = [{} for x in range(citySize+2)]
    carId = 0

    Window.size = (750, 750)

    for x in range(0, citySize+2):
        currentMat.append([])
        for y in range(0, citySize+2):
            caseData = [[{0: None}, {0: None}], [{0: None}, {0: None}]]
            for road in caseData:
                for way in road:
                    for i in range(roadLength - 1):
                        way[i] = None
                    way[roadLength - 1] = {0: None}
            currentMat[x].append(caseData)

    for x in range(1, citySize+1):
        for y in [0, citySize+1]:
            spawnCoord[x][y] = [[], []]
            for i in range(2):
                spawnCoord[x][y][i] = (y/(citySize+1) * (ttLength + 80) - 60, ttLength - roadWidth/2 - (x-1) * (roadLength*40 + roadWidth/2) - 60 - (1-i)*80 + y/(citySize+1)*160)
    for y in range(1, citySize+1):
        for x in [0, citySize+1]:
            spawnCoord[x][y] = [[], []]
            for i in range(2):
                spawnCoord[x][y][i] = (roadWidth/2 + (y-1) * (roadLength*40 + roadWidth/2) - 140 + (1-i)*80 + x/(citySize+1)*160, (1 - x/(citySize+1)) * (ttLength + 80) - 60)

    def addCars(self, city):
        global carId
        startPt = (randint(0, 3), randint(0, 1))
        startCoord = [0, 0, 0, startPt[1]]
        if startPt[0] == 0:
            startCoord[1] = 2*randint(0, citySize//2)+1
            startCoord[3] = 1 - startCoord[3]
        elif startPt[0] == 1:
            startCoord[0] = 2*randint(0, citySize//2)+1
        elif startPt[0] == 2:
            startCoord[0] = citySize+1
            startCoord[1] = 2*randint(0, citySize//2)+1
            startCoord[2] = 1
        else:
            startCoord[0] = 2*randint(0, citySize//2)+1
            startCoord[1] = citySize + 1
            startCoord[2] = 1
            startCoord[3] = 1 - startCoord[3]

        destination = []
        if mode == "Infinite": destination.append((randint(0, 2), randint(0, 1)))
        spawnPos = spawnCoord[startCoord[0]][startCoord[1]][startCoord[3]]
        car = Car(r=random() * 0.4 + 0.5, g=random() * 0.4 + 0.5, b=random() * 0.4 + 0.5, pos=spawnPos)

        if currentMat[startCoord[0]][startCoord[1]][startCoord[2]][startPt[1]][0] == None:
            currentMat[startCoord[0]][startCoord[1]][startCoord[2]][startPt[1]][0] = [[carId, startPt, destination, car], "Waiting"]
            city.add_widget(car)
            carId += 1

    def doStuff(self, city, *largs):
        global timeC
        global doNextAnim
        if len(doNextAnim) == 0:
            if timeC == 1:
                for i in range(200): self.addCars(city)
                timeC = 0
            else: timeC += 1
            for x in range(citySize):
                for y in range(citySize):
                    if x%2 == 0 and y%2 == 0 or (x+y)%2 == 1:
                        caseClasses[x][y].doTurn(doNextAnim)

    '''def status(self, dt):
        print("status : " + str(currentMat[2][3]))'''

    def build(self):

        global loaded

        city = BoxLayout(orientation='vertical', size=(ttLength, ttLength), size_hint=(None, None))

        for x in range(0, citySize):
            row = BoxLayout(orientation='horizontal', size=(ttLength, roadWidth * abs(x%2-1) + roadLength * 40 * 2 * (x%2)), size_hint=(None, None))
            currentMat.append([])
            for y in range(0, citySize):
                if x%2 == 0 and y%2 == 0:       # intersec
                    currentMat[x+1][y+1] = [
                        [{}, {}, {}, {}],
                        [{}, {}, {}, {}],
                        [{}, {}, {}, {}],
                        [{}, {}, {}, {}]
                    ]
                    inter = Intersec(roadWidth=roadWidth, xPos=x+1, yPos=y+1)
                    row.add_widget(inter)
                    caseClasses[x][y] = inter
                elif y%2 == 1 and x%2 == 0:    # horizontal road
                    currentMat[x+1][y+1] = [[{}, {}], [{}, {}]]
                    for road in currentMat[x+1][y+1]:
                        for way in road:
                            for i in range(roadLength):
                                way[i] = None
                            way[roadLength - 1] = {0: None}
                    hRoad = HorizRoad(roadWidth=roadWidth, roadLength=roadLength, xPos=x+1, yPos=y+1)
                    row.add_widget(hRoad)
                    caseClasses[x][y] = hRoad
                elif x%2 == 1 and y%2 == 0:           # vertical road
                    currentMat[x + 1][y + 1] = [[{}, {}], [{}, {}]]
                    for road in currentMat[x + 1][y + 1]:
                        for way in road:
                            for i in range(roadLength-1):
                                way[i] = None
                            way[roadLength-1] = {0: None}
                    vRoad = VertRoad(roadWidth=roadWidth, roadLength=roadLength, xPos=x+1, yPos=y+1)
                    row.add_widget(vRoad)
                    caseClasses[x][y] = vRoad
                else:
                    currentMat[x+1][y+1] = "Empty"
                    row.add_widget(Grass(size=(roadLength*40*2, roadLength*40*2)))
            city.add_widget(row)
        loaded = True

        scatter = Scatter(do_rotation=False, scale=0.5)
        scatter.add_widget(city)
        Clock.schedule_interval(partial(self.doStuff, scatter), 1/120)
        return scatter


if __name__ == '__main__':
    CityApp().run()