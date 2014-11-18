import pygame, random
from object_functions import *

class PahaPoiss(object):
    def __init__(self, type):
        """

        hello, im a bad guy
        """
        self.elusi = type["elusi"]
        self.rect = Rect(crd_out_x(600), crd_out_y(600), type["w"], type["h"]) # kus kutt spawnib
        self.color = type["color"] # v2rv
        self.speed = type["speed"] # ta kiirus
        self.dmg = type["dmg"] # kuti d2mm
        
    def attack(self,target):

        # liigub koguaeg peamehe poole
        if(self.rect.x < target.rect.x):
            self.rect.x += self.speed
        elif(self.rect.x > target.rect.x):
            self.rect.x -= self.speed
        if(self.rect.y < target.rect.y):
            self.rect.y += self.speed
        elif(self.rect.y > target.rect.y):
            self.rect.y -= self.speed
        #if(abs(self.rect.y - target.rect.y)<10): """ huiamine """
        #    self.rect.y += random.randint(-2,2)*20
        #    print ("ja")

    def show(self, scr): # joonistame valja
        pygame.draw.rect(scr, self.color, self.rect.get())

    def getRekt(self,dmg): # kui saab pihta kuuliga.
        self.elusi -= dmg
        if(self.elusi <= 0):
            return True
        else:
            return False