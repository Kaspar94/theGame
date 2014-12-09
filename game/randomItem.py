from timer import Timer
from object_functions import *
import pygame
import random
class RandomItem():
    def __init__(self,relvad,potid):
        self.rect = Rect(crd_in_x(),crd_in_y(),10,10)

        self.font=pygame.font.Font(None,30)

        self.timer = Timer(random.randint(10,20))
        self.timer.run()
        self.relvad = relvad
        self.potid = potid
        typeRandom = random.randint(1,20)
        if(typeRandom<3):
            self.type = "weapon"
            self.value = random.choice(list(relvad.keys()))
        elif(typeRandom > 2 and typeRandom < 15):
            self.type = "pot"
            self.value = random.choice(list(potid.keys()))
        else:
            self.type = "bullets"
            self.weaponType = random.choice(list(relvad.keys())) # pump
            self.value = self.relvad[self.weaponType]["pide"]*random.randint(1,3)
    def update(self):
        self.timer.update()

    def show(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.rect.get())
        text=self.font.render(str(self.timer.get_secs()), 1,(0,255,255))
        screen.blit(text, (self.rect.x,self.rect.y))

    def end(self):
        if(self.timer.end):
            return True
        else:
            return False




