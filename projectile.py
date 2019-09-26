import pygame, main, math
from pygame.math import Vector2

########################################################################################################################


class Projectile:
    def __init__(self,type,target,level,tower,index):
        self.index = index
        self.tower = tower
        self.type = type
        if self.type == "Archer":
            self.image = pygame.image.load("Images/Arrow.png")
            self.speed = 12
            self.damage = 1 * level
            self.splash = 0
        elif self.type == "Mortar":
            self.image = pygame.image.load("Images/MortarShell.png")
            self.speed = 12
            self.damage = 1 * level
            self.stage = 1
            self.splash = 20 + 5*level
        elif self.type == "Beehive":
            self.image = pygame.image.load("Images/Honey.png")
            self.speed = 12
            self.damage = 0
            self.splash = 0
            self.slowRate = level + 1
        self.speed += level
        self.target = target
        self.pos = self.image.get_rect()
        self.pos.center = self.tower.pos.center
        # self.vpos = Vector2(self.pos.center)
        self.rotate()

    ####################################################################################################################

    def rotate(self):
        # direction = self.target.pos.center - self.vpos
        # _,angle = direction.as_polar()
        #rel_x, rel_y = self.target.pos.centerx - self.pos.centerx, self.target.pos.centery - self.pos.centery
        x = self.target.pos.x - self.pos.x
        y = self.target.pos.y - self.pos.y
        angle = math.degrees(math.atan2(y, x))
        self.currentIm = pygame.transform.rotate(self.image, int(-angle))
        self.pos = self.currentIm.get_rect()
        self.pos.center = self.tower.pos.center

    ####################################################################################################################

    def move(self,enemies):
        if not (self.type == "Mortar" and self.stage == 1):
            nx,ny = self.target.pos.center
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
                try:
                    self.yinc = (abs(ychange) / abs(xchange)) * self.speed
                except ZeroDivisionError:
                    self.yinc = 0
            else:
                self.yinc = 1 * self.speed
                try:
                    self.xinc = (abs(xchange) / abs(ychange)) * self.speed
                except ZeroDivisionError:
                    self.xinc = 0
            self.exactx = self.pos.x
            self.exacty = self.pos.y

            self.exactx += self.xinc * self.xdir
            self.exacty += self.yinc * self.ydir
            self.pos.x = int(round(self.exactx, 0))
            self.pos.y = int(round(self.exacty, 0))

            ############################################################################################################

            if self.pos.right > self.target.pos.left-1 and self.pos.left < self.target.pos.right+1 and self.pos.bottom > self.target.pos.top-1 and self.pos.top < self.target.pos.bottom+1:
                if self.splash == 0:
                    if self.type == "Beehive":
                        self.target.slowRate = self.slowRate
                        self.target.slowCount = 255
                    self.target.health -= self.damage
                else:
                    self.tower.mkEffect(self.pos,self.splash)
                    for e in enemies:
                        if e.pos.right > self.pos.left-self.splash and e.pos.left < self.pos.right+self.splash and e.pos.top < e.pos.bottom + self.splash and e.pos.bottom > self.pos.top - self.splash:
                            e.health -= self.damage
                del self.tower.proj[self.tower.proj.index(self)]

        ########################################################################################################################

        else:
            self.pos.y -= self.speed
            if self.target.pos.x > self.pos.x: self.pos.x += 1
            else: self.pos.x -= 1
            if self.pos.y < -60:
                self.pos.x = self.pos.x + (self.target.pos.x - self.pos.x)/2
                # if self.target.pos.x > self.pos.x:
                #     self.pos.x = (self.target.pos.x - self.pos.x) /2 + self.pos.x
                # else:
                #     self.pos.x = self.pos.x - (self.pos.x - self.target.pos.x)/2
                self.stage += 1

########################################################################################################################


if __name__ == "__main__":
    main.initialise()