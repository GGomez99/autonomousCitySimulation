import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock
from random import randint
from random import random
from functools import partial

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
global animDurRoad
global animDurInt

animDurInt = 0.3
animDurRoad = 1

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
        c = self.center
        o = [c[0] - 20, c[1] + self.height / 2 - 20, c[1] - self.height / 2 - 20]
        for i in range(0, len(self._pathAnim[0][0])):
            for way in range(0, 2):
                for j in range(0, 2):
                    self._pathAnim[way][j][i] = [
                        (1 - j) * (o[0] + (-2 * way + 1) * 40 * 3) + j * (o[0] + (-2 * way + 1) * 40),
                        o[2 - way] + (-2 * way + 1) * (i * 2 + 1) * 40,
                    ]

    def move(self, car, futurePos, dur):

        def popNextMoveF(anim, widget):
            self._doNextMoveF.pop()

        anim = Animation(pos=futurePos, duration=dur)
        self._doNextMoveF.append(False)
        anim.start(car)
        anim.bind(on_complete=partial(popNextMoveF))


    def roadProg(self, *largs):

        if loaded:
            queue = currentMat[self.xPos][self.yPos]

            if len(self._doNextMoveF) == 0:
                # check queue
                for direction in range(0, 2):
                    for way in range(0, 2):
                        for i in range(0, len(queue[direction][way])):
                            if queue[direction][way][i][1] == -2:
                                car = queue[direction][way][-1][0]
                                print(len(self._pathAnim[direction][way]))
                                self.move(car[3], self._pathAnim[direction][way][i], animDurRoad)
                                if i == 0:
                                    queue[direction][way][i][1] = -1
                                else:
                                    queue[direction][way][i][1] = queue[direction][way][i-1][1]+1

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

    def startClock(self):
        Clock.schedule_interval(partial(self.roadProg), 1 / 80)



class HorizRoad(Widget):
    '''
    horizRoad queue pos:
            ________
                    1
           0________
    '''

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
        c = self.center
        o = [c[0] - self.width / 2 - 20, c[0] + self.width / 2 - 20, c[1] - 20]
        for i in range(0, len(self._pathAnim[0][0])):
            for way in range(0, 2):
                for j in range(0, 2):
                    self._pathAnim[way][j][i] = [
                        o[way] + (-2 * way + 1) * (i * 2 + 1) * 40,
                        (1 - j) * (o[2] + (2 * way - 1) * 40 * 3) + j * (o[2] + (2 * way - 1) * 40),
                    ]

    def move(self, car, futurePos, dur):

        def popNextMoveF(anim, widget):
            self._doNextMoveF.pop()

        anim = Animation(pos=futurePos, duration=dur)
        self._doNextMoveF.append(False)
        anim.start(car)
        anim.bind(on_complete=partial(popNextMoveF))

    def roadProg(self, *largs):

        if loaded:
            queue = currentMat[self.xPos][self.yPos]

            if len(self._doNextMoveF) == 0:
                # check queue
                for direction in range(0, 2):
                    for way in range(0, 2):
                        for i in range(0, len(queue[direction][way])):
                            car = queue[direction][way][-1][0]
                            self.move(car[3], self._pathAnim[direction][way][i], animDurRoad)


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

    def startClock(self):
        Clock.schedule_interval(partial(self.roadProg), 1 / 80)

class Grass(Widget):
    pass

