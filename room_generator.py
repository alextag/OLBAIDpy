import random
import pygame
from hephaestus import *
from entity import *
from Astar import *
from data import enemies,armors,weapons

class room():
    def __init__(self, units, entities,exits,triggerables,eidos,width,height,exlist,aa):
        self.aa = aa #aukson arithmos
        self.triggerables=triggerables
        self.units= units
        self.entities= entities
        self.exits=exits
        self.eidos=eidos
        self.width = width
        self.height = height
        self.exlist = exlist
        self.neigh = []
        

    def __gt__(self, node):
        if self.eidos>node.eidos:
            return True
        elif self.eidos==node.eidos:
            return len(self.exits)>len(node.exits)
        else:
            return False

    def __lt__(self, node):
        if self.eidos<node.eidos:
            return True
        elif self.eidos==node.eidos:
            return len(self.exits)<len(node.exits)
        else:
            return False

    def __eq__(self,node):
        return (len(self.doors)==len(node.doors))*(self.eidos==node.eidos)

class roomGen():

    def __init__(self, size, level, textures):
        self.level=level
        self.size = (size[0]/16,size[1]/16)
        self.walltext = textures[7]
        self.doortext = [textures[3],textures[4]]
        self.traptext = textures[5]
        self.chesttext = textures[6]
        self.armorer = smith(textures[-1],level)
        
        
    def generate(self, eidos, aa):#1:treasure room,2:room,3: starting room
        pos = []
        entities = []
        triggerables=[]
        units = []
        
        if eidos==3:
            width=random.randint(8,10)
            height=random.randint(8,10)
            exits=4
            monster_cap=0
            trap_cap=random.randint(0,self.level/5)
            obstacle_cap=random.randint(4,8)
        else:
            width=random.randint(8,16)
            height=random.randint(8,16)
            area=width*height
            if (area<=81):
                exits=random.randint(1,4)
                monster_cap=random.randint(2,3)
                trap_cap=random.randint(0,2)
                obstacle_cap=random.randint(4,8)
            elif (area<121):
                exits=random.randint(1,5)
                monster_cap=random.randint(2,4)
                trap_cap=random.randint(0,3)
                obstacle_cap=random.randint(5,10)
            elif (area<169):
                exits=random.randint(1,6)
                monster_cap=random.randint(3,6)
                trap_cap=random.randint(0,4)
                obstacle_cap=random.randint(8,14)
            else:
                exits=random.randint(1,8)
                monster_cap=random.randint(4,8)
                trap_cap=random.randint(1,6)
                obstacle_cap=random.randint(10,18)
            if eidos==1:
                chest_cap=random.randint(self.level-2,self.level-1)
                
        i=1
        while(i<width-1):
                j=1
                while(j<height-1):
                    pos.append((i,j))
                    j=j+1
                i=i+1
                
        exits_list=[]
        exlist=[]
        exposx=[]
        exposy=[]
        
        i=2
        while(i<width-2):
            exposx.append(i)
            i=i+2
        i=1
        while(i<height-1):
            exposy.append(i)
            i=i+2
        i=0

        wall=0
        walll=[1,2,3,4]
        while (i<exits):
            if (eidos==3):
                wall=wall+1
            else:
                wall=random.choice(walll)
            if wall==1:
                x=0
                if len(exposy)==0:
                    walll.pop(walll.index(1))
                    continue
                y=random.choice(exposy)
                exposy.pop(exposy.index(y))
            elif wall==2:
                x=width-1
                if len(exposy)==0:
                    walll.pop(walll.index(2))
                    continue
                y=random.choice(exposy)
                exposy.pop(exposy.index(y))
            elif wall==3:
                if len(exposx)==0:
                    walll.pop(walll.index(3))
                    continue
                x=random.choice(exposx)
                y=0
                exposx.pop(exposx.index(x))
            elif wall==4:
                if len(exposx)==0:
                    walll.pop(walll.index(4))
                    continue
                x=random.choice(exposx)
                y=height-1
                exposx.pop(exposx.index(x))
            exits_list.append(door(aa,None,wall,x*self.size[0],y*self.size[1],self.doortext))
            exlist.append((x*self.size[0],y*self.size[1]))
            
            i=i+1
        test_map=[]
        i=0
        while(i<width):
            j=0
            tempidi=[]
            while(j<height):
                tempidi.append(True)
                j=j+1
            test_map.append(tempidi)
            i=i+1
        i=0
        while(i<obstacle_cap):
            (x,y)=random.choice(pos)
            test_map[x][y]=False
           
            j=1
            p=0
            while j<exits:
                if Astar((exits_list[0].x/self.size[0],exits_list[0].y/self.size[1]),(exits_list[j].x/self.size[0],exits_list[j].y/self.size[1]),test_map):
                    j=j+1
                    continue
                p=p+1
                test_map[x][y]=True
                if(p==5):
                    break
                (x,y)=random.choice(pos)
                test_map[x][y]=False
                j=1
            if(p==5):
                i=i+1
                continue
            pos.pop(pos.index((x,y)))
            entities.append(entity(x*self.size[0],y*self.size[1],self.walltext))
            i=i+1
        i=0
        while(i<trap_cap):
            (x,y)=random.choice(pos)
            pos.pop(pos.index((x,y)))
            triggerables.append(triggerable(x*self.size[0],y*self.size[1],self.traptext))
            i=i+1
        i=0
        ref=['head','torso','legs','feet','arms']
        while(i<monster_cap):
            (x,y)=random.choice(pos)
            pos.pop(pos.index((x,y)))

            j=random.randint(0,len(enemies)-1)                
            units.append(enemies[j].create(x*self.size[0],y*self.size[1]))
            k=0
            while(k<2):
                k=k+1
            while(k<7):
                if(units[-1].items[k]):
                    units[-1].equip(self.armorer.generate_a(units[-1].items[k]),units[-1].items[k])
                k=k+1
            i=i+1
        if eidos==1:
            i=0
            while(i<chest_cap):
                (x,y)=random.choice(pos)
                pos.pop(pos.index((x,y)))
                units.append(triggerable(x*self.size[0],y*self.size[1],self.chesttext))
                i=i+1

        temp = room(units,entities,exits_list,triggerables,eidos,width,height,exlist,aa)
        for i in range(len(temp.exits)):
            temp.exits[i].room = temp
            
        return temp


if __name__=='__main__':
    new = roomGen((1024,768),1)
    temp = new.generate(2)
    print temp
