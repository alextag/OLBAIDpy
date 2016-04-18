import pygame
class GEngine():

    def __init__(self, mousepos, gamesize, window):
        #A pointer to the array that keeps track of the mouse position.
        self.mousepos = mousepos
        self.currentWorld = pygame.Surface(gamesize)
        self.gamesize = gamesize
        self.newsize = gamesize
        self.rpos = (0,0)
        self.room = None
        self.temproom = None
        self.window = window
        self.wallv_orig = None
        self.wallh_orig = None

    def setCurrWorld(self, images):
        self.wallv_orig = images[1]
        self.wallh_orig = images[2]
        if images[0].get_width()!=self.gamesize[0] or images[0].get_height()!=self.gamesize[1]:
            self.currentWorld = pygame.transform.scale(images[0],self.gamesize)
            return
        self.currentWorld = images[0]
        return

    def setRoom(self, room):
        self.room = room
        self.newsize = (int(room.width/16.0*self.gamesize[0]),int(room.height/16.0*self.gamesize[1]))
        self.temproom = pygame.transform.scale(self.currentWorld,self.newsize)
        self.rpos = (self.window[0]/2 - self.newsize[0]/2, self.window[1]/2 - self.newsize[1]/2)
        self.wallv = pygame.transform.scale(self.wallv_orig,(8,self.newsize[1]))
        self.wallh = pygame.transform.scale(self.wallh_orig,(self.newsize[0],8))
        self.temproom.blit(self.wallv,(0,0))
        self.temproom.blit(self.wallh,(0,0))
        self.temproom.blit(self.wallv,(self.newsize[0]-8,0))
        self.temproom.blit(self.wallh,(0,self.newsize[1]-8))
        boxes = []
        boxes.append(pygame.Rect((-2,0),(0,self.newsize[1])))
        boxes.append(pygame.Rect((0,-2),(self.newsize[0],0)))
        boxes.append(pygame.Rect((self.newsize[0],0),(0,self.newsize[1])))
        boxes.append(pygame.Rect((0,self.newsize[1]),(self.newsize[0],0)))
        return boxes

    def display(self, player, room, projectiles=[]):
        
        temp = pygame.Surface(self.newsize)
        temp.blit(self.temproom,(0,0))

        for each in self.room.entities:
            temp.blit(each.getText(),each.rect)
        for each in self.room.exits:
            temp.blit(each.getText(),each.rect)
        for each in self.room.triggerables:
            temp.blit(each.getText(),each.rect)
        for each in self.room.units:
            temp.blit(each.getText(),each.rect)
        
        temp.blit(player.getText(),player.rect)
        for each in projectiles:
            temp.blit(each.getText(),each.rect)

        return temp
