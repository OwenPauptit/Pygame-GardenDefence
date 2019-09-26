def save(towers,wavenum,money,health,slot):
    file = open("Data\save"+str(slot)+".txt","w")
    file.write(str(wavenum)+"\n")
    file.write(str(money)+"\n")
    file.write(str(health)+"\n")
    file.write(str(len(towers))+"\n")
    for t in towers:
        file.write(t.type+"\n")
        file.write(str(t.pos.centerx)+"\n")
        file.write(str(t.pos.centery)+"\n")
        file.write(str(t.plevel)+"\n")
        file.write(str(t.rlevel)+"\n")
    file.close()

if __name__=="__main__":
    save([],10,1,6,2)
