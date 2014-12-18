from object_functions import *
from timer import Timer
from variables import *
import random, pygame

class Laser():

    global SCREEN_WIDTH, SCREEN_HEIGHT

    def __init__(self,speed,dmg=2):

        self.LaserSound = pygame.mixer.Sound("Sounds/laser2.wav")
        self.LaserSound.set_volume(0.8)
        self.chan1 = pygame.mixer.find_channel()

        self.delay = Timer(speed)
        self.wait = Timer(1) # reageerimisaeg
        self.type = random
        self.random_crd()

        self.dmg = dmg

        self.colorWait = (255,0,255)
        self.colorReady = (255,0,0)

        self.initWait = False
        self.dmgTime = 0
        self.delay.run()

    def update_logic(self):
        self.delay.update()
        self.wait.update()
    def show(self,scr):
        if(self.delay.end): # kui aeg lasta
            

            if(self.wait.running == False and self.initWait == False): # delay l'bi, k2ivitame laser
                self.wait.run()
                self.initWait = True

            if(self.wait.end): # laseme

                pygame.draw.rect(scr,self.colorReady,self.rect.get())
                if(self.dmgTime == 0):
                    self.dmgTime = pygame.time.get_ticks()
                    self.chan1.play(self.LaserSound)
                else:
                    if(pygame.time.get_ticks() -self.dmgTime > 500):
                        self.bye() # aeg t'is, aeg minna
            else: # naitame et kohe lastakse

                pygame.draw.rect(scr,self.colorWait,self.rect.get())
    def bye(self):
        self.initWait = False
        self.delay.reset()
        self.wait.reset()
        self.dmgTime = 0
        self.random_crd()

    def random_crd(self):
        self.suurus = 5

        if(random.randint(1,2) == 1): # horisontaalne laser
            self.x = 0
            self.y = crd_in_y()
            self.h = self.suurus
            self.w = SCREEN_WIDTH
        else:
            self.y = 0
            self.x = crd_in_x()
            self.h = SCREEN_HEIGHT
            self.w = self.suurus

        self.rect = Rect(self.x,self.y,self.w,self.h)
