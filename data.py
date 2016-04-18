import pygame
from entity import weapon_prototype,armor_prototype,unit_prototype
ptext = []
wflavours = []
weapons = []
enemies = []
gui = []
armors = []
saveslots = [None,None,None,None]

def load_player():
    for each in [pygame.image.load("resources/pup.png").convert_alpha(),
             pygame.image.load("resources/pupright.png").convert_alpha(),
             pygame.image.load("resources/pright.png").convert_alpha(),
             pygame.image.load("resources/pdownright.png").convert_alpha(),
             pygame.image.load("resources/pdown.png").convert_alpha(),
             pygame.image.load("resources/pdownleft.png").convert_alpha(),
             pygame.image.load("resources/pleft.png").convert_alpha(),
             pygame.image.load("resources/pupleft.png").convert_alpha()
             ]:
        ptext.append(each)

def load_worlds():
    for each in [[pygame.image.load("resources/worlds/cave/world1.png").convert(),
                 pygame.image.load("resources/worlds/cave/wallv.png").convert(),
                 pygame.image.load("resources/worlds/cave/wallh.png").convert(),
                 pygame.image.load("resources/worlds/cave/door.png").convert_alpha(),
                  pygame.image.load("resources/worlds/cave/dooractive.png").convert_alpha(),
                  pygame.image.load("resources/worlds/cave/trap.png").convert_alpha(),
                  pygame.image.load("resources/worlds/cave/chest.png").convert_alpha(),
                  pygame.image.load("resources/worlds/cave/obstacle1.png").convert_alpha(),
                  ["cave"]],
                 [pygame.image.load("resources/worlds/forest/world1.png").convert(),
                 pygame.image.load("resources/worlds/forest/wallv.png").convert(),
                 pygame.image.load("resources/worlds/forest/wallh.png").convert(),
                 pygame.image.load("resources/worlds/forest/door.png").convert_alpha(),
                  pygame.image.load("resources/worlds/forest/dooractive.png").convert_alpha(),
                  pygame.image.load("resources/worlds/forest/trap.png").convert_alpha(),
                  pygame.image.load("resources/worlds/forest/chest.png").convert_alpha(),
                  pygame.image.load("resources/worlds/forest/obstacle1.png").convert_alpha(),
                  ["forest"]]
                 ]:
        wflavours.append(each)

def load_weapons():
    weapons.append(weapon_prototype(pygame.image.load("resources/sword.png").convert_alpha(),pygame.image.load("resources/bullet.png").convert_alpha(),[40,50],[0.4,0.5],pygame.image.load("resources/sworddis.png").convert_alpha()))
    weapons.append(weapon_prototype(pygame.image.load("resources/sword.png").convert_alpha(),None,[80,100],[0.4,0,4],pygame.image.load("resources/sworddis.png").convert_alpha()))

def load_armors():
    armors.append(armor_prototype(pygame.image.load("resources/sword.png").convert_alpha(),[0,100],[40,50],'head',pygame.image.load("resources/sworddis.png").convert_alpha()))
    armors.append(armor_prototype(pygame.image.load("resources/sword.png").convert_alpha(),[0,100],[40,50],'torso',pygame.image.load("resources/sworddis.png").convert_alpha()))
    armors.append(armor_prototype(pygame.image.load("resources/sword.png").convert_alpha(),[0,100],[40,50],'legs',pygame.image.load("resources/sworddis.png").convert_alpha()))
    armors.append(armor_prototype(pygame.image.load("resources/sword.png").convert_alpha(),[0,100],[40,50],'feet',pygame.image.load("resources/sworddis.png").convert_alpha()))
    armors.append(armor_prototype(pygame.image.load("resources/sword.png").convert_alpha(),[0,100],[40,50],'arms',pygame.image.load("resources/sworddis.png").convert_alpha()))

