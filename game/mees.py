import pygame

from object_functions import *
from variables import *
from bullet import Bullet
from timer import Timer

class Mees(object): # peamees
    global SCREEN_WIDTH, SCREEN_HEIGHT  # ekraani laius ja pikkus
    def __init__(self):

        #pygame.mixer.init(frequency=22050, size=-16, channels=4)
        self.saund = pygame.mixer.Sound("Sounds/singleshot.wav")
        self.saund.set_volume(0.2)
        self.chan = pygame.mixer.find_channel()

        self.saund2 = pygame.mixer.Sound("Sounds/teleport2.wav")
        self.saund2.set_volume(0.8)
        self.chan2 = pygame.mixer.find_channel()

        self.saund3 = pygame.mixer.Sound("Sounds/pickup.wav")
        self.saund3.set_volume(0.8)
        self.chan3 = pygame.mixer.find_channel()


        self.lives = 7 # mitu elu mehel
        self.rect = Rect(30,SCREEN_HEIGHT-100,10,10) # ta kast
        self.image = pygame.transform.scale((pygame.image.load("Pics/Kappa.png").convert_alpha()), (30,30))
        self.imageDisco = pygame.transform.scale((pygame.image.load("Pics/discokappa.png").convert_alpha()), (30,30))
        self.image2 = pygame.image.load('Pics/Untitled.png').convert_alpha()
        self.image2Rect = self.image2.get_rect()
        self.newRect = self.image.get_rect()
        self.rect.w = self.newRect[2]
        self.rect.h = self.newRect[3]
        self.speed = 0.8 # kiirus

        self.bullets = [] # valjalastud kuulid
        self.bulletCount = 20 # kuulide arv
        
        self.font=pygame.font.Font(None,30)

        #voimalikud relvad
        self.relvad = {
            "handgun" :
                { "dmg" : 1, # palju relv dmg teeb
                  "speed" : 2, # kui kiirelt kuul lendabs
                  "hoida" : 0, # kas automaat
                  "bullets" : 12, # palju kuule
                  "pide" : 12, # palju pide hoiab
                  "kokku" : -1 # palju kokku kuule
                },
            "machinegun" :
                { "dmg" : 1,
                  "speed" : 4,
                  "hoida" : 1,
                  "bullets" : 50,
                  "pide" : 50,
                  "kokku" : 300,
                  "vahe" : 0.2 # kuulide laskmis vahe ajaliselt automaatselt
                },
            "pump" :
                { "dmg" : 1,
                  "speed" : 2,
                  "hoida" : 0,
                  "bullets" : 8,
                  "pide" : 8,
                  "kokku" : 72,
               }
        }
        self.potid = {
            0 :
                {
                    "heals" : 2,
                     #"img" : "Pics/2HPpot.png"
                },
            1 :
                {
                    "heals" : 5
                    #"img" : "Pics/5HPpot.png"
                },
            2 :
                {
                    "speed" : 2,
                    "time" : 20
                }
        }

        self.relv = "handgun" # mis relv hetkel

        self.relvakogu = ["handgun","machinegun"]
        self.potikogu = []

        self.shootTimer = Timer(1)
        self.speedTimer = Timer(0)
        self.shootTimer.run()
        self.koos = []
        self.saiJuurde = 0
        self.dead = 0
    def update_logic(self):
        self.shootTimer.update()
        self.speedTimer.update()

        #vaatame et kastist v'lja ei laheks
        if(self.rect.y > SCREEN_HEIGHT-self.rect.h):
            self.rect.y = SCREEN_HEIGHT-self.rect.h
        elif(self.rect.y < 0):
            self.rect.y = 0
        if(self.rect.x > SCREEN_WIDTH-self.rect.w):
            self.rect.x = SCREEN_WIDTH-self.rect.w
        elif(self.rect.x < 0):
            self.rect.x = 0

        for bullet in self.bullets:
            bullet.update_logic()

        if(self.speedTimer.end == True and self.saiJuurde != 0):
            self.speed -= self.saiJuurde
            self.saiJuurde = 0
            
    def show(self, scr):
        if(self.saiJuurde != 0):
            scr.blit(self.imageDisco,self.rect.get())
        else:
            scr.blit(self.image,self.rect.get())

        for bullet in self.bullets: # joonistame koik kuulid
            bullet.show(scr)
        if (self.dead == 1):
            scr.blit(self.image2,self.image2Rect)
    def switchWeapon(self,slot): # vahetab relva
        try:
            self.relv = self.relvakogu[slot]
        except Exception as e:
            print (e)
            return

    def drinkPotion(self,slot): # juuakse potti
        try:
            if(self.speed != 0): # kui pole surnud
                pot = self.potid[self.potikogu[slot]]
                if "heals" in pot:
                    self.lives += pot["heals"]
                if "speed" in pot:
                    self.saiJuurde = pot["speed"]
                    self.speed += self.saiJuurde
                    self.speedTimer.reset_n(pot["time"])
                    self.speedTimer.reset()
                    self.speedTimer.run()
            del self.potikogu[slot]
        except Exception as e:
            print (e)
            return

    def shoot(self,start,end,mouseButton):
        if(self.relvad[self.relv]["kokku"] <= 0 and self.relvad[self.relv]["bullets"] <= 0 and self.relvad[self.relv]["kokku"] != -1): # pole kuule?
            return

        temp = Bullet(start[0],start[1],end[0],end[1],self.relvad[self.relv])
        self.chan.queue(self.saund) #############################SOUND
        if(self.relv == "pump"): # 2 kuuli lisaks
            temp2 = Bullet(start[0],start[1],end[0]-50,end[1]-50,self.relvad[self.relv])
            temp3 = Bullet(start[0],start[1],end[0]+50,end[1]+50,self.relvad[self.relv])
            self.bullets.append(temp2)
            self.bullets.append(temp3)
        self.bullets.append(temp)
        self.relvad[self.relv]["bullets"] -= 1 # laseb yhe kuuli valja

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

        if(self.lives <= 0): # kas oleme surnud?
            # ... siia midagi valja moelda
            # print ("gameover")
            self.speed = 0
            self.dead = 1
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
                        self.getRekt(blokk.dmg) # blokk teeb dmg ka kokkuporkel.
                    else:
                        self.rect.x = blokk.rect.x-self.rect.w
                elif(blokk.dx < 0): # blokk liigub vasakule
                    if(self.rect.x<blokk.rect.x):
                        self.rect.x =  blokk.rect.x-self.rect.w
                        self.rect.x -= blokk.lykkab
                        self.getRekt(blokk.dmg) # blokk teeb dmg ka kokkuporkel.
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
                        self.getRekt(blokk.dmg) # blokk teeb dmg ka kokkuporkel.

                    else:
                        self.rect.y = blokk.rect.y-self.rect.h
                elif(blokk.dy < 0): # blokk liigub yles
                    if(self.rect.y<blokk.rect.y):
                        self.rect.y =  blokk.rect.y-self.rect.h
                        self.rect.y -= blokk.lykkab
                        self.getRekt(blokk.dmg) # blokk teeb dmg ka kokkuporkel.
                    else:
                        self.rect.y = blokk.rect.y+blokk.rect.h
            self.chan2.queue(self.saund2)

    def pickup(self,item):
        if(item.type=="pot"):
            if(len(self.potikogu) < 3):
                self.potikogu.append(item.value)
                self.chan3.queue(self.saund3)
                return True
        elif(item.type=="weapon"):
            if not (item.value in self.relvakogu):
                self.relvakogu.append(item.value)
                self.chan3.queue(self.saund3)
                return True
        elif(item.type=="bullets"):
            if (item.weaponType in self.relvakogu):
                self.relvad[item.weaponType]["kokku"] += item.value
                self.chan3.queue(self.saund3)
                return True