class Intersec(Widget):

    global currentMat

    def __init__(self, **kwargs):
        super(Intersec, self).__init__(**kwargs)
        self._doNextMoveF = []
        self._doNextMoveR = []
    xPos = NumericProperty(0)
    yPos = NumericProperty(0)
    roadWidth = NumericProperty(0)

    def intersecProg(self, *largs):

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


            nbrCars = sum([len(way) for way in inQueue])
            def moveCar(car, futurePos, ttDur):
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

                def forwardAnim(futurePos, dur, *largs):
                    self._doNextMoveR.pop()
                    anim = Animation(pos=futurePos, duration=ttDur-dur)
                    self._doNextMoveF.append(False)
                    anim.start(largs[1])
                    anim.bind(on_complete=partial(popNextMoveF))

                dur = ttDur*0.1
                if correctAngle == angle: dur = 0
                self._doNextMoveR.append(False)
                rotat = Animation(angle=correctAngle, duration=dur)
                rotat.start(car[3])
                rotat.bind(on_complete=partial(forwardAnim, futurePos, dur))


            def checkPass(currentPos, posToGo, time):
                if time in inter[posToGo[0]][posToGo[1]]:
                    potBlocCar = inter[posToGo[0]][posToGo[1]][time]
                    if potBlocCar[2][0] == 1 and potBlocCar[1][1] != potBlocCar[2][1]:  # check if goes forward and changes way
                        if (time+1) in inter[currentPos[0]][currentPos[1]]:
                            if potBlocCar[0] == inter[currentPos[0]][currentPos[1]][time+1][0]: # check if that car goes where you are
                                return True
                if (time + 1) in inter[posToGo[0]][posToGo[1]]:
                    return True
                else:
                    return False

            def popNextMoveF(anim, widget):
                self._doNextMoveF.pop()

            if len(self._doNextMoveF)+len(self._doNextMoveR) == 0:
                # move by 1 every car
                for x in range(0, nbrWays*2):
                    for y in range(0, nbrWays * 2):
                        newInterCase = {}
                        if inter[x][y] != {0: []}:
                            for time, car in inter[x][y].items():
                                carDest = ((car[1][0] + car[2][0] + 1) % 4, car[2][1])
                                if endPos[carDest[0]][carDest[1]] == (x, y) and time == 0:
                                    if len(outQueue[carDest[0]][carDest[1]]) > 0:
                                        timeLastCar = outQueue[carDest[0]][carDest[1]][-1][1] + 1
                                    else:
                                        timeLastCar = -1
                                    print(((carDest[0] + 2) % 4, carDest[1]))
                                    car[1] = ((carDest[0] + 2) % 4, carDest[1])
                                    outQueue[carDest[0]][carDest[1]].append([car, timeLastCar])            # move car to outqueue if reach destination
                                    moveCar(car, outQueueAnim[carDest[0]][carDest[1]], animDurInt)
                                elif time != 0:
                                    newInterCase.update({time - 1: car})                    # move by 1 on timeline in case
                            inter[x][y] = newInterCase                                     # change the state of the case
                            if 0 in inter[x][y]:
                                moveCar(newInterCase[0], pathAnim[x][y], animDurInt)

                for road in range(0, len(inQueue)):                         # remove or reduce timer for cars in inqueue
                    for way in range(0, len(inQueue[road])):
                        for i in range(0, len(inQueue[road][way])):
                            item = inQueue[road][way][i]
                            if i == 0 and item[1] == 0:
                                inQueue[road][way].pop(0)
                            if item[1] > 0:
                                item[1] -= 1


                # take care of queue (add paths for cars)
                for road in range(0, 4):
                    for way in range(0, nbrWays):
                        if len(inQueue[road][way]) > 0 and inQueue[road][way][0][1] == -1:
                            car = inQueue[road][way][0][0]
                            doNotPath = True
                            markdown = 0
                            testPath = []
                            while doNotPath:                                # search for path
                                doNotPath = False
                                markdown += 1
                                x, y = startPos[car[1][0]][car[1][1]]
                                doNotPath = doNotPath or markdown in inter[x][y]
                                testPath = [markdown]

                                if car[2][0] != 1:                          # not forward
                                    futurePath = [(x, y)]
                                    for i in range(0, car[2][0] + abs(car[2][1] - int(car[2][0]*(1/2)))):         # go straight until facing exit
                                        x, y = x + dirToTake[car[1][0]][0], y + dirToTake[car[1][0]][1]
                                        futurePath.append((x, y))
                                        doNotPath = doNotPath or checkPass(futurePath[-2], (x, y), markdown + i)
                                        testPath.append(markdown + i + 1)

                                    x, y = futurePath[-1]
                                    markDone = car[2][0] + abs(car[2][1] - int(car[2][0]*(1/2)))
                                    for i in range(0, car[2][0] + abs(car[1][1] - int(car[2][0]*(1/2)))):        # straight after the turn towards exit
                                        turnDir = (car[1][0]+car[2][0]-1) % 4
                                        x, y = x + dirToTake[turnDir][0], y + dirToTake[turnDir][1]
                                        futurePath.append((x, y))
                                        doNotPath = doNotPath or checkPass(futurePath[-2], (x, y), markdown + i + markDone)
                                        testPath.append(markdown + i + markDone)


                                else:                                       # forward
                                    futurePath = [(x, y)]
                                    if car[1][1] != car[2][1]:      # if have to change way
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
                                                    changeMovX = startPos[car[1][0]][car[2][1]][0] - startPos[car[1][0]][car[1][1]][0]
                                                    changeMovY = startPos[car[1][0]][car[2][1]][1] - startPos[car[1][0]][car[1][1]][1]
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
                            for i in range(0, len(futurePath)):             # Add whole path at end timeline
                                x, y = futurePath[i]
                                if (markdown + i) in inter[x][y]:
                                    print("Error duplicate time key " + str(markdown + i))
                                    print("Newkey from" + str(car[0]))
                                    print("    tested " + str(testPath))
                                    print("    adding from " + str(markdown) + " to " + str(markdown + len(futurePath) - 1))
                                    print("Oldkey from" + str(inter[x][y][markdown + i][0]))
                                inter[x][y].update({markdown + i: car})

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

    def startClock(self):
        Clock.schedule_interval(partial(self.intersecProg), 1 / 80)


