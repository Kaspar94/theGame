import pygame, random
from object_functions import *
from timer import Timer
from bullet import Bullet
class Enemy(object):
    def __init__(self, type):
        """
        hello, im a bad guy
        """

        self.elusi = type["elusi"] # palju kutil elusi
        self.rect = Rect(crd_out_x(700), crd_out_y(700), type["w"], type["h"]) # kus kutt spawnib
        self.color = type["color"] # v2rv
        self.speed = type["speed"] # ta kiirus
        self.dmg = type["dmg"] # kuti d2mm kokkuporkel mehega
        self.shooter = False # eeldame et pole laskja

        if("weapon" in type): # kui kutil on relv
            self.shooter = True # ikka on laskja
            self.shootTimer = Timer(type["delay"]) # mitme sekundi tagant kuulid lendama hakkavad.
            self.bullets = []

        
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

        if(self.shooter): # pahalpoisil on relv!
            self.shootTimer.update() # uuendame tulistamis timerit

            if(self.shootTimer.end): # taimer jooksis nulli, ehk aeg lasta
                self.shoot(target)
                self.shootTimer.reset()

            for bullet in self.bullets: # uuendame kuule mis valja lastud
                bullet.update_logic()

        #if(abs(self.rect.y - target.rect.y)<10): """ huiamine """ # poiklemine kuulida eest siia!
        #    self.rect.y += random.randint(-2,2)*20
        #    print ("ja")

    def show(self, scr): # joonistame valja
        if(rect_in_map(self.rect)): # kontrollime kas objekt mapi sees et mitte teha asjatuid joonistamisi.
            pygame.draw.rect(scr, self.color, self.rect.get())

        if(self.shooter):
            for bullet in self.bullets:
                bullet.show(scr)

    def getRekt(self,dmg): # kui saab pihta kuuliga.
        self.elusi -= dmg
        if(self.elusi <= 0):
            return True
        else:
            return False

    def shoot(self,target):
        end = (target.rect.x,target.rect.y)
        temp = Bullet(self.rect.x,self.rect.y,end[0],end[1])
        self.bullets.append(temp)