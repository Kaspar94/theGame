from object_functions import *
from variables import *
import math, pygame

class Laine():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    def __init__(self,startX,startY,endX,endY):
        self.x = startX
        self.y = startY
        self.endX = endX
        self.endY = endY
        self.color = (255,255,255)
        self.w = 50
        self.velX = 0
        self.velY = 0
    def update_logic(self):
        pass

    def show(self,screen):
        #pygame.draw.line(screen,self.color,(self.startX,self.startY),(self.endX,self.endY))

        endY = self.endY
        endX = self.endX



        dist = calc_len(self.x,self.y,endX,endY)

        tx = endX-self.x
        ty = endY-self.y
        rad = math.atan2(ty,tx)
        angle = rad/math.pi*180
        velX = (tx/dist)
        velY = (ty/dist)
        if(dist > 1):
            self.x += velX
            self.y += velY
        #circle(Surface, color, pos, radius, width=0) -> Rect
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),100)