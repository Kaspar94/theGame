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
from enemy import Enemy
from variables import *
from randomItem import RandomItem

class Game:
    def __init__(self, REALWIDTH, REALHEIGHT, GAMEWIDTH, GAMEHEIGHT):
        """
        peaklass
        """
        global levelTime

        pygame.init()

        self.width = GAMEWIDTH
        self.height = GAMEHEIGHT
        self.realwidth = REALWIDTH
        self.realheight = REALHEIGHT
        self.screen = pygame.display.set_mode((self.realwidth,self.realheight))
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) # tavaline hiir n'htamatuks
        self.welcomeScreen = pygame.image.load('Pics/gameAvaekraan.png').convert()
        self.pauseScreen = pygame.image.load('Pics/paused.png').convert_alpha()

        self.background = pygame.transform.scale((pygame.image.load("Pics/spacev1.png").convert()), (1024,768))
        self.bg_imgRect = self.background.get_rect()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load('Music/madis.mp3') # <--------------------------------------------------------- SIIN TAUSTAMUSS
        #pygame.mixer.music.play(-1)  # maitu korda m'ngib
        self.music_playing = 1
        """
        kiirus - bloki kiirus
        maxw - maksimaalne laius
        maxh - maksimaaline pikkus
        lykkab - mitu pixlit lykkab eemale kokkuporkel
        dmg - mitu dmg teeb lykkamisega
        """

        self.blokityyp = {
            "tavaline" : {
                "maxKiirus" : 0.2, # bloki maksimaalne kiirus
                "w" : 50, # laius
                "h" : 50, # pikkus
                "lykkab" : 0, # lykkamistugevus
                "dmg" : 0, # dmg kokkuporkel
                "color" : (0,200,0)
            },
            "lykkaja" : {
                "maxKiirus" : 0.5,
                "w" : 20,
                "h" : 70,
                "lykkab" : 200,
                "dmg" : 2,
                "color" : (125,120,50)
            }


        }
        self.enemytype = {
            "tavaline" : {
                "elusi" : 1,
                "w": 15,
                "h": 15,
                "color" : (255,0,255),
                "speed" : 0.1,
                "dmg" : 1
            },
            "tulistaja" : {
                "elusi" : 2,
                "w" : 20,
                "h" : 20,
                "color" : (255,255,0),
                "speed" : 0.05,
                "dmg" : 2,
                "weapon" : 1,
                "delay" : 1
            },
            "boss" : {
                "boss" : 1,
                "elusi" : 1,
                "w" : 200,
                "h" : 200,
                "color" : (125,0,255),
                "speed" : 0.1,
                "dmg" : 1000,
                "weapon" : 1,
                "delay" : 1
            }
        }

        self.blokid = []
        self.pahad = []

        self.font=pygame.font.Font(None,30)

        self.level = 1

        self.levelTime = levelTime
        self.levelTimer = Timer(self.levelTime)

        self.run = True

        self.mouseHolding = False

        self.gaming = False

        self.randomItems = []

        # timer mis hakkab random aja tagant maha asju genereerima
        self.randomItemTimer = Timer(random.randint(10,self.levelTime*2))
        self.randomItemTimer.run()

        self.bossInit = False # alguses pole bossi

    def update_logic(self):

        if not self.gaming: # kui oleme avalehel voi kuskil mojal
            return

        self.generate_random_items()


        self.mees.update_logic() # uuendab meest

        if(self.mouseHolding): # kui hiirt hoitakse all->automaatne tulistamine
            self.mees.automatic()

        for blokk in self.blokid:

            blokk.update_logic() # uuendame bloki liikumist

            self.mees.check_collision(blokk) # vaatame kas blokk porkab kokku mehega

            for enemy in self.pahad:
                enemy.check_collision(blokk)

        self.check_bullets() # uuendab v2lja lastud kuulidega seotud loogikat

        self.man_item_collision()

        for enemy in game.pahad:
            enemy.attack(self.mees) # lape

            if(collision(enemy.rect, self.mees.rect)): # kui paha puutub peameest
                if(self.mees.getRekt(enemy.dmg)):
                    # mang labi
                    pass
                self.pahad.remove(enemy) # paha ohverdas kahjuks end :(

        #if(len(self.pahad) <= 10):
        #    self.create_enemies(10*self.level)

    def update_display(self): # uuendab koike mida naidatakse

        if self.gaming == True:
            self.screen.blit(self.background, self.bg_imgRect)

            self.mees.show(self.screen) # peavend

            for blokk in self.blokid: # joonistame koik blokid
                blokk.show(self.screen)

            for enemy in self.pahad: # joonistame koik pahad
                enemy.show(self.screen)

            for item in self.randomItems: #joonistame maas olevaid boonus asju
                item.show(self.screen)

            self.draw_text()

            if(self.levelTimer.paused == 1): # m2ng pausitud, n2itame pausi pilti
                self.screen.blit(self.pauseScreen,(0,0))
        else:
            self.screen.blit(self.welcomeScreen,(0,0))

        self.draw_cursor()
        pygame.display.flip()

    def draw_text(self):
        scoretext=self.font.render("Level:"+str(self.level), 1,(0,255,255))
        self.screen.blit(scoretext, (200, 700))
        scoretext2=self.font.render("Time left:"+str(self.levelTimer.get_secs()), 1,(0,255,255))
        self.screen.blit(scoretext2, (300, 700))
        for i,slot in enumerate(self.mees.relvakogu):
            if(game.mees.relv==slot):
                self.slotColor = (255,0,255)
            else:
                self.slotColor = (125,255,0)
            self.slots = self.font.render(str(i+1)+" "+str(slot), 1,self.slotColor)
            self.screen.blit(self.slots, (200+i*100,500))
        for i,slot in enumerate(self.mees.potikogu):
            self.slots = self.font.render(str(i+6)+" "+str(slot), 1,(125,255,0))
            self.screen.blit(self.slots, (500+i*100,500))

        pygame.draw.rect(self.screen,(125,125,125),(0,self.height+10,self.width,self.realheight-self.height))
    def Level(self):
        if(self.levelTimer.end == True):
            if(self.bossInit == False):
                print ("init boss")
                self.del_bloks()
                self.del_enemies()
                boss = Enemy(self.enemytype["boss"])
                boss.rect.w,boss.rect.h = (self.level*100,self.level*100)
                boss.type["h"] = (self.level*100)
                boss.type["w"] = (self.level*100)
                self.pahad.append(boss)
                self.bossInit = True
            else:
                if(len(self.pahad) == 0):
                    print ("p")
                    self.bossInit = False
                    self.levelTimer.reset()
                    self.next_level()

            #self.create_bloks(self.level*20)
            #self.create_enemies(self.level*10)

    def next_level(self):
        self.level += 1 # uuendame levelit
        self.create_bloks(self.level*5)
        self.create_enemies(self.level*15)
    def create_bloks(self,count): # loob uusi blokke
        for i in range(count):
            if(random.randint(1,3) > 1): # yks kolmele et tuleb ull blokk
                temp = Blokk(self.blokityyp["tavaline"])
            else:
                temp = Blokk(self.blokityyp["lykkaja"])

            self.blokid.append(temp)

    def create_enemies(self,count): # loob uusi vastaseid
        for i in range(count):
            if(random.randint(1,5) > 1): # 20% et tulistaja
                temp = Enemy(self.enemytype["tavaline"])
            else:
                temp = Enemy(self.enemytype["tulistaja"])
            self.pahad.append(temp)

    def del_bloks(self):
        self.blokid = []

    def del_enemies(self):
        self.pahad = []

    def check_bullets(self): #
        for bullet in self.mees.bullets: # vaatame millega kuulid kokku porkavad :
            if not(rect_in_map(bullet.rect)): # kustutame kuuli kui see poel enam mapi piires.wd
                if(bullet in self.mees.bullets): # mingi lamp
                    self.mees.bullets.remove(bullet)
                    continue # kuul eemaldatud, ehk votame jargmise ette

            for blokk in self.blokid: # blokiga?
                if(collision(bullet.rect, blokk.rect)):
                    if(bullet in self.mees.bullets):
                        self.mees.bullets.remove(bullet) # kui jah siis kustutame kuuli.
                    break

            for enemy in self.pahad: # pahade poistega ?
                if(collision(bullet.rect, enemy.rect)):
                    if (enemy.getRekt(bullet.dmg)):
                        if("boss" in enemy.type):
                            miniBoss = Enemy(enemy.type.copy(),True,enemy.rect.x-enemy.rect.w/2,enemy.rect.y-enemy.rect.h/2)
                            miniBoss2 = Enemy(enemy.type.copy(),True,enemy.rect.x+enemy.rect.w/2,enemy.rect.y+enemy.rect.h/2)
                            print (miniBoss.rect.h)
                            if(miniBoss.rect.h > 10): # kontrollime et liiga mini poleks
                                self.pahad.append(miniBoss)
                                self.pahad.append(miniBoss2)
                            print (len(self.pahad))
                        self.pahad.remove(enemy)

                    if(bullet in self.mees.bullets): # mingi lamp
                        self.mees.bullets.remove(bullet)

        for enemy in self.pahad:

            if(enemy.shooter):

                for bullet in enemy.bullets:
                    if not(rect_in_map(bullet.rect)): # kui kuul mapist valjas
                        if(bullet in enemy.bullets):
                            enemy.bullets.remove(bullet)
                            continue

                    for blokk in self.blokid: # blokiga?
                        if(collision(bullet.rect, blokk.rect)):
                            if(bullet in enemy.bullets):
                                enemy.bullets.remove(bullet) # kui jah siis kustutame kuuli.
                                break

                    if(collision(bullet.rect,self.mees.rect)):
                        self.mees.getRekt(bullet.dmg)
                        enemy.bullets.remove(bullet) # kui jah siis kustutame kuuli.

    def draw_cursor(self): # joonistab hiire sihiku
        mouse = pygame.mouse.get_pos()
        self.mouseLineLen = 20
        self.mouseColor = (255,255,255)
        pygame.draw.line(self.screen,(self.mouseColor),(mouse[0]-self.mouseLineLen,mouse[1]),(mouse[0]+self.mouseLineLen,mouse[1]),2)
        pygame.draw.line(self.screen,(self.mouseColor),(mouse[0],mouse[1]+self.mouseLineLen),(mouse[0],mouse[1]-self.mouseLineLen),2)

    def generate_random_items(self):

        self.randomItemTimer.update() # uuendame timerit mis h2ndlib uute asjade loomist

        for item in self.randomItems: # uuendame asju maas
            item.update()
            if(item.end()):
                self.randomItems.remove(item)

        if(self.randomItemTimer.end == True): # kui aeg saab otsa loome uue asja
            temp = RandomItem(self.mees.relvad,self.mees.potid)
            self.randomItems.append(temp)
            self.randomItemTimer.reset_n(random.randint(2,self.levelTime*2)) # uus suvaline countdown
            self.randomItemTimer.reset()

    def man_item_collision(self):
        for item in self.randomItems:
            if(collision(self.mees.rect,item.rect)): # kokkuporge mingi asjaga
                if(self.mees.pickup(item)): # kui korjamine successful
                    if(item in self.randomItems): # korjame yles, kaotame maast
                        self.randomItems.remove(item)




