import pygame, enemy, tower, time, random, loadGame, saveGame

########################################################################################################################


class Images:
    bg = pygame.image.load("Images\Background.png")
    playbtn = pygame.image.load("Images\PlayBtn.png")
    pausebtn = pygame.image.load("Images\PauseBtn.png")
    coin = pygame.image.load("Images\Coin.png")
    ffwhite = pygame.image.load("Images\FastForwardWhite.png")
    ffblack = pygame.image.load("Images\FastForwardBlack.png")
    upgrdBtn = pygame.image.load("Images\\upgradeBtn.png")
    sellBtn = pygame.image.load("Images\sellBtn.png")
    incr = pygame.image.load("Images\Increase Range.png")
    incp = pygame.image.load("Images\Increase Power.png")
    heart = pygame.image.load("Images\Heart.png")
    platG = pygame.image.load("Images\platGround.png")
    platJ = pygame.image.load("Images\platJoin.png")
    splat = pygame.image.load("Images\HoneySplat.png")
    settings = pygame.image.load("Images\Settings.png")
    slct = pygame.image.load("Images\Xselect.png")
    slider = pygame.image.load("Images\slider.png")
    saveLoad = pygame.image.load("Images\saveLoad.png")
    slotSlct = pygame.image.load("Images\slotSlct.png")


########################################################################################################################


class Config:
    muted = False
    volume = 1.0
    sfx = False

########################################################################################################################


class Wave:
    def __init__(self):
        self.enemyTypes = ["Spider()","Slug()","Mosquito()"]

        self.wave1 = []
        for i in range(5):
            self.wave1.append(50)
            self.wave1.append(Spider())
        self.wave2 = []
        for i in range(10):
            self.wave2.append(40)
            self.wave2.append(Spider())
        self.wave3 = []
        for i in range(20):
            self.wave3.append(30)
            self.wave3.append(Spider())
        self.wave3.append(100)
        self.wave3.append(Slug())
        self.wave4 = []
        for i in range(20):
            self.wave4.append(20)
            self.wave4.append(Spider())
            self.wave4.append(20)
            self.wave4.append(Spider())
            self.wave4.append(40)
            self.wave4.append(Slug())
        self.wave5 = []
        for i in range(20):
            for x in range(10):
                self.wave5.append(20)
                self.wave5.append(Slug())
            self.wave5.append(40)
            for x in range(9):
                self.wave5.append(Spider())
                self.wave5.append(20)
            self.wave5.append(Spider())

        self.wave6 = []
        self.wave6.append(50)
        for i in range(5):
            self.wave6.append(Mosquito())
            self.wave6.append(5)
        self.wave6.append(Mosquito())
        self.wave6.append(40)
        self.wave6.append(Spider())
        for i in range(30):
            for x in range(4):
                self.wave6.append(20)
                self.wave6.append(Spider())
            for x in range(6):
                self.wave6.append(20)
                self.wave6.append(Slug())
                self.wave6.append(20)
                self.wave6.append(Spider())
            for x in range(6):
                self.wave6.append(5)
                self.wave6.append(Mosquito())

        self.current = self.wave1
        self.index = 1

    ####################################################################################################################

    def Break(self):
        self.index += 1
        try:
            self.current = self.__getattribute__("wave"+str(self.index))
        except AttributeError:
            self.current = []
            for i in range(self.index*20):
                self.current.append(random.randint(10,50))
                i = random.randint(0,len(self.enemyTypes)-1)
                e = eval(self.enemyTypes[i])
                self.current.append(e)

########################################################################################################################


class Colours:
    white = (255,255,255)
    black = (0,0,0)
    grey = (160,160,160)
    green = (30, 186, 13)
    tranluGreen = (30, 186, 13,180)
    tranluLGrey = (120,120,120,180)
    tranluGrey = (80,80,80,180)
    red = (156,72,49)
    transpa = (0,0,0,0)

########################################################################################################################


def initialise():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    music = pygame.mixer.Sound("Sounds\BGM.wav").play(-1)
    width = 1200
    height = 700
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Garden Defence")
    screen.blit(Images.bg,(0,0))
    pygame.display.update()
    wave = Wave()
    playerHealth = 5
    font = pygame.font.Font("digital-7.ttf",72)
    towers = []
    money = 5000
    cost = {"Archer":20,"Mortar":60,"Beehive":100}
    dfont = pygame.font.Font("digital-7.ttf",24)
    main(width,height,screen,wave,playerHealth,font,towers,money,cost,dfont,music)

########################################################################################################################


def showHealth(playerHealth,screen,height):
    for i in range(0,playerHealth):
        screen.blit(Images.heart,(i*32+10,height-40))

########################################################################################################################

def rename(slot,screen):
    slot -= 1
    names = []
    file = open("Data\\names.txt","r")
    for i in range(3):
        names.append(file.readline())
        names[i] = names[i][:len(names[i])-1]
    file.close()

    font = pygame.font.Font("digital-7.ttf",30)
    labels = []
    for name in names:
        labels.append(font.render(name,1,Colours.white))

    names[slot] = ""
    condition = True

    while condition:
        screen.blit(Images.saveLoad,(100,250),(100,250,200,225))
        screen.blit(labels[0], (120, 285))
        screen.blit(labels[1], (120, 360))
        screen.blit(labels[2], (120, 435))
        if slot == 0:
            screen.blit(Images.slotSlct, (96, 266))
        elif slot == 1:
            screen.blit(Images.slotSlct, (96, 342))
        elif slot == 2:
            screen.blit(Images.slotSlct, (96, 417))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                condition = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    names[slot] = names[slot][:len(names[slot])-1]
                    labels[slot] = font.render(names[slot],1,Colours.white)
                elif event.key == pygame.K_RETURN:
                    names[slot] += "\n"
                    file = open("Data\\names.txt","w")
                    for i in range(0,3):
                        names[i] += "\n"
                        file.write(names[i])
                    file.close()
                    condition = False
                elif len(names[slot]) < 10:
                    names[slot] += chr(event.key)
                    labels[slot] = font.render(names[slot],1,Colours.white)
    return labels