class CityApp(App):

    global citySize
    global ttLength
    global roadWidth
    global roadLength
    global currentMat
    global loaded

    loaded = False
    citySize = 5
    roadWidth = 320
    roadLength = 5
    ttLength = (int(citySize / 2) + citySize % 2) * roadWidth + int(citySize / 2) * roadLength * 40 * 2
    currentMat = []
    for x in range(0, citySize+2):
        currentMat.append([])
        for y in range(0, citySize+2):
            currentMat[x].append([[[], []], [[], []]])

    def addCars(self, city, *largs):
        startPt = (randint(0, 3), randint(0, 1))
        destination = (randint(0, 2), randint(0, 1))
        car = Car(r=random() * 0.4 + 0.5, g=random() * 0.4 + 0.5, b=random() * 0.4 + 0.5)
        currentMat[2][3][0][0].append(
            [[0, (0, 0), destination, car],
             -1])
        city.add_widget(car)

    def status(self, dt):
        print(currentMat)

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
                    inter.startClock()
                elif y%2 == 1 and x%2 == 0:    # horizontal road
                    currentMat[x][y] = [[[], []], [[], []]]
                    hRoad = HorizRoad(roadWidth=roadWidth, roadLength=roadLength, xPos=+1, yPos=y+1)
                    row.add_widget(hRoad)
                    hRoad.startClock()
                elif x%2 == 1 and y%2 == 0:           # vertical road
                    currentMat[x+1][y+1] = [[[], []], [[], []]]
                    vRoad = VertRoad(roadWidth=roadWidth, roadLength=roadLength, xPos=x+1, yPos=y+1)
                    row.add_widget(vRoad)
                    vRoad.startClock()
                else:
                    currentMat[x+1][y+1] = "Empty"
                    row.add_widget(Grass(size=(roadLength*40*2, roadLength*40*2)))
            city.add_widget(row)
        loaded = True

        scatter = Scatter()
        scatter.add_widget(city)
        Clock.schedule_interval(partial(self.addCars, city), 4)
        return scatter


if __name__ == '__main__':
    CityApp().run()