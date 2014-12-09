import pygame,math
class Timer:
    global pause
    def __init__(self, countdown):
        self.paused = -1
        self.c = countdown*1000 # muudame sekundid millisekunditeks
        self.reset()
    def update(self):
        if(self.running == True):
            if(self.paused == -1): # pole pausil
                if(self.pauseStart != 0):
                    self.pauseTime += pygame.time.get_ticks()-self.pauseStart
                    self.pauseStart = 0
                if(pygame.time.get_ticks() - self.start >= self.c+self.pauseTime): # END
                    self.running = False
                    self.end = True
            elif(self.paused == 1):
                if(self.pauseStart == 0):
                    self.pauseStart = pygame.time.get_ticks()
    def pauseChange(self):
        self.paused = -self.paused
    def run(self):
        self.running = True
    def reset_n(self,n):
        self.c = n*1000
    def reset(self):
        self.start = pygame.time.get_ticks()        
        self.running = True
        self.pauseStart = 0
        self.pauseStop = 0
        self.pauseTime = 0
        self.end = False

    def get_secs(self):
        return math.floor(((self.c+self.pauseTime)-(pygame.time.get_ticks() - self.start))/1000)