def Settings(screen,music,money,towers,playerHealth,waveIndex):

    names = []

    file = open("Data\\names.txt", "r")
    for i in range(3):
        names.append(file.readline())
        names[i] = names[i][:len(names[i])-1]
    file.close()

    font = pygame.font.Font("digital-7.ttf", 30)
    labels = []
    for name in names:
        labels.append(font.render(name, 1, Colours.white))

    bfont = pygame.font.Font("digital-7.ttf",48)
    sfont = pygame.font.Font("digital-7.ttf",30)
    slabel1 = bfont.render("save game",1,Colours.white)
    slabel2 = sfont.render("save",1,Colours.white)
    llabel1 = bfont.render("load game",1,Colours.white)
    llabel2 = sfont.render("load",1,Colours.white)

    slider = False
    sav = False
    loa = False
    selected = 1

    while True:
        if sav:
            screen.blit(Images.saveLoad,(0,0))
            screen.blit(slabel1,(95,200))
            screen.blit(slabel2,(160,503))
        elif loa:
            screen.blit(Images.saveLoad,(0,0))
            screen.blit(llabel1,(95,200))
            screen.blit(llabel2,(160,503))
        else:
            screen.blit(Images.settings,(0,0))

        if sav or loa:
            screen.blit(labels[0],(120,285))
            screen.blit(labels[1],(120,360))
            screen.blit(labels[2],(120,435))
            if selected == 1:
                screen.blit(Images.slotSlct,(96,266))
            elif selected == 2:
                screen.blit(Images.slotSlct,(96,342))
            elif selected == 3:
                screen.blit(Images.slotSlct,(96,417))

        if Config.muted:
            screen.blit(Images.slct,(766,281))
        if Config.sfx:
            screen.blit(Images.slct,(766,325))
        screen.blit(Images.slider,(Config.volume*200+585,238))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                if x > 810 and y > 63 and x < 862 and y < 112:
                    return

                elif x > 765 and x < 802 and y > 280 and y < 318:
                    if Config.muted:
                        music.unpause()
                        Config.muted = False
                    else:
                        music.pause()
                        Config.muted = True

                elif x > 765 and x < 802 and y > 325 and y < 363:
                    if Config.sfx:
                        Config.sfx = False
                    else:
                        Config.sfx = True

                elif x > 600 and x < 800 and y > 245 and y < 260:
                    slider = True

                elif x > 450 and x < 600 and y > 475 and y < 550:
                    sav = True
                    loa = False

                elif x > 650 and x < 800 and y > 475 and y < 550:
                    loa = True
                    sav = False

                elif x > 96 and x < 274 and y > 266 and y < 326:
                    selected = 1
                    if event.button == 3:
                        labels = rename(selected,screen)
                elif x > 96 and x < 274 and y > 342 and y < 402:
                    selected = 2
                    if event.button == 3:
                        labels = rename(selected,screen)
                elif x > 96 and x < 274 and y > 417 and y < 477:
                    selected = 3
                    if event.button == 3:
                        labels = rename(selected,screen)

                elif loa and x > 120 and x < 253 and y > 492 and y < 538:
                    pygame.mixer.stop()
                    loadGame.load(selected)

                elif sav and x > 120 and x < 253 and y > 492 and y < 538:
                    saveGame.save(towers,waveIndex,money,playerHealth,selected)



                # elif x > 260 and x < 295 and y > 170 and y < 200:
                #     loa = False
                #     sav = False
                #     print (loa,sav)


            elif event.type == pygame.MOUSEBUTTONUP:
                slider = False

        if slider:
            x,_ = pygame.mouse.get_pos()
            if x > 600 and x < 800:
                Config.volume = (x - 600) / 200
            elif x < 600:
                Config.volume = 0
            elif x > 800:
                Config.volume = 1
            music.set_volume(Config.volume)





########################################################################################################################


