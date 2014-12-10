from timer import Timer
from object_functions import *
import pygame
import random
class RandomItem():
    def __init__(self,relvad,potid):
        bullets = pygame.image.load("Pics/bullets.png").convert_alpha()
        weaponCrate = pygame.image.load("Pics/weaponcrate.png").convert_alpha()
        speedpot = pygame.image.load("Pics/speedpot.png").convert_alpha()
        #2hppot = pygame.image.load("Pics/2HPpot.png").convert_alpha()
        #5hppot = pygame.image.load("Pics/5HPpot.png").convert_alpha()
        self.rect = Rect(crd_in_x(),crd_in_y(),10,10)

        self.font=pygame.font.Font(None,30)

        self.timer = Timer(random.randint(10,20))
        self.timer.run()
        self.relvad = relvad
        self.potid = potid
        typeRandom = random.randint(1,20)
        if(typeRandom<=5):
            self.type = "weapon"
            self.image = weaponCrate
            self.value = random.choice(list(relvad.keys()))
        elif(typeRandom > 5 and typeRandom < 15):
            self.type = "pot"
            self.image = speedpot
            self.value = random.choice(list(potid.keys()))
        else:
            self.type = "bullets"
            self.image = bullets
            self.weaponType = random.choice(list(relvad.keys())) # pump
            self.value = self.relvad[self.weaponType]["pide"]*random.randint(1,5)
    def update(self):
        self.timer.update()

    def show(self,screen):
        screen.blit(self.image, self.rect.get())
        #pygame.draw.rect(screen,(0,0,0),self.rect.get())
        text=self.font.render(str(self.timer.get_secs()), 1,(0,255,255))
        screen.blit(text, (self.rect.x,self.rect.y))

    def end(self):
        if(self.timer.end):
            return True
        else:
            return False




