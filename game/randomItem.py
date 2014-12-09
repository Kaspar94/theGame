from timer import Timer
from object_functions import *
import pygame
import random
class RandomItem():
    def __init__(self):
        self.rect = Rect(crd_in_x(),crd_in_y(),10,10)

        self.font=pygame.font.Font(None,30)

        self.timer = Timer(random.randint(5,15))
        self.timer.run()

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