def pause(towers,screen,bg,enemies,playerHealth,waveLabel,money,cost,dfont,height,music,waveIndex):
    font = pygame.font.Font("digital-7.ttf",72)
    surface = pygame.Surface((1200,700),pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            ############################################################################################################


            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x > 1067 and x < 1128 and y > 50 and y < 110:
                    return towers,money
                elif x > 10 and x < 65 and y > 80 and y < 130:
                    Settings(screen,music,money,towers,playerHealth,waveIndex)
                elif x> 1025 and y > 150 and x < 1175 and y < 300:
                    if money - cost["Archer"] >= 0:
                        money -= cost["Archer"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newArcher(screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused=True))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]
                        screen.blit(bg, (0, 0))
                        for t in towers:
                            if t.rlevel > 1:
                                for p in t.plats:
                                    screen.blit(p[0], p[1])
                            screen.blit(t.currentIm, t.pos)
                        for e in enemies:
                            screen.blit(e.currentIm, e.pos)
                            if e.slowRate > 1:
                                spl = Images.splat.copy()
                                spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
                                splPos = Images.splat.get_rect()
                                splPos.topright = e.pos.topright
                                screen.blit(spl, splPos)
                            pygame.draw.rect(screen, Colours.grey, e.hBarOuter)
                            pygame.draw.rect(screen, Colours.red, e.hBarInnerR)
                            pygame.draw.rect(screen, Colours.green, e.hBarInnerG)
                        screen.blit(waveLabel, (10, 10))
                        screen.blit(monLabel, monPos)
                        screen.blit(Images.coin, (950, 25))
                        screen.blit(Images.playbtn, (1050, 30))
                        screen.blit(Images.ffwhite, (1140, 100))
                        showHealth(playerHealth, screen, height=700)
                        pygame.display.update()

                elif x > 1025 and y > 325 and x < 1175 and y < 475:
                    if money - cost["Mortar"] >= 0:
                        money -= cost["Mortar"]
                        monLabel = font.render(str(money), 1, Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940, 10)
                        towers.append(
                            newMortar(screen, Images.bg, enemies, towers, playerHealth, waveLabel, monLabel,
                                      monPos))
                        if towers[len(towers) - 1].state == -1:
                            money += cost[towers[len(towers) - 1].type]
                            del towers[len(towers) - 1]
                        screen.blit(bg,(0,0))
                        for t in towers:
                            if t.rlevel > 1:
                                for p in t.plats:
                                    screen.blit(p[0], p[1])
                            screen.blit(t.currentIm,t.pos)
                        for e in enemies:
                            screen.blit(e.currentIm,e.pos)
                            if e.slowRate > 1:
                                spl = Images.splat.copy()
                                spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
                                splPos = Images.splat.get_rect()
                                splPos.topright = e.pos.topright
                                screen.blit(spl, splPos)
                            pygame.draw.rect(screen,Colours.grey,e.hBarOuter)
                            pygame.draw.rect(screen,Colours.red,e.hBarInnerR)
                            pygame.draw.rect(screen,Colours.green,e.hBarInnerG)
                        screen.blit(waveLabel,(10,10))
                        screen.blit(monLabel,monPos)
                        screen.blit(Images.coin,(950,25))
                        screen.blit(Images.playbtn,(1050,30))
                        screen.blit(Images.ffwhite,(1140,100))
                        showHealth(playerHealth,screen,height=700)
                        pygame.display.update()

                elif x> 1025 and y > 500 and x < 1175 and y < 650:
                    if money - cost["Beehive"] >= 0:
                        money -= cost["Beehive"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newBeehive(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]

                            screen.blit(bg, (0, 0))
                            for t in towers:
                                if t.rlevel > 1:
                                    for p in t.plats:
                                        screen.blit(p[0], p[1])
                                screen.blit(t.currentIm, t.pos)
                            for e in enemies:
                                screen.blit(e.currentIm, e.pos)
                                if e.slowRate > 1:
                                    spl = Images.splat.copy()
                                    spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
                                    splPos = Images.splat.get_rect()
                                    splPos.topright = e.pos.topright
                                    screen.blit(spl, splPos)
                                pygame.draw.rect(screen, Colours.grey, e.hBarOuter)
                                pygame.draw.rect(screen, Colours.red, e.hBarInnerR)
                                pygame.draw.rect(screen, Colours.green, e.hBarInnerG)
                            screen.blit(waveLabel, (10, 10))
                            screen.blit(monLabel, monPos)
                            screen.blit(Images.coin, (950, 25))
                            screen.blit(Images.playbtn, (1050, 30))
                            screen.blit(Images.ffwhite, (1140, 100))
                            showHealth(playerHealth, screen, height=700)
                            pygame.display.update()

                ########################################################################################################

                else:
                    for i,t in enumerate(towers):
                        if t.showBtns:
                            if t.type == "Archer": t.pos.centerx += 3
                            if x > t.pos.centerx-22 and x < t.pos.centerx+2 and y > t.pos.y-25 and y < t.pos.y-1:
                                money += int(cost[t.type]*(t.rlevel+t.plevel) / 4)
                                del towers[i]
                            elif x > t.pos.centerx+2 and x < t.pos.centerx+26 and y > t.pos.y-25 and y < t.pos.y-1:
                                t.showUps = True
                            elif t.showUps:
                                if x > t.pos.centerx -9 and x < t.pos.centerx + 13 and y > t.pos.y-50 and y < t.pos.y-26:
                                    if money >= int((cost[t.type]/2)*t.rlevel):
                                        money -= int((cost[t.type]/2)*t.rlevel)
                                        t.upgradeRange()
                                if x > t.pos.centerx+13 and x < t.pos.centerx + 35 and y > t.pos.y-50 and y < t.pos.y-26:
                                    if money >= int((cost[t.type]/2)*t.plevel):
                                        money -= int((cost[t.type]/2)*t.plevel)
                                        t.upgradePow()
                            if t.type == "Archer": t.pos.centerx -= 3
                        if (x > t.pos.left and x < t.pos.right and y > t.pos.top and y < t.pos.bottom) or (x > t.pos.centerx+2 and x < t.pos.centerx+26 and y > t.pos.y-25 and y < t.pos.y-1):
                            t.showBtns = True
                        else:
                            t.showBtns = False
                            t.showUps = False

        ################################################################################################################

        screen.blit(Images.bg,(0,0))
        screen.blit(Images.playbtn,(1050,30))
        screen.blit(Images.ffwhite,(1140,100))

        ################################################################################################################

        for i,e in enumerate(enemies):
            screen.blit(e.currentIm,e.pos)
            if e.slowRate > 1:
                spl = Images.splat.copy()
                spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
                splPos = Images.splat.get_rect()
                splPos.topright = e.pos.topright
                screen.blit(spl, splPos)
            pygame.draw.rect(screen,Colours.grey,e.hBarOuter)
            pygame.draw.rect(screen,Colours.red,e.hBarInnerR)
            pygame.draw.rect(screen,Colours.green,e.hBarInnerG)

        for i,t in enumerate(towers):
            if t.rlevel > 1:
                for p in t.plats:
                    screen.blit(p[0],p[1])
            screen.blit(t.currentIm,t.pos)

        for i,t in enumerate(towers):
            if t.showBtns:
                if t.type == "Archer":
                    if t.xdir == 1:
                        t.pos.centerx += 3
                    else:
                        t.pos.centerx -= 6
                surface.fill(Colours.transpa)
                pygame.draw.circle(surface,Colours.tranluLGrey,t.pos.center,t.radius)
                screen.blit(surface,(0,0))
                screen.blit(Images.sellBtn,(t.pos.centerx-22,t.pos.y-25))
                screen.blit(Images.upgrdBtn,(t.pos.centerx+2,t.pos.y-25))

                ########################################################################################################

                if t.showUps:
                    screen.blit(Images.incr,(t.pos.centerx-9,t.pos.y-50))
                    screen.blit(Images.incp,(t.pos.centerx+13,t.pos.y-50))
                    x,y = pygame.mouse.get_pos()

                    if money - int((cost[t.type] / 2) * t.rlevel) < 0:
                        surface.fill(Colours.transpa)
                        pygame.draw.rect(surface,Colours.tranluGrey,(t.pos.centerx-7,t.pos.y-48,20,20))
                        screen.blit(surface,(0,0))
                        surface.fill(Colours.transpa)
                    elif x > t.pos.centerx - 9 and x < t.pos.centerx + 12 and y > t.pos.y - 50 and y < t.pos.y - 26:
                        surface.fill(Colours.transpa)
                        pygame.draw.circle(surface, Colours.tranluGreen, t.pos.center, int(t.radius + 100))#(t.radius/t.rlevel)))
                        pygame.draw.circle(surface, Colours.tranluLGrey, t.pos.center, t.radius)
                        screen.blit(surface, (0, 0))
                        mlabel = dfont.render(str(int((cost[t.type] / 2) * t.rlevel)),1,Colours.white)
                        mpos = mlabel.get_rect()
                        mpos.bottomright = (t.pos.centerx+13,t.pos.y-51)
                        screen.blit(mlabel,mpos)
                        coin = pygame.transform.scale(Images.coin,(16,14))
                        cpos = coin.get_rect()
                        cpos.centery = mpos.centery + 2
                        cpos.left = mpos.right + 5
                        screen.blit(coin,cpos)

                    if money - int((cost[t.type] / 2) * t.plevel) < 0:
                        surface.fill(Colours.transpa)
                        pygame.draw.rect(surface, Colours.tranluGrey, (t.pos.centerx +15, t.pos.y - 48, 20, 20))
                        screen.blit(surface, (0, 0))
                        surface.fill(Colours.transpa)
                    elif x > t.pos.centerx + 13 and x < t.pos.centerx + 35 and y > t.pos.y - 50 and y < t.pos.y - 26:
                        if t.type == "Beehive":
                            Dlabel1 = dfont.render("Slow Down = " + str(t.damage), 1, Colours.black)
                        else:
                            Dlabel1 = dfont.render("Damage = "+str(t.damage),1,Colours.black)
                        Dpos1 = Dlabel1.get_rect().move(t.pos.centerx+38,t.pos.y-50)
                        Dlabel2 = dfont.render("+"+str(int(t.damage/t.plevel)),1,Colours.red)
                        Dpos2 = Dlabel2.get_rect().move(0,t.pos.y-50)
                        Dpos2.left = Dpos1.right + 5
                        screen.blit(Dlabel1,(Dpos1))
                        screen.blit(Dlabel2,(Dpos2))
                        mlabel = dfont.render(str(int((cost[t.type] / 2) * t.plevel)),1,Colours.white)
                        mpos = mlabel.get_rect()
                        mpos.bottomright = (t.pos.centerx+13,t.pos.y-51)
                        screen.blit(mlabel,mpos)
                        coin = pygame.transform.scale(Images.coin,(16,14))
                        cpos = coin.get_rect()
                        cpos.centery = mpos.centery + 2
                        cpos.left = mpos.right + 5
                        screen.blit(coin,cpos)

                if t.type == "Archer":
                    if t.xdir == 1:
                        t.pos.centerx -= 3
                    else:
                        t.pos.centerx += 6
                if t.rlevel > 1:
                    for p in t.plats:
                        screen.blit(p[0],p[1])
                screen.blit(t.currentIm,t.pos)

            ############################################################################################################

        surface = pygame.Surface((1200,700),pygame.SRCALPHA)
        if cost["Archer"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 155, 138, 138))
        if cost["Mortar"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 328, 138, 138))
        if cost["Beehive"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 501, 138, 138))
        screen.blit(surface, (0, 0))
        showHealth(playerHealth,screen,height)
        screen.blit(waveLabel,(10,10))
        monLabel = font.render(str(money), 1, Colours.black)
        monPos = monLabel.get_rect()
        monPos.topright = (940,10)
        screen.blit(monLabel, monPos)
        screen.blit(Images.coin,(950,25))
        pygame.display.update()

