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
from laser import Laser
from laine import Laine

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
        self.welcomeScreen = pygame.image.load('Pics/gameAvaekraan4.png').convert()
        self.statboard = pygame.image.load("Pics/statboard3.png").convert()
        self.pauseScreen = pygame.image.load('Pics/paused.png').convert_alpha()
        self.speedpot = pygame.image.load("Pics/speedpot.png").convert_alpha()
        self.hppot2 = pygame.image.load("Pics/2HPpot.png").convert_alpha()
        self.hppot5 = pygame.image.load("Pics/5HPpot.png").convert_alpha()
        self.background = pygame.transform.scale((pygame.image.load("Pics/spacev3.png").convert()), (1024,768))
        self.bg_imgRect = self.background.get_rect()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load('Sounds/track1_track2.mp3') # <--------------------------------------------------------- SIIN TAUSTAMUSS
        pygame.mixer.music.play(-1)  # maitu korda m'ngib
        self.music_playing = 1
        self.play_sounds = 1
        """
        kiirus - bloki kiirusW
        maxw - maksimaalne laius
        maxh - maksimaaline pikkus
        lykkab - mitu pixlit lykkab eemale kokkuporkel
        dmg - mitu dmg teeb lykkamisega
        """

        self.blokityyp = {
            "tavaline" : {
                "maxKiirus" : 0.2, # bloki maksimaalne kiirus
                "lykkab" : 0, # lykkamistugevus
                "dmg" : 0, # dmg kokkuporkel
                "img" : "Pics/tavalineblokkBlurred.png"
            },
            "lykkaja" : {
                "maxKiirus" : 0.5,
                "lykkab" : 200,
                "dmg" : 2,
                "img" : "Pics/lykkajablokkBlurred.png"
            }


        }
        self.enemytype = {
            "tavaline" : {
                "elusi" : 1,
                "img" : "Pics/tavalinevastane30x30.png",
                "speed" : 0.1,
                "dmg" : 1
            },
            "tulistaja" : {
                "elusi" : 2,
                "img" : "Pics/tulistajavastane40x40_2.png",
                "speed" : 0.05,
                "dmg" : 2,
                "weapon" : 1,
                "delay" : 1
            },
            "boss" : {
                "boss" : 1,
                "elusi" : 10,
                "img" : "Pics/boss.png",
                "speed" : 0.1,
                "dmg" : 1000,
                "weapon" : 1,
                "delay" : 1
            }
        }

        self.blokid = []
        self.pahad = []
        self.laserid = []
        self.lained = []

        pygame.font.get_fonts()
        self.font=pygame.font.SysFont('bauhaus93',35)


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

        self.linex = 300
        self.linexDx = 1

    def update_logic(self):

        if not self.gaming:
            return

        self.generate_random_items()


        self.mees.update_logic() # uuendab meest

        if(self.mouseHolding): # kui hiirt hoitakse all->automaatne tulistamine
            self.mees.automatic()

        for laser in self.laserid:
            laser.update_logic()

            if(collision(laser.rect,self.mees.rect) and laser.wait.end == True and laser.delay.end == True): # kui mees saab laserit
                self.mees.getRekt(laser.dmg) # mees saab dmg
                laser.bye()

        for laine in self.lained:
            laine.update_logic()

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

            for laser in self.laserid:
                laser.show(self.screen,self.play_sounds)

            for item in self.randomItems: #joonistame maas olevaid boonus asju
                item.show(self.screen)

            for laine in self.lained:
                laine.show(self.screen)

            self.draw_text()

            if(self.levelTimer.paused == 1): # m2ng pausitud, n2itame pausi pilti
                self.screen.blit(self.pauseScreen,(0,0))
        else:
            self.screen.blit(self.welcomeScreen,(0,0))
            self.linex += self.linexDx
            if(self.linex > 650 or self.linex < 210):
                self.linexDx = -self.linexDx
            pygame.draw.rect(self.screen,(0,255,0),(self.linex,550,100,2))

        self.draw_cursor()
        pygame.display.flip()

    def draw_text(self):
        self.screen.blit(self.statboard, (0,620))
        scoretext=self.font.render(str(self.level), 1,(20,250,20))
        self.screen.blit(scoretext, (471, 639))
        scoretext2=self.font.render(str(self.levelTimer.get_secs()), 1,(20,250,20))
        self.screen.blit(scoretext2, (550, 702))
        for i,slot in enumerate(self.mees.relvakogu):
            if(game.mees.relv==slot):
                self.slotColor = (20,200,20)
            else:
                self.slotColor = (0,0,0)
            self.slots = self.font.render(str(i+1)+" "+str(slot), 1,self.slotColor)
            self.screen.blit(self.slots, (700+i*100,642))
        for i,slot in enumerate(self.mees.potikogu):
            if(slot == 0):
                self.screen.blit(self.hppot2,(200+i*100,707))
            elif(slot == 1):
                self.screen.blit(self.hppot5,(200+i*100,707))
            elif(slot == 2):
                self.screen.blit(self.speedpot,(200+i*100,707))
            self.slots = self.font.render(str(i+6), 1,(50,0,0))
            self.screen.blit(self.slots, (200+i*100,698))
        if(game.mees.relv != "handgun"):
            bulletsNow = str(self.mees.relvad[self.mees.relv]["bullets"])
            bulletsTotal = str(self.mees.relvad[self.mees.relv]["kokku"])
        else:
            bulletsNow = "-"
            bulletsTotal = "-"

        scoretext=self.font.render(bulletsNow+"/"+bulletsTotal, 1,(20,250,20))
        if(self.mees.lives < 3):
            self.livesColor = (255,0,0)
        elif(self.mees.lives >= 3 and self.mees.lives < 5):
            self.livesColor = (255,128,0)
        else:
            self.livesColor = (0,255,0)
        scoretext2=self.font.render(str(self.mees.lives),1,self.livesColor)
        self.screen.blit(scoretext, (833, self.height+83))
        self.screen.blit(scoretext2, (175, self.height+21))

        #pygame.draw.rect(self.screen,(250,125,125),(0,self.height+10,self.width,self.realheight-self.height))

    def Level(self): # h2ndlib leveleid
        if(self.levelTimer.end == True):
            if(self.bossInit == False):
                self.del_bloks()
                self.del_enemies()
                boss = Enemy(self.enemytype["boss"],True,w=self.level*25,h=self.level*25)
                boss.elusi = (self.level*3)
                self.pahad.append(boss)
                self.bossInit = True
                self.create_lasers(2*self.level)
                game.mees.speed += 0.2
            else:
                if(len(self.pahad) == 0):
                    self.bossInit = False
                    self.levelTimer.reset()
                    self.del_lasers()
                    self.next_level()

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
                temp.elusi = random.randint(1,self.level)
            else:
                temp = Enemy(self.enemytype["tulistaja"])
                temp.elusi = random.randint(2,self.level*2)
            if(random.randint(1,5) > 3):
                temp.poiklemine = 1
            self.pahad.append(temp)

    def create_lasers(self,count):
        for i in range(count):
            temp = Laser(random.randint(2,self.level*8))
            self.laserid.append(temp)

    def del_bloks(self):
        self.blokid = []

    def del_enemies(self):
        self.pahad = []

    def del_lasers(self):
        self.laserid = []

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
                            try:  # viskab mingi errori non-integer stop for randrange(). Ei oska muudmoodi lahendada :(
                                miniBoss = Enemy(enemy.type,True,enemy.rect.x+random.randint(0,enemy.rect.w),enemy.rect.y,enemy.rect.w/2,enemy.rect.h/2)
                                miniBoss2 = Enemy(enemy.type,True,enemy.rect.x+random.randint(0,enemy.rect.w),enemy.rect.y+enemy.rect.h,enemy.rect.w/2,enemy.rect.h/2)
                                miniBoss.elusi,miniBoss2.elusi = (self.level*3),(self.level*3)
                                if(miniBoss.rect.h > 10): # kontrollime et liiga mini poleks
                                    self.pahad.append(miniBoss)
                                    self.pahad.append(miniBoss2)
                            except Exception as e:
                                print (e)
                        self.pahad.remove(enemy)

                    if(bullet in self.mees.bullets): # mingi lamp
                        self.mees.bullets.remove(bullet)

        for enemy in self.pahad:

            if(enemy.shooter):

                for bullet in enemy.bullets:
                    if not(rect_in_map(bullet.rect)): # kui kuul mapist valjas, kaotame
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
            self.randomItemTimer.reset_n(random.randint(10,self.levelTime*2)) # uus suvaline countdown
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
game.create_bloks(0) # viis vastast
game.create_enemies(0) # kaks vastast, viisakas
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

            if evt.key == pygame.K_n:
                game.play_sounds = -game.play_sounds
                if(game.play_sounds > 0):
                    game.mees.saund.set_volume(0.2)
                    game.mees.saund2.set_volume(0.2)
                    game.mees.saund3.set_volume(0.2)
                else:
                    game.mees.saund.set_volume(0)
                    game.mees.saund2.set_volume(0)
                    game.mees.saund3.set_volume(0)

            if not game.gaming: # 2rme vaata teisi evente kui m2ng ei k2i.
                continue

            if evt.key == pygame.K_p:
                game.levelTimer.pauseChange()
                game.randomItemTimer.pauseChange()
                game.mees.speedTimer.pauseChange()
                for item in game.randomItems:
                    item.timer.pauseChange()
                for laser in game.laserid:
                    laser.wait.pauseChange()
                    laser.delay.pauseChange()

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
                    if not ("vahe" in game.mees.relvad[game.mees.relv]): # kui on automaat siis hakkab ise tulistama
                        game.mees.shoot((game.mees.rect.x,game.mees.rect.y),pygame.mouse.get_pos(),pygame.mouse.get_pressed())
                    game.mouseHolding = True
                    game.lained = []
                elif(pygame.mouse.get_pressed()[2] == 1): # peavend saadab ulti v2lja
                    if(game.mees.laine()):
                        temp = Laine(game.mees.rect.x,game.mees.rect.y,pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                        game.lained.append(temp)

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

