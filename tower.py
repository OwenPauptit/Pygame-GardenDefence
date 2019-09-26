import pygame, main, projectile,time

########################################################################################################################


class Colours:
    red = (255,0,0)
    green = (0,255,0)
    tranluGrey = (80,80,80,180)
    #grass = [(22,121,25),(50,174,53),(49,156,51),(57,171,59),(57,189,61),(33,139,36),(255,255,255),(100,255,255)]

########################################################################################################################


class Tower:
    def __init__(self,type,animLen,screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused=False,loading=False,pos=None):
        self.type = type
        self.animLen = animLen
        self.images = []
        for i in range(1,animLen+1):
            self.images.append(pygame.image.load("Images\\L1"+type+"_"+str(i)+".png"))
        self.state = 0
        self.counter = 0
        self.currentIm = self.images[self.state]
        self.firing = False
        self.proj = []
        self.setAttributes()
        self.pos = self.currentIm.get_rect()
        self.plevel = 1
        self.rlevel = 1
        self.damage = 1
        self.showBtns = False
        self.showUps = False
        self.xdir = 1
        self.plats = []
        self.effects = []
        self.eCounter = []
        if loading:
            self.pos.center = pos
        else:
            self.place(screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused)


    ####################################################################################################################

    def fire(self):
        self.counter += 1
        if self.counter > self.animLen * 1 / self.speed:
            self.changeState()
            self.counter = 0
        self.currentIm = self.images[self.state]
        if self.target.pos.centerx > self.pos.centerx:
            self.currentIm = pygame.transform.flip(self.currentIm,True,False)
            self.xdir = -1
        else:
            self.xdir = 1

    ####################################################################################################################

    def isEnemy(self,enemies):
        if not self.firing:
            for e in enemies:
                shouldFire = True
                if self.type == "Beehive":
                    if e.slowRate > 1:
                        shouldFire = False
                for p in self.proj:
                    if e == p.target and (e.health <= 1 or self.type == "Beehive"):
                        shouldFire = False
                if shouldFire:
                    coords = [e.pos.topleft,e.pos.topright,e.pos.bottomright,e.pos.bottomleft]
                    if self.type == "Archer": self.pos.x += 7
                    for coord in coords:
                        if (coord[0]-self.pos.centerx)**2 + (coord[1]-self.pos.centery)**2 < self.radius**2:
                            self.target = e
                            self.firing = True
                            break
                    if self.type == "Archer": self.pos.x -= 7
                    if self.firing: break
                #if (x1 - self.pos.right < self.radius and x1 - self.pos.right > 0) or (self.pos.left - x2 < self.radius and self.pos.left - x2 > 0) or (y1 - self.pos.bottom < self.radius and y1 - self.pos.bottom > 0) or (self.pos.top - y2 < self.radius and self.pos.top - y2 > 0):
                    # self.target = e
                    # self.firing = True
                    # break
            if self.firing:
                self.changeState()
                self.fire()
        else:
            self.fire()

    ####################################################################################################################

    def changeState(self):

        if self.target.health < 1:
            self.state = 0
            self.firing = False

        if self.type != "Beehive":
            if self.state == len(self.images)-1:
                self.state = 0
                self.firing = False
                i = 1
                while True:
                    if not pygame.mixer.Channel(i).get_busy():
                        if main.Config.sfx == False:
                            pygame.mixer.Channel(1).set_volume(main.Config.volume)
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Sounds\sfx_"+str(self.type)+".wav"))
                        break
                    else:
                        i += 1
                        if i == 9: i = 1
                self.proj.append(projectile.Projectile(self.type,self.target,self.plevel, self,len(self.proj)))
            else:
                self.state += 1
        else:
            if self.state == 3:
                self.state += 1
                self.firing = False
                if main.Config.sfx == False:
                    pygame.mixer.Channel(1).set_volume(main.Config.volume)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("Sounds\sfx_"+str(self.type)+".wav"))
                self.proj.append(projectile.Projectile(self.type,self.target,self.plevel, self,len(self.proj)))
            elif self.state == len(self.images)-1:
                self.state = 0
            else:
                self.state += 1

    ####################################################################################################################

    def setAttributes(self):
        if self.type == "Archer":
            self.speed = 0.3
            self.radius = 100
        elif self.type == "Mortar":
            self.speed = 1
            self.radius = 200
        elif self.type == "Beehive":
            self.speed = 1
            self.radius = 100


    ####################################################################################################################

    def mkEffect(self,pos,splash):
        temp = []
        for i in range(1,7):
            im = pygame.image.load("Images\L1%s-Effect_%s.png" % (self.type,i)) #(self.plevel, self.type, i))
            xm = splash*2
            ym = int((xm / 45) * 30)
            #ym = int(30 * (1 + self.plevel/5 - 0.2))
            im = pygame.transform.scale(im,(xm,ym))
            p = im.get_rect()
            p.center = pos.midbottom
            p.y += 8
            temp.append([im,p])
        self.effects.append(temp)
        self.eCounter.append(0)

    def showEffects(self,screen):
        for i,e in enumerate(self.effects):
            screen.blit(e[0][0],e[0][1])
            self.eCounter[i] += 1
            if self.eCounter[i] > 0:
                del e[0]
                self.eCounter[i] = 0
                if e == []:
                    del self.effects[i]
                    del self.eCounter[i]

    ####################################################################################################################

    def upgradeRange(self):
        self.radius += 100# int(self.radius + (self.radius/self.rlevel))
        self.rlevel += 1
        if self.rlevel == 2:
            image = main.Images.platG
        else:
            image = main.Images.platJ
        pos = image.get_rect()
        pos.midbottom = self.pos.midbottom
        self.pos.y -= 10
        self.plats.append([image,pos])

    def upgradePow(self):
        self.damage = int(self.damage + self.damage/self.plevel)
        self.plevel+= 1

    ####################################################################################################################

    def place(self,screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused):
        location = False
        lc = pygame.image.load("Images\LocationCheck.png")
        LocSurface = pygame.Surface((1200,700))
        LocSurface.blit(lc,(0,0))

        for t in towers:
            if t.type == "Archer":  t.pos.x += 7
            pygame.draw.circle(LocSurface,Colours.red,t.pos.midbottom,t.pos.width)
            if t.type == "Archer": t.pos.x -= 7

        ################################################################################################################

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = -1
                        return
                if event.type == pygame.MOUSEBUTTONDOWN and location:
                    pygame.draw.circle(LocSurface,Colours.red,(x,y),self.pos.width)
                    return

                else:
                    screen.blit(bg, (0, 0))
                    screen.blit(waveLabel, (10, 10))
                    screen.blit(monLabel,monPos)
                    screen.blit(main.Images.coin, (950, 25))
                    if paused:
                        screen.blit(main.Images.playbtn,(1050,30))

                    ####################################################################################################

                    else:
                        screen.blit(main.Images.pausebtn, (1050, 30))

                    for i, t in enumerate(towers):
                        if t.rlevel > 1:
                            for p in t.plats:
                                screen.blit(p[0], p[1])
                        screen.blit(t.currentIm, t.pos)

                    for i, e in enumerate(enemies):
                        screen.blit(e.currentIm, e.pos)
                        if e.slowRate > 1:
                            spl = main.Images.splat.copy()
                            spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
                            splPos = main.Images.splat.get_rect()
                            splPos.topright = e.pos.topright
                            screen.blit(spl, splPos)
                        pygame.draw.rect(screen, main.Colours.grey, e.hBarOuter)
                        pygame.draw.rect(screen,main.Colours.red,e.hBarInnerR)
                        pygame.draw.rect(screen, main.Colours.green, e.hBarInnerG)

                    main.showHealth(playerHealth,screen,height=700)

                    ####################################################################################################

                    x, y = pygame.mouse.get_pos()
                    colour = LocSurface.get_at((x,y))

                    surface = pygame.Surface((1200,700),pygame.SRCALPHA)

                    self.pos.midbottom = (x,y)

                    if self.type == "Archer":   self.pos.x += 7
                    pygame.draw.circle(surface,Colours.tranluGrey,self.pos.center,self.radius)
                    screen.blit(surface,(0,0))
                    ElipseRect = (self.pos.left-self.pos.width/2,self.pos.bottom-self.pos.width/5,self.pos.width*2,self.pos.width/2)
                    if self.type =="Archer":    self.pos.x -= 7
                    if colour != Colours.red:
                        location = True
                        pygame.draw.ellipse(screen,Colours.green,ElipseRect)
                    else:
                        location = False
                        pygame.draw.ellipse(screen,Colours.red,ElipseRect)


                    screen.blit(self.currentIm,self.pos)
                    pygame.display.update()

########################################################################################################################


if __name__ == "__main__":
    main.initialise()