########################################################################################################################

def gameover(screen,height,width,towers,enemies,currentWave):
    for t in towers:
        if t.rlevel > 1:
            for p in t.plats:
                screen.blit(p[0], p[1])
        screen.blit(t.currentIm,t.pos)
    for e in enemies:
        screen.blit(e.currentIm,e.pos)
        if e.slowRate > 1:
            spl = Images.splat.copy()
            spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
            splPos = Images.splat.get_rect()
            splPos.topright = e.pos.topright
            screen.blit(spl, splPos)

    font1 = pygame.font.Font("digital-7.ttf",120)
    font2 = pygame.font.Font("digital-7.ttf",80)

    label = font1.render("GAMEOVER",1,Colours.black)
    labelPos = label.get_rect()
    labelPos.center = ((width-200)/2,height/2)
    screen.blit(label,labelPos)

    label = font2.render("WAVE: %s" %currentWave,1,Colours.black)
    labelPos = label.get_rect()
    labelPos.midtop = ((width-200)/2,height/2+80)
    screen.blit(label,labelPos)

    highscore = open("Data\highscore.txt","r").readline()

    if currentWave > int(highscore):
        label = font2.render("NEW HIGHSCORE!",1,Colours.black)
        h = open("Data\highscore.txt","w")
        h.write(str(currentWave))
        h.close()
    else:
        label = font2.render("HIGHSCORE: %s" % highscore,1,Colours.black)
    labelPos = label.get_rect()
    labelPos.midtop = ((width-200)/2,height/2+160)
    screen.blit(label,labelPos)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                initialise()

