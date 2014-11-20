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

    def check_collision(self,blokk):
        if(collision(self.rect,blokk.rect)):
            if(blokk.suund == "hor"): # blokk liigub horisontaalselt
                # tulles alt voi ylevalt lykkame tagasi
                if(self.rect.x+self.rect.w<blokk.rect.x+blokk.rect.w and (self.rect.y < blokk.rect.y)):
                    self.rect.y = blokk.rect.y-self.rect.h
                    return
                elif(self.rect.x+self.rect.w<blokk.rect.x+blokk.rect.w and(self.rect.y+self.rect.h>blokk.rect.y+blokk.rect.h)):
                    self.rect.y = blokk.rect.y+blokk.rect.h
                    return

                if(blokk.dx > 0): # blokk liigub paremale
                    if(self.rect.x+self.rect.w>blokk.rect.x+blokk.rect.w):
                        self.rect.x = blokk.rect.x+blokk.rect.w
                       # self.rect.x += blokk.lykkab
                    else:
                        self.rect.x = blokk.rect.x-self.rect.w
                elif(blokk.dx < 0): # blokk liigub vasakule
                    if(self.rect.x<blokk.rect.x):
                        self.rect.x =  blokk.rect.x-self.rect.w
                        #self.rect.x -= blokk.lykkab
                    else:
                        self.rect.x = blokk.rect.x+blokk.rect.w

            elif(blokk.suund == "ver"): # blokk liigub vertikaalselt
                # tulles alt voi ylevalt lykkame tagasi
                if(self.rect.y+self.rect.h<blokk.rect.y+blokk.rect.h and (self.rect.x < blokk.rect.x)):
                    self.rect.x = blokk.rect.x-self.rect.w
                    return
                elif(self.rect.y+self.rect.h<blokk.rect.y+blokk.rect.h and self.rect.x+self.rect.w>blokk.rect.x+blokk.rect.w):
                    self.rect.x = blokk.rect.x+blokk.rect.w
                    return

                if(blokk.dy > 0): # blokk liigub alla
                    if(self.rect.y+self.rect.h>blokk.rect.y+blokk.rect.h):
                        self.rect.y = blokk.rect.y+blokk.rect.h
                        #self.rect.y += blokk.lykkab
                    else:
                        self.rect.y = blokk.rect.y-self.rect.h
                elif(blokk.dy < 0): # blokk liigub yles
                    if(self.rect.y<blokk.rect.y):
                        self.rect.y =  blokk.rect.y-self.rect.h
                        #self.rect.y -= blokk.lykkab
                    else:
                        self.rect.y = blokk.rect.y+blokk.rect.h