game = Game(REAL_SCREEN_WIDTH,REAL_SCREEN_HEIGHT,SCREEN_WIDTH, SCREEN_HEIGHT) # peamaang
game.mees = Mees() # peavend

""" level 1 """
game.create_bloks(5) # viis vastast
game.create_enemies(20) # kaks vastast, viisakas
"""         """


while game.run == True: # main loop

    #uuendame taimereid
    game.levelTimer.update()
    for item in game.randomItems:
        item.timer.update()
    #EVENT
    for evt in pygame.event.get(): # koik eventid
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_RETURN:
                game.gaming = True
            if evt.key == pygame.K_m:
                if(game.music_playing == 1):
                    pygame.mixer.music.pause()
                    game.music_playing = -1
                else:
                    pygame.mixer.music.unpause()
                    game.music_playing = 1
            if not game.gaming: # 2rme vaata teisi evente kui m2ng ei k2i.
                continue
            if evt.key == pygame.K_p:
                game.levelTimer.pauseChange()
                game.randomItemTimer.pauseChange()
                for item in game.randomItems:
                    item.timer.pauseChange()
            elif evt.key == pygame.K_1:
                game.mees.switchWeapon(0)
            elif evt.key == pygame.K_2:
                game.mees.switchWeapon(1)
            elif evt.key == pygame.K_3:
                game.mees.switchWeapon(2)
            elif evt.key == pygame.K_4:
                game.mees.switchWeapon(3)
            elif evt.key == pygame.K_5:
                game.mees.switchWeapon(4)
            elif evt.key == pygame.K_6:
                game.mees.drinkPotion(0)
            elif evt.key == pygame.K_7:
                game.mees.drinkPotion(1)
        elif evt.type == pygame.QUIT: # kasutaja soovib lahkuda
            game.run = False
        elif evt.type == pygame.MOUSEBUTTONDOWN:
            if(game.levelTimer.paused == -1): # kui mang pole pausitud
                if (pygame.mouse.get_pressed()[0] == 1): # kui vasakut hiireklahvi vajutatakse.
                    game.mees.shoot((game.mees.rect.x,game.mees.rect.y),pygame.mouse.get_pos(),pygame.mouse.get_pressed())
                    game.mouseHolding = True
        elif evt.type == pygame.MOUSEBUTTONUP:
            if(game.levelTimer.paused == -1):
                game.mouseHolding = False
        
    if(game.levelTimer.paused != 1 and game.gaming): # kui m2ng pausitud voi avaekraanil, ei tee midagi

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

