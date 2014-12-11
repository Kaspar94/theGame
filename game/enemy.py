import pygame, random
from object_functions import *
from timer import Timer
from bullet import Bullet
import math
class Enemy(object):
    def __init__(self, type, miniboss=False,crd_x=False,crd_y=False,w=False,h=False):
        """
        hello, im a bad guy
        """
        self.type = type
        self.elusi = self.type["elusi"] # palju kutil elusi
        self.x = crd_out_x(500)
        self.y = crd_out_y(400)
        if(miniboss and w != False and h != False):
            if(crd_x != False and crd_y != False):
                self.x = crd_x
                self.y = crd_y
            self.image = pygame.transform.scale((pygame.image.load(self.type["img"]).convert_alpha()), \
                                             (int(w), int(h)))
        else:
            self.image = pygame.image.load(self.type["img"]).convert_alpha() # välimus
        self.rect = Rect(self.x, self.y, 0, 0) # kus kutt spawniba
        self.speed = self.type["speed"] # ta kiirus
        self.dmg = self.type["dmg"] # kuti d2mm kokkuporkel mehega
        self.shooter = False # eeldame et pole laskja
        self.newRect= self.image.get_rect()
        self.rect.w = self.newRect[2]
        self.rect.h = self.newRect[3]
        self.maxElusi = False
        if("weapon" in type): # kui kutil on relv
            self.shooter = True # ikka on laskja
            self.shootTimer = Timer(self.type["delay"]) # mitme sekundi tagant kuulid lendama hakkavad.
            self.shootTimer.run()
            self.bullets = []

        self.font=pygame.font.Font(None,27)

    def attack(self,target):
        if(self.maxElusi == False):
            self.maxElusi = self.elusi
        self.distance = (target.rect.x - self.rect.x, target.rect.y - self.rect.y) # they did the math
        self.norm = math.sqrt(self.distance[0] ** 2 + self.distance[1] ** 2)
        self.direction = (self.distance[0] / self.norm, self.distance[1] / self.norm)
        self.bullet_vector = (self.direction[0] * self.speed, self.direction[1] * self.speed)

        self.rect.x += self.bullet_vector[0]
        self.rect.y += self.bullet_vector[1]
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
            scr.blit(self.image, self.rect.get())

            #joonistab health bari
            if(self.maxElusi > 0):
                self.greenBar = (self.elusi*self.rect.w)/self.maxElusi
                korgus = self.rect.y+self.rect.h+5
                pygame.draw.line(scr,(0,255,0),(self.rect.x,korgus),(self.rect.x+self.greenBar+2,korgus),3)
                pygame.draw.line(scr,(255,0,0),(self.rect.x+self.greenBar,korgus),(self.rect.x+self.rect.w,korgus),3)
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
        temp = Bullet(self.rect.x+int(self.rect.w/2),self.rect.y+int(self.rect.h/2),end[0],end[1])
        self.bullets.append(temp)

    def check_collision(self,blokk): # ???
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