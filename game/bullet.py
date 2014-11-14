import pygame, math
from object_functions import *
class Bullet(object):
    def __init__(self,startX,startY,mouseX,mouseY,relv):
        self.rect = Rect(startX,startY,5,5)
        self.relv = relv
        self.startX = startX
        self.startY = startY
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = self.relv["speed"]
        self.dmg = self.relv["dmg"]
        
        self.distance = (self.mouseX - self.startX, self.mouseY - self.startY) # they did the math
        self.norm = math.sqrt(self.distance[0] ** 2 + self.distance[1] ** 2)
        self.direction = (self.distance[0] / self.norm, self.distance[1] / self.norm)
        self.bullet_vector = (self.direction[0] * self.speed, self.direction[1] * self.speed)
        self.color = (0,0,0)
        
    def update_logic(self):
        self.rect.x += self.bullet_vector[0]
        self.rect.y += self.bullet_vector[1]
        
    def show(self,scr):
        pygame.draw.rect(scr, self.color, self.rect.get())
        
    