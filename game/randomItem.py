from timer import Timer
from object_functions import *
import pygame
import random
class RandomItem():
    def __init__(self,relvad,potid):

        self.bullets = pygame.image.load("Pics/bullets.png").convert_alpha()
        self.weaponCrate = pygame.image.load("Pics/weaponcrate.png").convert_alpha()
        self.speedpot = pygame.image.load("Pics/speedpot.png").convert_alpha()
        self.hppot2 = pygame.image.load("Pics/2HPpot.png").convert_alpha()
        self.hppot5 = pygame.image.load("Pics/5HPpot.png").convert_alpha()

        self.rect = Rect(crd_in_x(),crd_in_y(),10,10)

        self.font=pygame.font.Font(None,30)
        self.timer = Timer(random.randint(10,20))
        self.timer.run()
        self.relvad = relvad
        self.potid = potid

        typeRandom = random.randint(1,20)

        if(typeRandom<=5):
            self.type = "weapon"
            self.image = self.weaponCrate
            self.value = random.choice(list(relvad.keys()))
        elif(typeRandom > 5 and typeRandom < 19):
            self.type = "pot"
            self.value = random.choice(list(potid.keys()))
            self.value = 2
            if(self.value == 0):
                self.image = self.hppot2
            elif(self.value == 1):
                self.image = self.hppot5
            elif(self.value == 2):
                self.image = self.speedpot
        else:
            self.type = "bullets"
            self.image = self.bullets
            self.weaponType = random.choice(list(relvad.keys())) # pump
            while self.weaponType == "handgun":
                self.weaponType = random.choice(list(relvad.keys())) # pump
            self.value = self.relvad[self.weaponType]["pide"]*random.randint(1,5)

        self.newRect = self.image.get_rect()
        self.rect.w = self.newRect[2]
        self.rect.h = self.newRect[3]
    def update(self):
        self.timer.update()

    def show(self,screen):
        screen.blit(self.image, self.rect.get())
        text=self.font.render(str(self.timer.get_secs()), 1,(0,255,255))
        screen.blit(text, (self.rect.x,self.rect.y))

    def end(self):
        if(self.timer.end):
            return True
        else:
            return False




