import pygame
from pygame.locals import *
from sys import exit
from gui import *
from GEngine import *
from entity import *
from projectile import *
from room_generator import *
from world_generator import *
from data import *

class game():

    def __init__(self):
        pygame.init()
        (winsize,fullscr) = self.loadsettings()
        mouse_pressed = False

        #Determining window size
        winsizes = [(1024,768),(1280,1024),(1366,768),(1680,1050),(1920,1080)]
        if winsize not in [0,1,2,3,4]:
            winsize = 0
        self.screen_width = winsizes[winsize][0]
        self.screen_height = winsizes[winsize][1]
        windowsize = (self.screen_width, self.screen_height)

        #Rendering Main Menu
        textfont = pygame.font.SysFont("Arial",32)
        temp = textfont.render("Start",True,(255,255,255))
        self.butextures = [pygame.image.load("resources/unpressed.png"),pygame.image.load("resources/pressed.png"),
                      pygame.image.load("resources/hover.png")]
        startb = button(self.screen_width/2-60,self.screen_height/2-200,self.butextures)
        startb.setTxt(temp)
        exitb = button(self.screen_width/2-60,self.screen_height/2,self.butextures)
        temp = textfont.render("Exit",True,(255,255,255))
        exitb.setTxt(temp)

        
        mouse_pressed = False
        mousepos = [-1,-1]
        
        #Creating the game window
        if fullscr:
            self.screen = pygame.display.set_mode(windowsize,pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(windowsize)
        pygame.display.set_caption("OLBAID")
        pygame.display.set_icon(pygame.image.load("resources/olbaid.png"))

        #Main loop
        while 1:
            self.screen.fill((0,0,0))
            mousepos = pygame.mouse.get_pos()
            self.screen.blit(startb.getText(mouse_pressed,mousepos[0],mousepos[1]),startb.rect)
            self.screen.blit(exitb.getText(mouse_pressed,mousepos[0],mousepos[1]),exitb.rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT or ((event.type == KEYDOWN) and (event.key==K_ESCAPE)):
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False
                        if startb.getPressed():
                            self.gamemenu(windowsize)
                        if exitb.getPressed():
                            pygame.quit()
                            exit()

    def gamemenu(self, windowsize):
        textfont = pygame.font.SysFont("Arial",32)
        mouse_pressed = False
        pls = load_resources()
        resize_resources(self.screen_height,self.screen_width)
        posx = [((self.screen_width*0.25)-60),((self.screen_width*0.75)-60),((self.screen_width*0.25)-60),((self.screen_width*0.75)-60)]
        posy = [((self.screen_height*0.25)-200),((self.screen_height*0.25)-200),((self.screen_height*0.75)-200),((self.screen_height*0.75)-200)]
        self.butextures = [pygame.image.load("resources/unpressed.png"),pygame.image.load("resources/pressed.png"),
                      pygame.image.load("resources/hover.png")]
        plbuttons = []
        for i in range(len(pls)):
            if pls[i][1]:
                text = textfont.render(pls[i][0],True,(255,255,255))
                plbuttons.append(button(posx[i],posy[i],self.butextures))
                plbuttons[-1].setTxt(text)
            else:
                text = textfont.render("Empty",True,(255,255,255))
                plbuttons.append(button(posx[i],posy[i],[self.butextures[0],self.butextures[0],self.butextures[0]]))
                plbuttons[-1].setTxt(text)

        exitb = button(self.screen_width/2-60,self.screen_height-100,self.butextures)
        temp = textfont.render("Back",True,(255,255,255))
        exitb.setTxt(temp)

        while 1:
            self.screen.fill((0,0,0))
            mousepos = pygame.mouse.get_pos()
            for i in plbuttons:
                self.screen.blit(i.getText(mouse_pressed,mousepos[0],mousepos[1]),i.rect)
            self.screen.blit(exitb.getText(mouse_pressed,mousepos[0],mousepos[1]),exitb.rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False
                        if exitb.getPressed():
                            return
                        for i in range(len(plbuttons)):
                            if pls[i][1] and plbuttons[i].getPressed():
                                self.gamescreen(windowsize,pls[i])
                                #save
                                return

    def gamescreen(self,windowsize,pls):
        textfont = pygame.font.SysFont("Arial",32)
        mouse_pressed = False

        basespeed = self.screen_height/460.0
        player = players(0,0,ptext,100,basespeed)
        eqslots = ['main','off','head','torso','legs','feet','arms']
        pleq = pls[-1]
        if pleq[0]>-1:
            player.equip(weapons[pleq[0]].create(pls[2]),'main')
        if pleq[1]>-1:
            player.equip(weapons[pleq[1]].create(pls[2]),'off')
            print "off?"
        for i in range(2,len(pleq)):
            if pleq[i]>-1:
                player.equip(pleq[i].create(pls[2]),eqslots[i])
        for i in range(30):
            player.stash.append(weapons[0].create())
        
        temp = textfont.render("Save & Quit",True,(255,255,255))
        exitb = button(self.screen_width/2-temp.get_width()/2-2,self.screen_height-100,self.butextures,temp.get_width()+4)
        exitb.setTxt(temp)
        
        temp = textfont.render("Go on an adventure!",True,(255,255,255))
        dungeonb = button(self.screen_width/2-temp.get_width()/2-2, self.screen_height/2-100,self.butextures,temp.get_width()+4)
        dungeonb.setTxt(temp)

        prevb = button(self.screen_width/2-220, self.screen_height/2+50,self.butextures)
        temp = textfont.render("Prev.",True,(255,255,255))
        prevb.setTxt(temp)

        nextb = button(self.screen_width/2+100, self.screen_height/2+50,self.butextures)
        temp = textfont.render("Next.",True,(255,255,255))
        nextb.setTxt(temp)

        temp = textfont.render("Open Stash",True,(255,255,255))
        stashb = button(self.screen_width/2-temp.get_width()/2-2, self.screen_height/2+150,self.butextures,temp.get_width()+4)
        stashb.setTxt(temp)

        difficulties = ['Easy','Medium','Hard']
        diff_index = 1
        diff_txt = textfont.render(difficulties[diff_index],True,(255,255,255))

        player.skills[0] = skill("skillshot",(50,100),120,pygame.image.load("resources/fireball.png").convert_alpha(),1)

        while 1:
            self.screen.fill((0,0,0))
            mousepos = pygame.mouse.get_pos()
            self.screen.blit(dungeonb.getText(mouse_pressed,mousepos[0],mousepos[1]),dungeonb.rect)
            self.screen.blit(prevb.getText(mouse_pressed,mousepos[0],mousepos[1]),prevb.rect)
            self.screen.blit(nextb.getText(mouse_pressed,mousepos[0],mousepos[1]),nextb.rect)
            self.screen.blit(exitb.getText(mouse_pressed,mousepos[0],mousepos[1]),exitb.rect)
            self.screen.blit(stashb.getText(mouse_pressed,mousepos[0],mousepos[1]),stashb.rect)
            self.screen.blit(diff_txt,(self.screen_width/2-50, self.screen_height/2+50))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False
                        if exitb.getPressed():
                            return
                        elif prevb.getPressed():
                            if diff_index>0:
                                diff_index -=1
                                diff_txt = textfont.render(difficulties[diff_index],True,(255,255,255))
                        elif nextb.getPressed():
                            if diff_index<len(difficulties)-1:
                                diff_index +=1
                                diff_txt = textfont.render(difficulties[diff_index],True,(255,255,255))
                        elif dungeonb.getPressed():
                            self.game(windowsize,player,diff_index)
                        elif stashb.getPressed():
                            self.stashscreen(windowsize,player)

    def stashscreen(self,windowsize,player):
        textfont = pygame.font.SysFont("Arial",32)
        mouse_pressed = False
        temp = textfont.render("<",True,(255,255,255))
        exitb = button(10,0,self.butextures,temp.get_width(),temp.get_height())
        exitb.setTxt(temp)

        buttons = []
        counterx = 0
        countery = 80
        for i in player.stash:
            if counterx+i.image.get_width()>windowsize[0]-100:
                counterx = 0
                countery += i.image.get_height() + 20
            buttons.append(button(10+counterx,10+countery,[i.image]*3))
            counterx+=i.image.get_width() + 10
            
        while 1:
            self.screen.fill((0,0,0))
            mousepos = pygame.mouse.get_pos()
            for i in buttons:
                self.screen.blit(i.getText(mouse_pressed,mousepos[0],mousepos[1]),i.rect)
            self.screen.blit(exitb.getText(mouse_pressed,mousepos[0],mousepos[1]),exitb.rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False
                        if exitb.getPressed():
                            return

    def game(self, windowsize, player, diff_index):
        #Initializing variables
            #Gametime and framerate
        clock = pygame.time.Clock()
        framerate = 60
        basespeed = self.screen_height/460.0
            #Key/Mouse
        mouse_pressed = False
        mousepos = [-1,-1]
            #Graphics
        textfont = pygame.font.SysFont("Arial",24)
        gamesize = (self.screen_height,self.screen_height)
        ge = GEngine(mousepos,gamesize,windowsize)
        self.inventory = False
            #Game
        paused = False
        projectiles = []
        
        ge.setCurrWorld(wflavours[0])
        self.inv = self.makeInv()
        ondoorout = textfont.render("Press 'E' to exit the dungeon",True,(0,0,255))
        ondoorin = textfont.render("Press 'E' to go through the door",True,(0,0,255))

        #Loading world
        kosmos=world(3*(diff_index+1),1,wflavours[0],gamesize)
        self.roomhead = kosmos.start()
        self.currroom = self.roomhead
        
        #The bounds added by the GEngine to the given room
        self.bounds = ge.setRoom(self.currroom)

        #Player
        spawn = (self.currroom.exits[0].rect.x,self.currroom.exits[0].rect.y)
        self.ondoor = self.currroom.exits[0]
        player.x,player.y = spawn
        

        #player.live(100,basespeed)
        

        
        
        while 1:
            #FPS limiter.
            time = clock.tick(framerate)
            mouse_pressed = pygame.mouse.get_pressed()
            #FPS counter.
            thetext = "FPS: " + str(1000/time)
            temp = textfont.render(thetext,True,(0,0,0),(255,255,255))
            time = time / 1000.0

            #Get the current position of the mouse.
            mousepos = pygame.mouse.get_pos()

            #Empty the screen and then fill it with map and the counter.
            self.screen.fill((0,0,0))
            self.screen.blit(ge.display(player,self.currroom,projectiles),ge.rpos)
            self.screen.blit(temp,(0,0))
            if not self.ondoor is None:
                if self.ondoor.link is None:
                    self.screen.blit(ondoorout, (0,self.screen_height-ondoorout.get_height()))
                else:
                    self.screen.blit(ondoorin, (0,self.screen_height-ondoorout.get_height()))
            if self.inventory:
                self.screen.blit(self.inv.getText(),self.inv.rect)
            #Move all projectiles
            self.move_proj(player,gamesize,projectiles)
            

            
            pygame.display.update()

            keys = pygame.key.get_pressed()

            player.movey = 0
            player.movex = 0
            if keys[K_w]:
                player.movey = -1
                if keys[K_s]:
                    player.movey = 0
            elif keys[K_s]:
                player.movey = 1

            if keys[K_d]:
                player.movex = 1
                if keys[K_a]:
                    player.movex = 0
            elif keys[K_a]:
                player.movex = -1
                
            for event in pygame.event.get():
                if event.type == QUIT or ((event.type == KEYDOWN) and (event.key==K_ESCAPE)):
                    return
                elif event.type == KEYDOWN:
                    if event.key==K_i:
                        if self.inventory:
                            self.inventory = False
                        else:
                            self.inventory = True
                elif event.type == KEYUP:
                    if event.key==K_e:
                        if not self.ondoor is None:
                            if self.changeRoom(ge, player):
                                projectiles = []
                            else:
                                return

            self.move_player(player)

            if mouse_pressed[0]:
                attackbuffer = player.attack((mousepos[0]-ge.rpos[0],mousepos[1]-ge.rpos[1]))
                if attackbuffer[0] == "projectile":
                    projectiles.append(attackbuffer[1])
            if mouse_pressed[2]:
                attackbuffer = player.cast(0,(mousepos[0]-ge.rpos[0],mousepos[1]-ge.rpos[1]))
                if attackbuffer[0] == "projectile":
                    projectiles.append(attackbuffer[1])

            player.tick()
            self.gameTick()
            
    def changeRoom(self, ge, player):
        if not self.ondoor.link is None:
            if self.ondoor.link.room is None:
                return False
            self.currroom = self.ondoor.link.room
            self.bounds = ge.setRoom(self.currroom)
            (player.rect.x,player.rect.y) = (self.ondoor.link.x,self.ondoor.link.y)
            (player.x,player.y) = (self.ondoor.link.x,self.ondoor.link.y)
            self.ondoor = self.ondoor.link
            return True
        return False

    def gameTick(self):
        entities = self.currroom.units
        for each in entities:
            if each.isDead:
                entities.remove(each)
                continue
            each.AI()
            each.tick()

    def move_proj(self,player,gamesize,projectiles):
        for each in projectiles:
            each.move()
            if each.rect.x<-12 or each.rect.y<-12 or each.rect.x>gamesize[0] or each.rect.y>gamesize[1]:
                try:
                    projectiles.remove(each)
                except ValueError:
                    pass
                continue
            if each.rect.colliderect(player.rect):
                if each.owner != player:
                    player.hurt(each)
                    try:
                        projectiles.remove(each)
                    except ValueError:
                        pass
                    continue
            for i in self.bounds:
                if each.rect.colliderect(i):
                    try:
                        projectiles.remove(each)
                    except ValueError:
                        pass
                    break
            for i in self.currroom.entities:
                if each.rect.colliderect(i.rect):
                    try:
                        projectiles.remove(each)
                    except ValueError:
                        pass
                    break

            for i in self.currroom.units:
                if each.rect.colliderect(i.rect):
                    if each.owner != i:
                        i.hurt(each)
                        try:
                            projectiles.remove(each)
                        except ValueError:
                            pass
                        break
    
            #for other in projectiles:
            #    if each.rect.colliderect(other.rect):
            #        if each!=other and:
            #            try:
            #                projectiles.remove(each)
            #            except ValueError:
            #                pass
            #            try:
            #                projectiles.remove(other)
            #            except ValueError:
            #                pass
            #            break

    def move_player(self,player):
        player.move(player.movex,0)
        if self.check_collision(player):
            player.rollback()
        player.move(0,player.movey)
        if self.check_collision(player):
            player.rollback()
        player.look(player.movex,player.movey)
        return

    def check_collision(self,player):
        temp = True
        for each in self.currroom.exits:
            if player.rect.colliderect(each.rect):
                self.ondoor = each
                each.active = True
                temp = False
                break
        if temp:
            if not self.ondoor is None:
                self.ondoor.active = False
            self.ondoor = None
        for each in self.bounds:
            if player.rect.colliderect(each):
                return True
        for each in self.currroom.entities:
            if player.rect.colliderect(each.rect):
                return True
        for each in self.currroom.units:
            if player.rect.colliderect(each.rect):
                return True
        return False

    def loadsettings(self):
        winsize = 0
        fullscr = False
        fin = open("settings.ini","r")
        for line in fin:
            temp = line.split(" ")
            if temp[0] == "winsize":
                try:
                    winsize = int(temp[2])
                except ValueError:
                    winsize = 0
            elif temp[0] == "fullscr":
                try:
                    fullscr = int(temp[2])
                    if fullscr == 1:
                        fullscr = True
                except ValueError:
                    winsize = False
        return (winsize,fullscr)

    def makeInv(self):
        newsize = (self.screen_width/4,self.screen_height/2)
        temp = gui[0]
        temp.blit(gui[1],(temp.get_width()/2,temp.get_height()/2))
        temp = pygame.transform.scale(temp, newsize)
        return interface(self.screen_width-newsize[0],self.screen_height-newsize[1],temp)
if __name__ == "__main__":
    new = game()
