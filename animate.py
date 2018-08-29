import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
from random import random
from functools import partial
Window.size = (600, 600)

class BG(Widget):
    pass

class Car(Widget):
    angle = NumericProperty(0)
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

class Layout(FloatLayout):
    pass



class Inter1App(App):

    global doNextMoveF
    global doNextMoveR
    doNextMoveF = []
    doNextMoveR = []

    def intersecProg(self, layout, inQueue, outQueue, inter1, *largs):


        path = ((0, 0), (1, 0), (1, 1), (0, 1))

        c = Window.center
        c = [c[0] - 20, c[1] - 20]
        roadAlign = 40
        pathAnim = [
            (c[0] - roadAlign, c[1] + roadAlign),
            (c[0] - roadAlign, c[1] - roadAlign),
            (c[0] + roadAlign, c[1] - roadAlign),
            (c[0] + roadAlign, c[1] + roadAlign),
        ]
        inQueueAnim = [
            (c[0] - roadAlign, c[1] + roadAlign * 11),
            (c[0] - roadAlign * 11, c[1] - roadAlign),
            (c[0] + roadAlign, c[1] - roadAlign * 11),
            (c[0] + roadAlign * 11, c[1] + roadAlign),
        ]
        outQueueAnim = [
            (c[0] + roadAlign, c[1] + roadAlign * 11),
            (c[0] - roadAlign * 11, c[1] + roadAlign),
            (c[0] - roadAlign, c[1] - roadAlign * 11),
            (c[0] + roadAlign * 11, c[1] - roadAlign),
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
                doNextMoveR.pop()
                anim = Animation(pos=futurePos, duration=ttDur-dur*1.3)
                doNextMoveF.append(False)
                anim.start(largs[1])
                anim.bind(on_complete=partial(popNextMoveF))

            dur = 0.15
            if correctAngle == angle: dur = 0
            doNextMoveR.append(False)
            rotat = Animation(angle=correctAngle, duration=dur)
            rotat.start(car[3])
            rotat.bind(on_complete=partial(forwardAnim, futurePos, dur))


        def popNextMoveF(anim, widget):
            doNextMoveF.pop()

        if len(doNextMoveF)+len(doNextMoveR) == 0:
            # move by 1 every car
            for pathIndex in range(0, len(path)):
                x, y = path[pathIndex][0],  path[pathIndex][1]
                newInterCase = {}
                if inter1[x][y] != {0: []}:
                    for time, car in inter1[x][y].items():
                        carDestination = (car[1] + car[2] + 1) % 4
                        if path[carDestination] == path[(pathIndex+1)%4] and time == 0:
                            outQueue[carDestination].append(car)                            # move car to outqueue if reach destination
                            moveCar(car, outQueueAnim[carDestination], 1)
                        elif time != 0:
                            newInterCase.update({time - 1: car})                    # move by 1 on timeline in case
                    inter1[x][y] = newInterCase                                     # change the state of the case
                    if 0 in inter1[x][y]:
                        moveCar(newInterCase[0], pathAnim[pathIndex], 1)
            newInQueue = []
            for wayQueue in inQueue:                         # remove or reduce timer for cars in inqueue
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
            for way in range(0, 4):
                for carIndex in range(0, len(inQueue[way])):
                    if inQueue[way][carIndex][1] == -1:
                        car = inQueue[way][carIndex][0]
                        doNotPath = True
                        markdown = 0
                        while doNotPath:  # search for path
                            doNotPath = False
                            markdown += 1
                            for i in range(way, way + car[2] + 1):
                                pos = i % 4
                                x, y = path[pos][0], path[pos][1]
                                doNotPath = doNotPath or (markdown + i - way) in inter1[x][y]
                        for i in range(way, way + car[2] + 1):  # Add whole path at end timeline
                            pos = i % 4
                            x, y = path[pos][0], path[pos][1]
                            inter1[x][y].update({markdown + i - way: car})
                        inQueue[way][carIndex][1] = markdown - 1  # Add when car exit inQueue
                        layout.add_widget(car[3])
                        anim = Animation(pos=inQueueAnim[car[1]], duration=0)
                        anim &= Animation(angle=90 * car[1], duration=0)
                        doNextMoveF.append(False)
                        oldPos = car[3].pos[:]
                        anim.start(car[3])
                        anim.bind(on_complete=partial(popNextMoveF))

            '''print "This move:"
            for i in range(0, 2):
                for j in range(0, 2):
                    print "In case " + str(i) + ", " + str(j)
                    list = []
                    for key, item in inter1[i][j].items():
                        list.append(str(key)+": "+str(item[0]))
                    print list'''
    def build(self):

        inQueue = [[], [], [], []]
        inter1 = [
            [{}, {}],
            [{}, {}]
        ]
        outQueue = [[], [], [], []]
        nbrCars = 10
        for i in range(1, nbrCars + 1):
            startPt = randint(0, 3)
            inQueue[startPt].append([[i, startPt, randint(0, 2), Car(r=random()*0.4+0.5, g=random()*0.4+0.5, b=random()*0.4+0.5)], -1])

        layout = Layout()
        layout.add_widget(BG())

        Clock.schedule_interval(partial(self.intersecProg, layout, inQueue, outQueue, inter1), 1/60)
        return layout


if __name__ == '__main__':
    Inter1App().run()