from variables import *
import random
class Rect:
    """
    oma rect klass et oleks voimalik floate kasutada
    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def get(self):
        return (self.x, self.y, self.w, self.h)

    def set(self,crds): # satib uued koordinaaid n shit
        self.x,self.y,self.w,self.h=crds
    
def collision(rect1, rect2): # kontrollib kas kokkuporge
    if(rect1.x < rect2.x+rect2.w and rect1.x+rect1.w > rect2.x and \
       rect1.y < rect2.y+rect2.h and rect1.y+rect1.h > rect2.y):
        return True
    else:
        return False

def crd_out_y(range): # genereerib suvalise y koordinaadi mapist v2ljas arg. range raadiuses
    global SCREEN_HEIGHT
    yUD = random.randint(1,2)
    if(yUD == 1):
        y = random.randint(-range,0)
    else:
        y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT+range)
    return y

def crd_out_x(range): # genereerib suvalise x koordinaadi mapist v2ljas arg. range raadiuses
    global SCREEN_WIDTH
    xLR = random.randint(1,2)
    if(xLR == 1):
        x = random.randint(-range,0)
    else:
        x = random.randint(SCREEN_WIDTH,SCREEN_WIDTH+range)
    return x

def crd_in_x(): # genereerib suvalise x koordinaadi mapi sees
    global SCREEN_WIDTH
    return random.randint(0,SCREEN_WIDTH)

def crd_in_y(): # genereerib suvalise y koordinaadi mapi sees
    global SCREEN_HEIGHT
    return random.randint(0,SCREEN_HEIGHT)

def rect_in_map(rect): # tagastab true kui objekt asub mapis
    global SCREEN_HEIGHT,SCREEN_WIDTH
    if not(rect.x+rect.w < 0 or rect.x > SCREEN_WIDTH or rect.y > SCREEN_HEIGHT or rect.y+rect.h < 0):
        return True
    else:
        return False