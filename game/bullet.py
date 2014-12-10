import pygame, math
from object_functions import *
class Bullet(object):
    def __init__(self,startX,startY,mouseX,mouseY,relv=False):
        self.rect = Rect(startX,startY,5,5)
        self.startX = startX
        self.startY = startY
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.image = pygame.image.load("Pics/bullet.png").convert()
        if(relv != False):
            self.relv = relv
            self.speed = self.relv["speed"]
            self.dmg = self.relv["dmg"]
        else:
            self.speed = 0.5
            self.dmg = 1

        self.distance = (self.mouseX - self.startX, self.mouseY - self.startY) # they did the math
        self.norm = math.sqrt(self.distance[0] ** 2 + self.distance[1] ** 2)
        self.direction = (self.distance[0] / self.norm, self.distance[1] / self.norm)
        self.bullet_vector = (self.direction[0] * self.speed, self.direction[1] * self.speed)
        self.color = self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
    def update_logic(self):
        self.rect.x += self.bullet_vector[0]
        self.rect.y += self.bullet_vector[1]
        
    def show(self,scr):
        scr.blit(self.image, self.rect.get())
        
    