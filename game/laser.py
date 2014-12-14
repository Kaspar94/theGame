from object_functions import *
from timer import Timer
import random

class Laser():
    def __init__(self,speed):
        self.delay = Timer(speed)
        self.wait = Timer(1)
        self.type = random

    def update(self):
        pass
    def show(self):
        pass
