import random
import pygame
from projectile import *
class entity():

    def __init__(self, x, y, image, passable=False):
        self.x = x
        self.y = y
        if not type(image) is type(list()):
            self.text = [image]
        else:
            self.text = image
        self.orient = 0
        self.rect = pygame.Rect((x,y),(self.text[0].get_width(),self.text[0].get_height()))
        self.passable = passable
        
    def look(self, direc):
        self.orient = direc

    def look(self, x, y):
        if x==0:
            if y==1:
                self.orient = 4
            elif y==-1:
                self.orient = 0
        elif x==1:
            if y==1:
                self.orient = 3
            elif y==0:
                self.orient = 2
            else:
                self.orient = 1
        else:
            if y==1:
                self.orient = 5
            elif y==0:
                self.orient = 6
            else:
                self.orient = 7
    def getText(self):
        return self.text[self.orient]

class unit(entity):

    def __init__(self, x, y, image,items,health,speed):
        entity.__init__(self,x,y,image)
        self.prevrect = self.rect.copy()
        self.inv = {"main":None,"off":None,"head":None,"torso":None,"legs":None,"feet":None,'arms':None}
        self.movex = 0
        self.movey = 0
        self.items=items
        self.isDead = False
        self.mhp = health
        self.hp = self.mhp
        self.basehp = health
        self.speed = speed
        self.melee = True
        self.dmg = 0
        self.bullet = None
        self.attackspeed = 0
        self.attacktimer = 0
        self.casttimer = 0
        self.framerate = 60
        self.skills = [None,None,None,None,None]

    def move(self, x=0, y=0):
        self.prevrect = self.rect.copy()
        self.x = self.x + x*self.speed
        self.rect.x = self.x
        self.y = self.y + y*self.speed
        self.rect.y = self.y
        #self.rect.move_ip(x*self.speed,y*self.speed)
        return

    def rollback(self):
        self.rect = self.prevrect
        self.x = self.rect.x
        self.y = self.rect.y
        return

    def attack(self, target):
        if self.attacktimer <= 0 and self.casttimer<=0:
            self.attacktimer = self.framerate*self.attackspeed
            if self.inv["main"] is None:
                return ["noWeapon"]
            if self.melee:
                pass
            else:
                tempx = target[0] - self.rect.x
                tempy = target[1] - self.rect.y
                if tempx != 0:
                    tempx = tempx/abs(tempx)
                if tempy != 0:
                    tempy = tempy/abs(tempy)
                self.look(tempx,tempy)
                                                        #Weapon rect kanonika.
                return ["projectile",projectile(target,(self.rect.x,self.rect.y),self.bullet,self,self.dmg,self.speed+0.5)]
        return [self.attacktimer]

    def cast(self, num, target):
        if self.skills[num] is None:
            return "NoSkill"
        if self.skills[num].onCD():
            return "CD"
        else:
            stat = self.skills[num].cast()
            if self.skills[num].effect == "heal":
                self.hp += stat
                if self.hp >self.mhp:
                    self.hp = self.mhp
                return "Done"
            elif self.skills[num].effect == "skillshot":
                return ["projectile",projectile(target,(self.rect.x,self.rect.y),self.skills[num].image,self,stat,self.speed+self.skills[num].speed)]
            self.casttimer = 20
        

    def tick(self):
        if self.attacktimer>0:
            self.attacktimer -= 1
        if self.casttimer>0:
            self.casttimer -= 1
        for i in self.skills:
            if not i is None:
                i.tick()
            

    def equip(self, gear, slot):
        if (isinstance(gear,weapon) and slot in ["main","off"]) or ((isinstance(gear,armor) and slot in ["head","torso","arms","legs","feet"]) and gear.slot == slot):
            self.inv[slot] = gear
            self.reevaluate()
        else:
            print "Can't do that"
               
    def reevaluate(self):
        self.mhp = self.basehp
        self.hp = min(self.mhp,self.hp)
        if not self.inv["main"] is None:
            self.bullet = self.inv["main"].bullet
            self.melee = self.inv["main"].melee
            self.dmg = self.inv["main"].dmg
            self.attackspeed = self.inv["main"].attsp
        for i in ["head","torso","arms","legs","feet"]:
            if not self.inv[i] is None:
                self.mhp+=self.inv[i].defense
                self.hp += self.inv[i].defense

    def hurt(self, source):
        self.hp = self.hp - source.dmg
        if self.hp<=0:
            self.die()

    def die(self):
        self.isDead = True

    def AI(self):
        pass

