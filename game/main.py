"""
p - PAUS
hiireklikk - tulistamine
ASDW - liikumine

Autorid: Kaspar Kliimask, Madis Kariler eheh
"""
import pygame, sys, random, math, time, os

from timer import Timer
from object_functions import *
from blokk import Blokk
from mees import Mees
from enemy import PahaPoiss
from variables import *


class Game:
    def __init__(self, WIDTH, HEIGHT):
        """
        peaklass
        """
        global levelTime

        pygame.init()

        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

        #pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        #pygame.mixer.music.load('madis.mp3') # <--------------------------------------------------------- SIIN TAUSTAMUSS 
        #pygame.mixer.music.play(-1)  # mitu korda m'ngib

        """
        kiirus - bloki kiirus
        maxw - maksimaalne laius
        maxh - maksimaaline pikkus
        lykkab - mitu pixlit lykkab eemale kokkuporkel
        dmg - mitu dmg teeb lykkamisega
        """
        self.blokityyp = {
            "tavaline" : {
                "maxKiirus" : 0.6,
                "maxW" : 50,
                "maxH" : 50,
                "lykkab" : 0,
                "dmg" : 0,
                "color" : (0,200,0)
            },
            "lykkaja" : {
                "maxKiirus" : 0.4,
                "maxW" : 10,
                "maxH" : 60,
                "lykkab" : 200,
                "dmg" : 2,
                "color" : (125,120,50)
            }


        }

        self.blokid = []
        self.pahad = []

        self.font=pygame.font.Font(None,30)

        self.level = 1

        self.levelTimer = Timer(levelTime)

        self.run = True

    def update_logic(self):
        self.mees.update_logic() # uuendab meest
        
        for blokk in self.blokid:
            blokk.update_logic()
    
            if (collision(blokk.rect, self.mees.rect)): #kokkuporge MEHE JA BLOKI VAHEL
                if(blokk.dx < 0): # blokk liigub vasakule
                    if(self.mees.rect.x <= blokk.rect.x):
                        self.mees.rect.x = blokk.rect.x-self.mees.rect.w # lykkame kaasa
                        self.mees.rect.x -= blokk.lykkab
                    else:
                        self.mees.rect.x += 1 # lykkame tagasi
                        self.mees.rect.x += blokk.lykkab
                elif(blokk.dx > 0): # blokk liigub paremale
                    if(self.mees.rect.x >= blokk.rect.x):
                        self.mees.rect.x = blokk.rect.x+blokk.rect.w
                        self.mees.rect.x += blokk.lykkab
                    else:
                        self.mees.rect.x -= 1
                        self.mees.rect.x -= blokk.lykkab

        self.check_bullets() # uuendab kuulidega seotud loogikat

        for enemy in game.pahad:
            enemy.attack(self.mees) # tyre

            if(collision(enemy.rect, self.mees.rect)): # kui paha puutub peameest
                self.mees.getRekt(enemy.dmg) # peamees saab dmg
                self.pahad.remove(enemy) # paha ohverdas kahjuks end :(

    def update_display(self):
        self.screen.fill((255,255,255)) # background
        self.mees.show(game.screen) # peavend
        
        for blokk in self.blokid: # joonistame koik blokid
            blokk.show(self.screen)
            
        for bullet in self.mees.bullets: # joonistame koik kuulid
            bullet.show(self.screen)
            
        for enemy in self.pahad: # joonistame koik pahad
            enemy.show(self.screen)

        # muu lape
        pygame.draw.rect(self.screen, (0,0,0), (0,700,640,10)) # porand
        scoretext=self.font.render("Score:"+str(self.level), 1,(0,255,255))
        self.screen.blit(scoretext, (200, 700))
        pygame.display.flip()
        
    def Level(self):
        if(self.levelTimer.end == True):
            self.levelTimer.reset()
            self.next_level()
            self.del_bloks()
            self.del_enemies()
            self.create_bloks(self.level*3)
            self.create_enemies(self.level*3)
    def next_level(self):
        self.level += 1 # uuendame levelit
        time.sleep(1)
        print ("nextlvl")
        #self.blokid = [] # kustutame vanad ?
        #self.pahad = []
        
    def create_bloks(self,count): # loob uusi blokke
        for i in range(count):
            if(random.randint(1,3) > 1): # yks kolmele et tuleb ull blokk
                temp = Blokk(self.blokityyp["tavaline"])
            else:
                temp = Blokk(self.blokityyp["lykkaja"])

            self.blokid.append(temp)

    def create_enemies(self,count): # loob uusi vastaseid
        for i in range(count):
            temp = PahaPoiss(game.level,1,20)
            self.pahad.append(temp)

    def del_bloks(self):
        self.blokid = []

    def del_enemies(self):
        self.pahad = []

    def check_bullets(self): # 
        for bullet in self.mees.bullets: # vaatame millega kuulid kokku porkavad :
            bullet.update_logic()
            for blokk in self.blokid: # blokiga?
                if(collision(bullet.rect, blokk.rect)):
                   self.mees.bullets.remove(bullet) # kui jah siis kustutame kuuli.
                   break
            for enemy in self.pahad: # pahade poistega ?
                if(collision(bullet.rect, enemy.rect)):
                    if (enemy.getRekt(bullet.dmg)):
                        self.pahad.remove(enemy)
                    if(bullet in self.mees.bullets): # mingi lamp
                        self.mees.bullets.remove(bullet)
    
    




game = Game(SCREEN_WIDTH, SCREEN_HEIGHT) # peamaang
game.mees = Mees() # peavend

""" level 1 """
game.create_bloks(10) # viis vastast
game.create_enemies(2) # kaks vastast
"""         """


while game.run == True: # main loop
    game.levelTimer.update()
    #EVENT
    for evt in pygame.event.get(): # koik eventid
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_p:
                game.levelTimer.pauseChange()
        if evt.type == pygame.QUIT: # kasutaja soovib lahkuda
            game.run = False
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if(game.levelTimer.paused == -1):
                game.mees.shoot((game.mees.rect.x,game.mees.rect.y),pygame.mouse.get_pos(),pygame.mouse.get_pressed())
        
    if(game.levelTimer.paused == 1):
        continue
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_a]):
        game.mees.rect.x -= game.mees.speed
    if(keys[pygame.K_d]):
        game.mees.rect.x += game.mees.speed
    if(keys[pygame.K_w]):
        game.mees.rect.y -= game.mees.speed
    if(keys[pygame.K_s]):
        game.mees.rect.y += game.mees.speed

            
    #LOGIC
    
    game.update_logic()
    
    game.Level()
        
    #DISPLAY
        
    game.update_display()
           
pygame.quit()

