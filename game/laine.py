from object_functions import *
from variables import *
import math, pygame

class Laine():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    def __init__(self,startX,startY,endX,endY):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.color = (255,255,255)
        self.w = 50
    def update_logic(self):
        pass

    def show(self,screen):
        pygame.draw.line(screen,self.color,(self.startX,self.startY),(self.endX,self.endY))

        endY = self.endY
        endX = self.endX
        length = calc_len(self.startX,self.startY,self.endX,self.endY)

        len2 = abs(self.startY-self.endY)
        deg = math.degrees(math.asin(len2/length))
        alfa = math.radians(90-deg)
        alfa_2 = math.radians(90+deg)

        if endY < SCREEN_HEIGHT/2 and endX > SCREEN_WIDTH/2 or endY > SCREEN_HEIGHT/2 and endX < SCREEN_WIDTH/2:
            finalX1 = endX+self.w * math.cos(alfa)
            finalY1 = endY+self.w * math.sin(alfa)
            finalX2 = endX-self.w * math.cos(alfa)
            finalY2 = endY-self.w * math.sin(alfa)
            pygame.draw.line(screen,self.color,(endX,endY),(finalX1, \
                                                       finalY1))
            pygame.draw.line(screen,self.color,(endX,endY),(finalX2, \
                                                       finalY2))

        else:
            finalX1 = endX+self.w * math.cos(alfa_2)
            finalY1 = endY+self.w * math.sin(alfa_2)
            finalX2 = endX-self.w * math.cos(alfa_2)
            finalY2 = endY-self.w * math.sin(alfa_2)
            pygame.draw.line(screen,self.color,(endX,endY),(finalX1, \
                                                       finalY1))
            pygame.draw.line(screen,self.color,(endX,endY),(finalX2, \
                                                    finalY2))