def load_enemies():
    enemies.append(unit_prototype('Goblin',pygame.image.load("resources/monsterc.png").convert_alpha(),120,1,[80,50,2,20,100,0,0],"cave"))
    enemies.append(unit_prototype('Animal',pygame.image.load("resources/monster.png").convert_alpha(),80,1,[0,0,0,0,0,0,0],"forest"))

def load_gui():
    gui.append(pygame.image.load("resources/inventory.png").convert_alpha())
    gui.append(pygame.image.load("resources/invslot.png").convert_alpha())

def load_saveslots():
    currslot = 0
    names = ["Bob","Bob","Bob","Bob"]
    working = [False,False,False,False]
    done = [False,False,False,False]
    levels = [1,1,1,1]
    gear = [[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]]
    fin = open("resources/data.txt")
    for line in fin:
        temp = line.split("<")
        for i in temp:
            temp2 = i.split(">")[0]
            temp2 = temp2.split(":")
            if temp2[0]=="slot":
                try:
                    currslot = int(temp2[1])
                    if done[currslot-1]:
                        working[currslot-1] = False
                    else:
                        working[currslot-1] = True
                        done[currslot-1] = True
                except ValueError:
                    currslot = 0
            elif currslot>0 and currslot<5 and working[currslot-1]:
                if temp2[0]=="name":
                    names[currslot-1] = temp2[1]
                elif temp2[0]=="level":
                    try:
                        levels[currslot-1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="main":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(weapons):
                        gear[currslot-1][0] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="off":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(weapons):
                        gear[currslot-1][1] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="head":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(armors):
                        gear[currslot-1][2] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="torso":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(armors):
                        gear[currslot-1][3] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="legs":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(armors):
                        gear[currslot-1][4] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="feet":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(armors):
                        gear[currslot-1][5] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                elif temp2[0]=="arms":
                    try:
                        temp2[1] = int(temp2[1])
                    except ValueError:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                    if temp2[1]>=-1 and temp2[1]<len(armors):
                        gear[currslot-1][6] = temp2[1]
                    else:
                        names[currslot-1] = "Corrupted"
                        working[currslot-1] = False
                #elif temp2[0]=="stash":
    pls = []
    for i in range(len(names)):
        pls.append([names[i],working[i],levels[i],gear[i]])
    return pls

def load_resources():
    load_player()
    load_worlds()
    load_weapons()
    load_armors()
    load_enemies()
    load_gui()
    return load_saveslots()

def resize_resources(screenh,screenw):
    nsize = min(int((screenh/16.0)),48)
    if nsize == 512:
        return
    for i in range(len(weapons)):
        #for each in weapons[i].text ...
        weapons[i].text = pygame.transform.scale(weapons[i].text,(int((nsize*weapons[i].text.get_width())/(float(ptext[0].get_width()))),int((nsize*weapons[i].text.get_height())/(float(ptext[0].get_width())))))
        sizex = int((screenw*weapons[i].image.get_width())/1920.0)
        weapons[i].image = pygame.transform.scale(weapons[i].image,(sizex,int((sizex*weapons[i].image.get_height())/float(weapons[i].image.get_width()))))
    for i in range(len(armors)):
        #for each in armors[i].text ...
        armors[i].text = pygame.transform.scale(armors[i].text,(int((nsize*armors[i].text.get_width())/(float(ptext[0].get_width()))),int((nsize*armors[i].text.get_height())/(float(ptext[0].get_width())))))
        sizex = int((screenw*armors[i].image.get_width())/1920.0)
        armors[i].image = pygame.transform.scale(armors[i].image,(sizex,int((sizex*armors[i].image.get_height())/float(armors[i].image.get_width()))))
    for i in range(len(ptext)):
        ptext[i] = pygame.transform.scale(ptext[i],(nsize-1,nsize-1))
    for each in range(len(wflavours)):
        for i in range(3,len(wflavours[each])-1):
            wflavours[each][i] = pygame.transform.scale(wflavours[each][i],(nsize,nsize))
    for i in range(len(enemies)):
        enemies[i].image = pygame.transform.scale(enemies[i].image,(nsize,nsize))
