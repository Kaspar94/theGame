class PahaPoiss(object):
    def __init__(self, eluMax, speedMax, suurusMin):
        self.elusi = random.randint(1,eluMax) # palju pahal kutil elusi on?
        self.rectx,self.recty = crd_out_of_map(300)
        self.rect = Rect(self.rectx, self.recty, random.randint(suurusMin,30), random.randint(suurusMin,30)) # kus kutt spawnib
        self.color = (255,0,255) # v2rv
        self.speed = 0.1 # ta kiirus
        self.dmg = 1
        
    def attack(self,target):
        if(self.rect.x < target.rect.x):
            self.rect.x += self.speed
        elif(self.rect.x > target.rect.x):
            self.rect.x -= self.speed
        if(self.rect.y < target.rect.y):
            self.rect.y += self.speed
        elif(self.rect.y > target.rect.y):
            self.rect.y -= self.speed
        #if(abs(self.rect.y - target.rect.y)<10): """ huiamine """
        #    self.rect.y += random.randint(-2,2)*20
        #    print ("ja")
    def show(self, scr):
        pygame.draw.rect(scr, self.color, self.rect.get())
    def getRekt(self,dmg):
        self.elusi -= dmg
        if(self.elusi <= 0):
            return True
        else:
            return False
