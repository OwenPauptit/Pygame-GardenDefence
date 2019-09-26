import pygame, main

########################################################################################################################


class Enemy:
    def __init__(self,type,animLen):
        self.images = []
        self.animLen = animLen
        self.type = type
        for i in range(1,animLen+1):
            self.images.append(pygame.image.load("Images\\"+type+"_"+str(i)+".png"))
        # self.imageOrig = pygame.image.load("enemy_1.png")
        # self.rotations = [-15,-7.5,0,7.5,15,7.5,0,-7.5]
        self.state = 0
        self.counter = 0
        #self.imageRota = pygame.transform.rotate(self.imageOrig,self.rotations[self.state])
        self.path = [(-50,222),(117,229),(243,221),(398,194),(503,110),(621,70),(734,104),(809,198),(825,300),(882,362),(946,422),(953,514),(940,620),(880,635),(802,610),(745,580),(741,468),(635,422),(531,421),(492,466),(444,548),(326,600),(163,550),(97,450),(-50,450)]
        self.pathPos = 0
        self.currentIm  = self.images[self.state]
        self.pos = self.currentIm.get_rect().move(self.path[self.pathPos])
        self.targetSet = False
        self.alive = True
        self.slowRate = 1
        self.slowCount = 0
        self.asignSpec()
        self.calcHealthBar()

    ####################################################################################################################

    def move(self):
        if self.slowCount > 0:
            self.slowCount -= 0.5
            if self.slowCount < 50:
                self.slowCount = 0
                self.slowRate = 1
        if not self.targetSet:
            self.targetSet = True
            nx = self.path[self.pathPos + 1][0]
            ny = self.path[self.pathPos + 1][1]
            xchange = nx - self.pos.x
            ychange = ny - self.pos.y

            if xchange > 0:
                self.xdir = 1
            else:
                self.xdir = -1
            if ychange > 0:
                self.ydir = 1
            else:
                self.ydir = -1

            if abs(xchange) > abs(ychange):
                self.xinc = 1 * self.speed
                self.yinc = (abs(ychange) / abs(xchange)) * self.speed
            else:
                self.yinc = 1 * self.speed
                self.xinc = (abs(xchange) / abs(ychange)) * self.speed
            self.exactx = self.pos.x
            self.exacty = self.pos.y

        self.exactx += (self.xinc * self.xdir) / self.slowRate
        self.exacty += (self.yinc * self.ydir) / self.slowRate
        self.pos.x = int(round(self.exactx, 0))
        self.pos.y = int(round(self.exacty, 0))

        ################################################################################################################

        if (self.pos.x == self.path[self.pathPos + 1][0] and self.pos.y == self.path[self.pathPos + 1][1]) or (self.exactx > self.path[self.pathPos+1][0] - (1.5*self.speed) and self.exactx < self.path[self.pathPos+1][0] + (1.5*self.speed) and self.exacty > self.path[self.pathPos+1][1] - (1.5*self.speed) and self.exacty < self.path[self.pathPos+1][1] + (1.5*self.speed)):
            self.pathPos += 1
            self.targetSet = False

        ################################################################################################################

        self.counter += 1
        if self.counter > self.animLen*0.8/self.speed:
            self.changeState()
            self.counter =0
        self.currentIm = self.images[self.state]
        if self.xdir == -1: self.currentIm = pygame.transform.flip(self.currentIm,True,False)

        self.calcHealthBar()

    ####################################################################################################################

    def changeState(self):
        if self.state == len(self.images)-1:
            self.state = 0
        else:
            self.state += 1

    ####################################################################################################################

    def asignSpec(self):
        if self.type == "Spider":
            self.fullHealth = 3
            self.health = self.fullHealth
            self.speed = 1#1.25
            self.value = 1
        elif self.type == "Slug":
            self.fullHealth = 8
            self.health = self.fullHealth
            self.speed = 0.5
            self.value = 2
        elif self.type == "Mosquito":
            self.fullHealth = 2
            self.health = self.fullHealth
            self.speed = 5
            self.value = 0

    ####################################################################################################################

    def isHit(self,x,y):
        if x > self.pos.left and x < self.pos.right and y > self.pos.top and y < self.pos.bottom:
            self.health -= 1
            if self.health == 0:
                self.alive = False

    ####################################################################################################################

    def calcHealthBar(self):
        x = self.pos.centerx - (self.health*6) / 2
        y = self.pos.top - 8
        self.hBarOuter = (x-2,y-2,self.fullHealth*6+4,8)
        self.hBarInnerR = (x, y, self.fullHealth * 6, 4)
        self.hBarInnerG = (x,y,self.health*6,4)

########################################################################################################################


if __name__ == "__main__":
    main.initialise()