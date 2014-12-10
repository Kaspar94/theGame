from object_functions import *
import random, pygame
from variables import *
class Blokk(object): # tyypiline takistus
    global SCREEN_HEIGHT
    def __init__(self,tyyp):

        self.dx = 0
        self.dy = 0

        if(random.randint(1,2) == 1):
            # hakkab liikuma horisontaalselt
            self.dx = random.uniform(0.1,tyyp["maxKiirus"])
            self.suund = "hor"
        else:
            # hakkab liikuma vertikaalselt
            self.dy = random.uniform(0.1,tyyp["maxKiirus"])
            self.suund = "ver" # suund horisont.

        self.lykkab = tyyp["lykkab"]
        self.dmg = tyyp["dmg"]
        self.image = pygame.image.load(tyyp["img"]).convert()
        self.rect = Rect(0,0,0,0) # loome ymbrise
        self.w = self.image.get_rect()[2]
        self.h = self.image.get_rect()[3]
        self.new_crds()
        self.new_shape()
    def update_logic(self):

        if (((self.suund == "hor") and (self.rect.x+self.rect.w < 0 and self.dx < 0 or self.rect.x-self.rect.w > SCREEN_WIDTH  and self.dx > 0))\
            or (self.suund == "ver") and (self.rect.y+self.rect.h < 0 and self.dy < 0 or self.rect.y-self.rect.h > SCREEN_HEIGHT and self.dy > 0)):
                # kui kast jookseb valja mapist
            self.new_crds()
            self.new_shape()

        self.rect.x += self.dx
        self.rect.y += self.dy

    def show(self, scr): # n2itab
        if(rect_in_map(self.rect)): # kontrollime kas objekt mapi sees et mitte teha asjatuid joonistamisi.
            scr.blit(self.image, self.rect.get())

    def new_shape(self): # loob uue kuju blokile
        self.rect.w = self.w
        self.rect.h = self.h
        if(self.lykkab > 0):
            """
            lykkavad blokid on peeniksed aga pikad.
            seega kui blokk liigub vertikaalselt peame ara vahetama
            """
            if(self.dy != 0): # vaatame kas liigub vertikaalselt
                self.rect.w = self.h
                self.rect.h = self.w

    def new_crds(self):
        if(self.suund == "hor"): # loome koordinaaid horisontaalselt liikumiseks

            self.rect.x = crd_out_x(200) # votame suvad koordinaadid
            self.rect.y = crd_in_y()

            if(self.rect.x > 0): # kui kast paremal pool:
                self.dx = -self.dx # liigume vasakule mitte paremale
        else: # loome koordinaadid vertikaalselt liitkumiseks
            self.rect.x = crd_in_x()
            self.rect.y = crd_out_y(200)
            if(self.rect.y > 0):
                self.dy = -self.dy # liigume seljuhul alla.

    def disappear(self): # muutub nahtamatuks veits ajaks.
        pass