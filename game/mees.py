import pygame, random
from object_functions import *
from variables import *
from bullet import Bullet
from timer import Timer

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
        self.relvad = {
            "handgun" :
                { "dmg" : 1, # palju relv dmg teeb
                  "speed" : 0.5, # kui kiirelt kuul lendab
                  "hoida" : 0, # kas automaat
                  "bullets" : 12, # palju kuule
                  "pide" : 12, # palju pide hoiab
                  "kokku" : 48, # palju kokku kuule
                  "korraga" : 1
                },
            "machinegun" :
                { "dmg" : 1,
                  "speed" : 2,
                  "hoida" : 1,
                  "bullets" : 50,
                  "pide" : 50,
                  "kokku" : 300,
                  "korraga" : 1,
                  "vahe" : 0.2 # kuulide laskmis vahe ajaliselt automaatselt
                },
            "pump" :
                { "dmg" : 1,
                  "speed" : 1.5,
                  "hoida" : 0,
                  "bullets" : 8,
                  "pide" : 8,
                  "kokku" : 72,
                  "korraga" : 1,
                  "vahe" : 0.2 # kuulide laskmis vahe ajaliselt automaatselt(kui hoida == 1)
               }
        }
        
        self.relv = "handgun" # mis relv hetkel
        self.relvakogu = { # 1 kui olemas, 0 kui mitte
            "handgun" : 1,
            "machinegun" : 1,
            "pump" : 1
        }

        self.shootTimer = Timer(1)

    def update_logic(self):
        self.shootTimer.update()
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

    def switchWeapon(self,slot): # vahetab relva
        if(self.relvakogu[slot] == 1): # relv on relvakogus
            self.relv = slot
            print (self.relv)
        else:
            return
    def drinkPotion(self,pot): # juuakse potti
        pass

    def shoot(self,start,end,mouseButton):
        if(self.relvad[self.relv]["kokku"] <= 0 and self.relvad[self.relv]["bullets"] <= 0): # pole kuule?
            return

        for i in range(self.relvad[self.relv]["korraga"]):      # laseme kuulid valja     
            temp = Bullet(start[0],start[1],end[0],end[1],self.relvad[self.relv])
            if(self.relv == "pump"): # 2 kuuli lisaks
                temp2 = Bullet(start[0],start[1],end[0]-50,end[1]-50,self.relvad[self.relv])
                temp3 = Bullet(start[0],start[1],end[0]+50,end[1]+50,self.relvad[self.relv])
                self.bullets.append(temp2)
                self.bullets.append(temp3)
            self.bullets.append(temp)
        
        self.relvad[self.relv]["bullets"] -= self.relvad[self.relv]["korraga"]

        if(self.relvad[self.relv]["bullets"] <= 0):
            if(self.relvad[self.relv]["kokku"] > 0): #vaatame kas varupidemes
                if(self.relvad[self.relv]["kokku"] <= self.relvad[self.relv]["pide"]): # viimane pide
                    self.relvad[self.relv]["bullets"] += self.relvad[self.relv]["kokku"]
                    self.relvad[self.relv]["kokku"] = 0
                else:
                    self.relvad[self.relv]["bullets"] += self.relvad[self.relv]["pide"]
                    self.relvad[self.relv]["kokku"] -= self.relvad[self.relv]["pide"]

    def automatic(self):
        """
        automaatne tulistamine
        """
        if(self.relvad[self.relv]["hoida"] == 1):
            if(self.shootTimer.end):
                self.shoot((self.rect.x,self.rect.y),pygame.mouse.get_pos(),pygame.mouse.get_pressed())
                self.shootTimer.reset_n(self.relvad[self.relv]["vahe"])
                self.shootTimer.reset()
        else: return

    def getRekt(self,dmg):
        """
        peategelane saab dmgi
        """
        self.lives -= dmg # vahendame elusi dmg vorra

        if(self.lives == 0): # kas oleme surnud?
            # ... siia midagi valja moelda
            print ("gameover")
            self.speed = 0
            return True # tagastab true kui null elu, et mang teaks mida edasi teha
        return False

    def check_collision(self,blokk): # uurib kokkupuudet mehe ja bloki vahel

        if(collision(blokk.rect, self.rect)): #kokkuporge MEHE JA BLOKI VAHEL

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
                        self.rect.x += blokk.lykkab
                    else:
                        self.rect.x = blokk.rect.x-self.rect.w
                elif(blokk.dx < 0): # blokk liigub vasakule
                    if(self.rect.x<blokk.rect.x):
                        self.rect.x =  blokk.rect.x-self.rect.w
                        self.rect.x -= blokk.lykkab
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
                        self.rect.y += blokk.lykkab
                    else:
                        self.rect.y = blokk.rect.y-self.rect.h
                elif(blokk.dy < 0): # blokk liigub yles
                    if(self.rect.y<blokk.rect.y):
                        self.rect.y =  blokk.rect.y-self.rect.h
                        self.rect.y -= blokk.lykkab
                    else:
                        self.rect.y = blokk.rect.y+blokk.rect.h


