import pygame, random
from object_functions import Rect
from variables import *
from bullet import Bullet

class Mees(object): # peamees
    global SCREEN_WIDTH, SCREEN_HEIGHT  # ekraani laius ja pikkus
    def __init__(self):
        self.lives = 7 # mitu elu mehel
        self.rect = Rect(30,SCREEN_HEIGHT-100,10,10) # ta kast
        self.color = (255,255,0) # ta varv

        self.speed = 0.5 # kiirus

        self.bullets = [] # valjalastud kuulid
        self.bulletCount = 20 # kuulide arv
        
        self.font=pygame.font.Font(None,30)

        #voimalikud relvad
        self.relvad = { "handgun" :
                        { "dmg" : 1,
                          "speed" : 0.5,
                          "hoida" : 0,
                          "bullets" : 12,
                          "pide" : 12,
                          "kokku" : 48,
                          "korraga" : 1
                        },
                        "machinegun" :
                        { "dmg" : 1,
                          "speed" : 0.5,
                          "hoida" : 1,
                          "bullets" : 50,
                          "pide" : 50,
                          "kokku" : 300,
                          "korraga" : 1
                        }
                       } 
        
        self.relv = "handgun" # mis relv hetkel
        
    def update_logic(self):
        #vaatame et kastist v'lja ei laheks
        if(self.rect.y > SCREEN_HEIGHT):
            self.rect.y = SCREEN_HEIGHT
        elif(self.rect.y < 0):
            self.rect.y = 0
        if(self.rect.x > SCREEN_WIDTH):
            self.rect.x = SCREEN_WIDTH
        elif(self.rect.x < 0):
            self.rect.x = 0
            
    def show(self, scr):
        pygame.draw.rect(scr, self.color, self.rect.get())
        scoretext=self.font.render("Bullets:"+str(self.relvad[self.relv]["bullets"])+"/"+str(self.relvad[self.relv]["kokku"]), 1,(255,0,255))
        scoretext2=self.font.render("Lives:"+str(self.lives), 1,(255,0,255))
        scr.blit(scoretext, (300, 730))
        scr.blit(scoretext2, (200, 730))

    def shoot(self,start,end,mouseButton):
        if(self.relvad[self.relv]["bullets"] <= 0): # pole kuule?
            return
        
        for i in range(self.relvad[self.relv]["korraga"]):      # laseme kuulid valja     
            temp = Bullet(start[0],start[1],end[0],end[1],self.relvad[self.relv])
            self.bullets.append(temp)
        
        self.relvad[self.relv]["bullets"] -= self.relvad[self.relv]["korraga"]

        if(self.relvad[self.relv]["bullets"] <= 0):
            if(self.relvad[self.relv]["kokku"] > 0): #vaatame kas varupidemes
                if(self.relvad[self.relv]["kokku"] <= 12):
                    self.relvad[self.relv]["bullets"] += self.relvad[self.relv]["kokku"]
                    self.relvad[self.relv]["kokku"] = 0
                else:
                    self.relvad[self.relv]["bullets"] += self.relvad[self.relv]["pide"]
                    self.relvad[self.relv]["kokku"] -= self.relvad[self.relv]["pide"]

    def getRekt(self,dmg):
        self.lives -= dmg
        if(self.lives == 0):
            print ("gameover")
            self.speed = 0