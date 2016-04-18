import pygame
import random
from room_generator import *

class world:
    def __init__(self,rooms,level,texture,gamesize):
        
        builder = roomGen(gamesize,level,texture)
        self.room_cap=rooms
        self.rooms=[]
        i=1
        self.rooms.append(builder.generate(3,0))
        while (i<self.room_cap):#- ta treasure rooms pou t ftiaxnume apo kato
            self.rooms.append(builder.generate(2,i))
            i=i+1
        while (i<self.room_cap):
            self.rooms.append(builder.generate(1,i))
            i=i+1
        self.connect()
        self.clean_up()

    def start(self):
        return self.rooms[0] 

    def connect(self):
        self.rooms.sort(reverse=True)
        open_set=[]
        i=0
        while(i<len(self.rooms[0].exits)):
            open_set.append(self.rooms[0].exits[i])
            i=i+1
        j=1
        step=1
        while(len(open_set)>0):
            i=0
            flag=False
            while(i<len(self.rooms[j].exits)):
                k=0
                while(k<len(open_set)):
                    if(self.compatible(self.rooms[j].exits[i])==open_set[k].wall):
                        if self.link(self.rooms[j].exits[i],open_set[k])==False:
                            k=k+1
                            continue
                        open_set.pop(k)
                        if (j==1):
                            if(k==0):
                                self.rooms[0].exits[0],self.rooms[0].exits[1]=self.rooms[0].exits[1],self.rooms[0].exits[0]
                            open_set.pop(0)
                        flag=True
                        #swap paei proti i porta afti
                        self.rooms[j].exits[0],self.rooms[j].exits[i]=self.rooms[j].exits[i],self.rooms[j].exits[0]
                        k=1
                        while(k<len(self.rooms[j].exits)):
                            open_set.append(self.rooms[j].exits[k])
                            k=k+1
                        break
                    k=k+1
                if (flag):
                    break
                else:
                    i=i+1
            if (flag):
                j=j+1
                step=1
                if(j>=len(self.rooms)):
                    break
            else:
                if(j+step>=len(self.rooms)):
                    break
                self.rooms[j],self.rooms[j+step]=self.rooms[j+step],self.rooms[j]
                step=step+1

    def clean_up(self):
        i=0
        while(i<len(self.rooms)):
            j=0
            if(i==0):
                j=1
            while(j<len(self.rooms[i].exits)):
                if(self.rooms[i].exits[j].link)==None:
                    self.rooms[i].exits.pop(j)
                    continue
                j=j+1
            i=i+1
    
    def compatible(self,door):
        if(door.wall==1):
            return 2
        elif(door.wall==2):
            return 1
        elif(door.wall==3):
            return 4
        elif(door.wall==4):
            return 3
        else:
            return Null
        
    def link(self,door1,door2):
        if(door1.link==None) and(door2.link==None):
            door1.link=door2
            door2.link=door1
            return True
        else:
            return False

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((768,768))
    from data import *
    load_resources()
    flav = [None,None,None,None,None,None,None,None,None,None,None,None]
    i = 0
    while i<1000:
        print i
        kosmos = world(3,1,wflavours[0],(768,768))
        roomhead = kosmos.start()
        i = i + 1
    pygame.quit()
    exit()
