from object_functions import *
from variables import *
import math, pygame
def calc_len(x1,y1,x2,y2):
    return (math.sqrt(pow((x2-x1),2)+pow((y2-y1),2)))
class Laine():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    def __init__(self,startX,startY,endX,endY,type):
        self.type = type
        self.x = startX
        self.y = startY
        self.endX = endX
        self.endY = endY
        if(self.type == "lyke"):
            self.color = (0,0,0)
        else:
            self.color = (255,0,0)
        self.r = 100
        self.velX = 0
        self.velY = 0
    def update_logic(self):
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
            return True

    def show(self,screen):
        #circle(Surface, color, pos, radius, width=0) -> Rect
        #if(self.type != "lyke"):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.r)