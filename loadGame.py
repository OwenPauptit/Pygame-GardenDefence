import tower,main,pygame

def load(saveSlot):
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    music = pygame.mixer.Sound("Sounds\BGM.wav").play(-1)
    width = 1200
    height = 700
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Garden Defence")
    screen.blit(main.Images.bg,(0,0))
    pygame.display.update()
    wave = main.Wave()
    font = pygame.font.Font("digital-7.ttf",72)
    cost = {"Archer":20,"Mortar":60,"Beehive":100}
    dfont = pygame.font.Font("digital-7.ttf",24)

    file = open("Data\save"+str(saveSlot)+".txt","r")
    rwave = int(file.readline())
    money = int(file.readline())
    playerHealth = int(file.readline())
    numT = int(file.readline())

    towArr = []
    towers = []

    for i in range(0,numT):
        type = file.readline()
        x = int(file.readline())
        y = int(file.readline())
        plevel = int(file.readline())
        rlevel = int(file.readline())
        towArr.append([type,(x,y),plevel,rlevel])

    for tower in towArr:
        type = "main.new"+tower[0][:(len(tower[0])-1)]+"(screen, main.Images.bg, [], [], 0, '', '', (0,0), loading=True,pos="+str(tower[1])+")"
        towers.append(eval(type))
        while tower[2] > 1:
            towers[len(towers)-1].upgradePow()
            tower[2] -= 1
        while tower[3] > 1:
            towers[len(towers)-1].upgradeRange()
            tower[3] -= 1

    wave.index = rwave -1
    wave.Break()

    main.main(width,height,screen,wave,playerHealth,font,towers,money,cost,dfont,music)

    # print (wave,money,health,numT)
    # for i,t in enumerate(towers):
    #     print ("\nTower",i)
    #     print (t.type)
    #     print(t.plevel)
    #     print(t.rlevel)
    #     print (t.pos.center)

if __name__ == "__main__":
    load(1)