########################################################################################################################


def Spider():
    spider = enemy.Enemy("Spider",4)
    return spider


def Slug():
    slug = enemy.Enemy("Slug",4)
    return slug


def Mosquito():
    mosq = enemy.Enemy("Mosquito",4)
    return mosq

########################################################################################################################


def newArcher(screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused=False,loading=False,pos=None):
    archer = tower.Tower("Archer",4,screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused,loading,pos)
    return archer

def newMortar(screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused=False,loading=False,pos=None):
    mortar = tower.Tower("Mortar",10,screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused,loading,pos)
    return mortar

def newBeehive(screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused=False,loading=False,pos=None):
    bee = tower.Tower("Beehive",8,screen,bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused,loading,pos)
    return bee

########################################################################################################################


def main(width,height,screen,wave,playerHealth,font,towers, money, cost,dfont,music):
    enemies = []
    count = 0
    speed = "Normal"
    surface = pygame.Surface((1200,700),pygame.SRCALPHA)
    waveLabel = font.render("WAVE "+str(wave.index),1,Colours.black)

    ####################################################################################################################

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            ############################################################################################################

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x > 1072 and x < 1128 and y > 50 and y < 110:
                    pos = Images.playbtn.get_rect().move(1050,30)
                    screen.blit(Images.bg,pos,pos)
                    screen.blit(Images.playbtn,(1050,30))
                    screen.blit(Images.ffwhite,(1140,100))
                    pygame.display.update()
                    towers,money = pause(towers,screen,Images.bg,enemies,playerHealth,waveLabel,money,cost,dfont,height,music,wave.index)
                    screen.blit(Images.bg, pos,pos)
                    screen.blit(Images.pausebtn, (1050, 30))
                    pygame.display.update()
                elif x > 10 and x < 65 and y > 80 and y < 130:
                    Settings(screen,music,money,towers,playerHealth,wave.index)
                elif x> 1025 and y > 150 and x < 1175 and y < 300:
                    if money - cost["Archer"] >= 0:
                        money -= cost["Archer"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newArcher(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]
                elif x> 1025 and y > 325 and x < 1175 and y < 475:
                    if money - cost["Mortar"] >= 0:
                        money -= cost["Mortar"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newMortar(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]
                elif x> 1025 and y > 500 and x < 1175 and y < 650:
                    if money - cost["Beehive"] >= 0:
                        money -= cost["Beehive"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newBeehive(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]
                elif x > 1140 and y > 105 and x < 1170 and y < 125:
                    speed = "Fast"

                ########################################################################################################

                else:

                    for i,t in enumerate(towers):
                        if t.showBtns:
                            if t.type == "Archer": t.pos.centerx += 3
                            if x > t.pos.centerx-22 and x < t.pos.centerx+2 and y > t.pos.y-25 and y < t.pos.y-1:
                                money += int(cost[t.type]*(t.rlevel+t.plevel) / 4)
                                del towers[i]
                            elif x > t.pos.centerx+2 and x < t.pos.centerx+26 and y > t.pos.y-25 and y < t.pos.y-1:
                                t.showUps = True

                            ############################################################################################

                            elif t.showUps:
                                if x > t.pos.centerx -9 and x < t.pos.centerx + 13 and y > t.pos.y-50 and y < t.pos.y-26:
                                    if money >= int((cost[t.type]/2)*t.rlevel):
                                        money -= int((cost[t.type]/2)*t.rlevel)
                                        t.upgradeRange()
                                if x > t.pos.centerx+13 and x < t.pos.centerx + 35 and y > t.pos.y-50 and y < t.pos.y-26:
                                    if money >= int((cost[t.type]/2)*t.plevel):
                                        money -= int((cost[t.type]/2)*t.plevel)
                                        t.upgradePow()

                            ############################################################################################

                            if t.type == "Archer": t.pos.centerx -= 3
                        if (x > t.pos.left and x < t.pos.right and y > t.pos.top and y < t.pos.bottom) or (x > t.pos.centerx+2 and x < t.pos.centerx+26 and y > t.pos.y-25 and y < t.pos.y-1):
                            t.showBtns = True
                        else:
                            t.showBtns = False
                            t.showUps = False

            ############################################################################################################

            if event.type == pygame.MOUSEBUTTONUP:
                # x,y = pygame.mouse.get_pos()
                # if x > 1140 and y > 105 and x < 1170 and y < 125:
                if speed == "Fast":
                    speed = "Normal"

        ################################################################################################################

        screen.blit(Images.bg,(0,0))
        screen.blit(Images.pausebtn,(1050,30))
        if speed == "Normal":
            screen.blit(Images.ffwhite,(1140,100))
        else:
            screen.blit(Images.ffblack,(1140,100))

        ################################################################################################################

        for i,e in enumerate(enemies):
            if e.health <= 0:
                money += e.value
                del enemies[i]
            else:
                screen.blit(e.currentIm,e.pos)
                if e.slowRate > 1:
                    spl = Images.splat.copy()
                    spl.fill((255, 255, 255, int(e.slowCount)), None, pygame.BLEND_RGBA_MULT)
                    splPos = Images.splat.get_rect()
                    splPos.topright = e.pos.topright
                    screen.blit(spl, splPos)
                pygame.draw.rect(screen,Colours.grey,e.hBarOuter)
                pygame.draw.rect(screen,Colours.red,e.hBarInnerR)
                pygame.draw.rect(screen,Colours.green,e.hBarInnerG)

                try:
                    e.move()
                except IndexError:
                    e.alive = False
                    del enemies[i]
                    playerHealth -= 1
                    if playerHealth == 0: gameover(screen,height,width,towers,enemies,wave.index)
                if e.pos.right < -5 and e.pathPos > 1:
                    e.alive = False
                    del enemies[i]
                    playerHealth -= 1
                    if playerHealth == 0: gameover(screen, height, width, towers, enemies,wave.index)


        ################################################################################################################

        for i,t in enumerate(towers):
            if t.rlevel > 1:
                for p in t.plats:
                    screen.blit(p[0],p[1])
            screen.blit(t.currentIm,t.pos)

        for i,t in enumerate(towers):
            t.isEnemy(enemies)
            if t.showBtns:
                if t.type == "Archer":
                    if t.xdir == 1:
                        t.pos.centerx += 3
                    else:
                        t.pos.centerx -= 6
                surface.fill(Colours.transpa)
                pygame.draw.circle(surface,Colours.tranluLGrey,t.pos.center,t.radius)
                screen.blit(surface,(0,0))
                screen.blit(Images.sellBtn,(t.pos.centerx-22,t.pos.y-25))
                screen.blit(Images.upgrdBtn,(t.pos.centerx+2,t.pos.y-25))

                ########################################################################################################

                if t.showUps:
                    screen.blit(Images.incr,(t.pos.centerx-9,t.pos.y-50))
                    screen.blit(Images.incp,(t.pos.centerx+13,t.pos.y-50))
                    x,y = pygame.mouse.get_pos()

                    if money - int((cost[t.type] / 2) * t.rlevel) < 0:
                        surface.fill(Colours.transpa)
                        pygame.draw.rect(surface,Colours.tranluGrey,(t.pos.centerx-7,t.pos.y-48,20,20))
                        screen.blit(surface,(0,0))
                        surface.fill(Colours.transpa)
                    elif x > t.pos.centerx - 9 and x < t.pos.centerx + 12 and y > t.pos.y - 50 and y < t.pos.y - 26:
                        surface.fill(Colours.transpa)
                        pygame.draw.circle(surface, Colours.tranluGreen, t.pos.center, int(t.radius + 100))#(t.radius/t.rlevel)))
                        pygame.draw.circle(surface, Colours.tranluLGrey, t.pos.center, t.radius)
                        screen.blit(surface, (0, 0))
                        mlabel = dfont.render(str(int((cost[t.type] / 2) * t.rlevel)),1,Colours.white)
                        mpos = mlabel.get_rect()
                        mpos.bottomright = (t.pos.centerx+13,t.pos.y-51)
                        screen.blit(mlabel,mpos)
                        coin = pygame.transform.scale(Images.coin,(16,14))
                        cpos = coin.get_rect()
                        cpos.centery = mpos.centery + 2
                        cpos.left = mpos.right + 5
                        screen.blit(coin,cpos)

                    if money - int((cost[t.type] / 2) * t.plevel) < 0:
                        surface.fill(Colours.transpa)
                        pygame.draw.rect(surface, Colours.tranluGrey, (t.pos.centerx +15, t.pos.y - 48, 20, 20))
                        screen.blit(surface, (0, 0))
                        surface.fill(Colours.transpa)
                    elif x > t.pos.centerx + 13 and x < t.pos.centerx + 35 and y > t.pos.y - 50 and y < t.pos.y - 26:
                        if t.type == "Beehive":
                            Dlabel1 = dfont.render("Slow Down = " + str(t.damage), 1, Colours.black)
                        else:
                            Dlabel1 = dfont.render("Damage = "+str(t.damage),1,Colours.black)
                        Dpos1 = Dlabel1.get_rect().move(t.pos.centerx+38,t.pos.y-50)
                        Dlabel2 = dfont.render("+"+str(int(t.damage/t.plevel)),1,Colours.red)
                        Dpos2 = Dlabel2.get_rect().move(0,t.pos.y-50)
                        Dpos2.left = Dpos1.right + 5
                        screen.blit(Dlabel1,(Dpos1))
                        screen.blit(Dlabel2,(Dpos2))
                        mlabel = dfont.render(str(int((cost[t.type] / 2) * t.plevel)),1,Colours.white)
                        mpos = mlabel.get_rect()
                        mpos.bottomright = (t.pos.centerx+13,t.pos.y-51)
                        screen.blit(mlabel,mpos)
                        coin = pygame.transform.scale(Images.coin,(16,14))
                        cpos = coin.get_rect()
                        cpos.centery = mpos.centery + 2
                        cpos.left = mpos.right + 5
                        screen.blit(coin,cpos)

                    ####################################################################################################

                if t.type == "Archer":
                    if t.xdir == 1:
                        t.pos.centerx -= 3
                    else:
                        t.pos.centerx += 6
                if t.rlevel > 1:
                    for p in t.plats:
                        screen.blit(p[0],p[1])
                screen.blit(t.currentIm,t.pos)
            for p in t.proj:
                p.move(enemies)
                screen.blit(p.currentIm,p.pos)
            t.showEffects(screen)

        ################################################################################################################

        surface = pygame.Surface((1200,700),pygame.SRCALPHA)
        if cost["Archer"] > money:
            pygame.draw.rect(surface,Colours.tranluGrey,(1031,155,138,138))
        if cost["Mortar"] > money:
            pygame.draw.rect(surface,Colours.tranluGrey,(1031,328,138,138))
        if cost["Beehive"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 501, 138, 138))
        screen.blit(surface,(0,0))
        showHealth(playerHealth,screen,height)
        screen.blit(waveLabel,(10,10))
        monLabel = font.render(str(money), 1, Colours.black)
        monPos = monLabel.get_rect()
        monPos.topright = (940,10)
        screen.blit(monLabel, monPos)
        screen.blit(Images.coin,(950,25))
        pygame.display.update()
        if speed == "Normal":
            time.sleep(0.02)

        ################################################################################################################

        if len(wave.current) > 0:
            count += 1
            delay = wave.current[0]
            if count > delay:
                count = 0
                enemies.append(wave.current[1])
                del wave.current[0]
                del wave.current[0]
        elif len(enemies) == 0:
            wave.Break()
            break

    ####################################################################################################################

    while True:

        screen.blit(Images.bg, (0, 0))
        screen.blit(Images.playbtn, (1050, 30))

        ################################################################################################################

        for i,t in enumerate(towers):
            if t.rlevel > 1:
                for p in t.plats:
                    screen.blit(p[0],p[1])
            screen.blit(t.currentIm,t.pos)

        for i, t in enumerate(towers):
            if t.showBtns:
                if t.type == "Archer":
                    if t.xdir == 1:
                        t.pos.centerx += 3
                    else:
                        t.pos.centerx -= 6
                surface.fill(Colours.transpa)
                pygame.draw.circle(surface,Colours.tranluLGrey,t.pos.center,t.radius)
                screen.blit(surface,(0,0))
                screen.blit(Images.sellBtn,(t.pos.centerx-22,t.pos.y-25))
                screen.blit(Images.upgrdBtn,(t.pos.centerx+2,t.pos.y-25))

                ########################################################################################################

                if t.showUps:
                    screen.blit(Images.incr,(t.pos.centerx-9,t.pos.y-50))
                    screen.blit(Images.incp,(t.pos.centerx+13,t.pos.y-50))
                    x,y = pygame.mouse.get_pos()

                    if money - int((cost[t.type] / 2) * t.rlevel) < 0:
                        surface.fill(Colours.transpa)
                        pygame.draw.rect(surface,Colours.tranluGrey,(t.pos.centerx-7,t.pos.y-48,20,20))
                        screen.blit(surface,(0,0))
                        surface.fill(Colours.transpa)
                    elif x > t.pos.centerx - 9 and x < t.pos.centerx + 12 and y > t.pos.y - 50 and y < t.pos.y - 26:
                        surface.fill(Colours.transpa)
                        pygame.draw.circle(surface, Colours.tranluGreen, t.pos.center, int(t.radius + 100))##(t.radius/t.rlevel)))
                        pygame.draw.circle(surface, Colours.tranluLGrey, t.pos.center, t.radius)
                        screen.blit(surface, (0, 0))
                        mlabel = dfont.render(str(int((cost[t.type] / 2) * t.rlevel)),1,Colours.white)
                        mpos = mlabel.get_rect()
                        mpos.bottomright = (t.pos.centerx+13,t.pos.y-51)
                        screen.blit(mlabel,mpos)
                        coin = pygame.transform.scale(Images.coin,(16,14))
                        cpos = coin.get_rect()
                        cpos.centery = mpos.centery + 2
                        cpos.left = mpos.right + 5
                        screen.blit(coin,cpos)

                    if money - int((cost[t.type] / 2) * t.plevel) < 0:
                        surface.fill(Colours.transpa)
                        pygame.draw.rect(surface, Colours.tranluGrey, (t.pos.centerx +15, t.pos.y - 48, 20, 20))
                        screen.blit(surface, (0, 0))
                        surface.fill(Colours.transpa)
                    elif x > t.pos.centerx + 13 and x < t.pos.centerx + 35 and y > t.pos.y - 50 and y < t.pos.y - 26:
                        if t.type == "Beehive":
                            Dlabel1 = dfont.render("Slow Down = " + str(t.damage), 1, Colours.black)
                        else:
                            Dlabel1 = dfont.render("Damage = "+str(t.damage),1,Colours.black)
                        Dpos1 = Dlabel1.get_rect().move(t.pos.centerx+38,t.pos.y-50)
                        Dlabel2 = dfont.render("+"+str(int(t.damage/t.plevel)),1,Colours.red)
                        Dpos2 = Dlabel2.get_rect().move(0,t.pos.y-50)
                        Dpos2.left = Dpos1.right + 5
                        screen.blit(Dlabel1,(Dpos1))
                        screen.blit(Dlabel2,(Dpos2))
                        mlabel = dfont.render(str(int((cost[t.type] / 2) * t.plevel)),1,Colours.white)
                        mpos = mlabel.get_rect()
                        mpos.bottomright = (t.pos.centerx+13,t.pos.y-51)
                        screen.blit(mlabel,mpos)
                        coin = pygame.transform.scale(Images.coin,(16,14))
                        cpos = coin.get_rect()
                        cpos.centery = mpos.centery + 2
                        cpos.left = mpos.right + 5
                        screen.blit(coin,cpos)

                    ####################################################################################################

                if t.type == "Archer":
                    if t.xdir == 1:
                        t.pos.centerx -= 3
                    else:
                        t.pos.centerx += 6
                if t.rlevel > 1:
                    for p in t.plats:
                        screen.blit(p[0],p[1])
                screen.blit(t.currentIm, t.pos)
                t.showEffects(screen)

        ################################################################################################################

        surface = pygame.Surface((1200, 700), pygame.SRCALPHA)
        if cost["Archer"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 155, 138, 138))
        if cost["Mortar"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 328, 138, 138))
        if cost["Beehive"] > money:
            pygame.draw.rect(surface, Colours.tranluGrey, (1031, 501, 138, 138))
        screen.blit(surface, (0, 0))

        showHealth(playerHealth, screen, height)
        screen.blit(waveLabel, (10, 10))
        monLabel = font.render(str(money), 1, Colours.black)
        monPos = monLabel.get_rect()
        monPos.topright = (940, 10)
        screen.blit(monLabel, monPos)
        screen.blit(Images.coin, (950, 25))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x > 1072 and x < 1128 and y > 50 and y < 110:
                    main(width,height,screen,wave,playerHealth,font,towers,money,cost,dfont,music)
                elif x > 10 and x < 65 and y > 80 and y < 130:
                    Settings(screen,music,money,towers,playerHealth,wave.index)
                if x> 1025 and y > 150 and x < 1175 and y < 300:
                    if money - cost["Archer"] >= 0:
                        money -= cost["Archer"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newArcher(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos,paused=True))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]
                elif x> 1025 and y > 325 and x < 1175 and y < 475:
                    if money - cost["Mortar"] >= 0:
                        money -= cost["Mortar"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newMortar(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]
                elif x> 1025 and y > 500 and x < 1175 and y < 650:
                    if money - cost["Beehive"] >= 0:
                        money -= cost["Beehive"]
                        monLabel = font.render(str(money),1,Colours.black)
                        monPos = monLabel.get_rect()
                        monPos.topright = (940,10)
                        towers.append(newBeehive(screen,Images.bg,enemies,towers,playerHealth,waveLabel,monLabel,monPos))
                        if towers[len(towers)-1].state == -1:
                            money += cost[towers[len(towers)-1].type]
                            del towers[len(towers)-1]

                ########################################################################################################

                else:
                    for i, t in enumerate(towers):
                        if t.showBtns:
                            if t.type == "Archer": t.pos.centerx += 3
                            if x > t.pos.centerx - 22 and x < t.pos.centerx + 2 and y > t.pos.y - 25 and y < t.pos.y - 1:
                                money += int(cost[t.type] * (t.rlevel + t.plevel) / 4)
                                del towers[i]
                            elif x > t.pos.centerx + 2 and x < t.pos.centerx + 26 and y > t.pos.y - 25 and y < t.pos.y - 1:
                                t.showUps = True

                            ############################################################################################

                            elif t.showUps:
                                if x > t.pos.centerx - 9 and x < t.pos.centerx + 13 and y > t.pos.y - 50 and y < t.pos.y - 26:
                                    if money >= int((cost[t.type] / 2) * t.rlevel):
                                        money -= int((cost[t.type] / 2) * t.rlevel)
                                        t.upgradeRange()
                                if x > t.pos.centerx + 13 and x < t.pos.centerx + 35 and y > t.pos.y - 50 and y < t.pos.y - 26:
                                    if money >= int((cost[t.type] / 2) * t.plevel):
                                        money -= int((cost[t.type] / 2) * t.plevel)
                                        t.upgradePow()

                            ############################################################################################

                            if t.type == "Archer": t.pos.centerx -= 3
                        if (x > t.pos.left and x < t.pos.right and y > t.pos.top and y < t.pos.bottom) or (
                                x > t.pos.centerx + 2 and x < t.pos.centerx + 26 and y > t.pos.y - 25 and y < t.pos.y - 1):
                            t.showBtns = True
                        else:
                            t.showBtns = False
                            t.showUps = False

########################################################################################################################


if __name__ == "__main__":
    initialise()