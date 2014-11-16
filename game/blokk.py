from object_functions import *
import random, pygame
from variables import *
class Blokk(object): # tyypiline takistus
    global SCREEN_HEIGHT
    def __init__(self,tyyp):
        self.dx = random.uniform(0.1,tyyp["maxKiirus"])
        self.maxW = tyyp["maxW"]
        self.maxH = tyyp["maxH"]
        self.lykkab = tyyp["lykkab"]
        self.dmg = tyyp["dmg"]
        self.color = tyyp["color"] # v2rv
        self.rect = Rect(0,0,0,0) # loome ymbrise
        self.new_crds()
        self.new_shape()
        self.dy = 0 # speed

    def update_logic(self):
        if(self.rect.x < 0 and self.dx < 0 or self.rect.x > SCREEN_WIDTH and self.dx > 0):
            self.new_crds()
            self.new_shape()
        self.rect.x += self.dx
        self.rect.y += self.dy
    def show(self, scr): # n2itab 
        pygame.draw.rect(scr, self.color ,self.rect.get())

    def new_shape(self): # loob uue kuju blokile
        self.rect.w = random.randint(5,self.maxW)
        self.rect.h = random.randint(5,self.maxH)

    def new_crds(self):
        self.rect.x = crd_out_x(200) # votame suvad koordinaadid
        self.rect.y = crd_in_y()
        if(self.rect.x > 0):
            self.dx = -self.dx # kui kast tuleb paremalt poolt, muudame suunda
            #self.lykkab = -self.lykkab # lykkab vasakule mitte paremale