import random
import pygame
from entity import weapon_prototype,armor_prototype
from data import armors,weapons

class smith:

    def __init__(self,enviroment,lvl):
        self.enviroment=enviroment
        self.level=lvl

    def generate_w(self):
        choice=random.choice(weapons)
        return choice.create()

        
    def generate_a(self):
        choice=random.choice(armors)
        return choice.create()

    def generate_a(self,slot):
        sub_set=[]
        i=0
        while(i<len(armors)):
            if(armors[i].slot==slot):
                sub_set.append(armors[i])
            i=i+1
        choice=random.choice(sub_set)
        return choice.create()