class unit_prototype():
    def __init__(self,name,image,life,speed,rates,enviroment):
        self.name=name
        self.hp=life
        self.speed=speed
        self.image=image
        self.rates=rates
        self.enviroment=enviroment
        

    def create(self,x,y):
        items=['main','off','head','torso','legs','feet','arms']
        i=0
        while(i<7):
            temp=random.randint(0,100)
            if(temp>self.rates[i]):
                items[i]=False
            i=i+1
        
        return unit(x,y,self.image,items,self.hp,self.speed)

class weapon():

    def __init__(self, image, bullet, dmg, attsp, imagedis, name):
        self.name = name
        self.text = image
        self.image = imagedis
        self.bullet = bullet
        self.melee = False
        if bullet is None:
            self.melee = True
        self.dmg = dmg
        self.attsp = attsp

    def getText(self):
        return self.text

class weapon_prototype():
    def __init__(self, image, bullet, dmg, attsp, imagedis, name = "dummy"):
	self.name = name
	self.text = image
	self.image = imagedis
	self.bullet = bullet
	self.dmg = dmg
	self.attsp = attsp
	self.melee = False
	if bullet is None:
	    self.melee = True
		
    def create(self, level = 1):
	dmg = random.randint(self.dmg[0],self.dmg[1])
	attsp = float(random.randint(self.attsp[0]*100,self.attsp[1]*100))/100
	return weapon(self.text,self.bullet,dmg,attsp,self.image,self.name)

class armor_prototype():
    def __init__(self, image, defense, durability, slot, imagedis, name = "dummy"):
	self.name = name
	self.text = image
	self.image = imagedis
	self.defense = defense
	self.durability = durability
	self.slot = slot
		
    def create(self, level = 1):
	durability = random.randint(self.durability[0],self.durability[1])
	defense = random.randint(self.defense[0],self.defense[1])
	return armor(self.text,defense, durability, self.slot, self.image, self.name)

class armor():

    def __init__(self, image, defense, durability, slot, imagedis, name = "dummy"):
        self.text = image
        self.image = imagedis
        self.defense = defense
        self.durab = durability
        self.slot = slot

    def getText(self):
        return self.text

class triggerable(entity):
    
    def __init__(self, x, y, image):
        entity.__init__(self,x,y,image)
        self.prevrect = self.rect.copy()
        self.isDead = False

    def live(self):
        self.framerate = 60

    def AI(self):
        pass

    def tick(self):
        pass

    def die(self):
        self.isDead = True

    def hurt(self, source=None):
        pass

class players(unit):

    def __init__(self, x, y, image,hp,speed):
       unit.__init__(self,x,y,image,[],hp,speed)
       
       self.stash = []

    def customize(self, race, righthanded):
        self.rhanded = righthanded
        self.race = race

    def equip(self, gear, slot):
        if (isinstance(gear,weapon) and slot in ["main","off"]) or ((isinstance(gear,armor) and slot in ["head","torso","arms","legs","feet"]) and gear.slot == slot):
            if not self.inv[slot] is None:
                self.stash.append(self.inv[slot])
            self.inv[slot] = gear
            self.reevaluate()
        else:
            print "Can't do that"
            
    def reevaluate(self):
        self.mhp = self.basehp
        self.hp = min(self.mhp,self.hp)
        if not self.inv["main"] is None:
            self.bullet = self.inv["main"].bullet
            self.melee = self.inv["main"].melee
            self.dmg = self.inv["main"].dmg
            self.attackspeed = self.inv["main"].attsp
        for i in ["head","torso","arms","legs","feet"]:
            if not self.inv[i] is None:
                self.mhp+=self.inv[i].defense
            
            

class door(entity):
    def __init__(self,room,porta,wall,x,y,image):
        entity.__init__(self,x,y,image)
        self.x=x
        self.y=y
        self.wall=wall #1:left,2:right,3:top,4:bot
        self.room=room
        self.link=porta
        self.active = False

    def getText(self):
        if self.active:
            return self.text[1]
        return self.text[0]

class skill():

    def __init__(self, effect, stat, cooldown, image, speed = -1):
        self.effect = effect
        self.image = image
        self.stat = stat
        self.speed = speed
        self.cooldown = cooldown
        self.currcd = 0

    def onCD(self):
        if self.currcd>0:
            return True
        return False

    def tick(self):
        if self.currcd>0:
            self.currcd -= 1

    def cast(self):
        self.currcd = self.cooldown
        return random.randint(self.stat[0],self.stat[1])
            
