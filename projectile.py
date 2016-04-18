import pygame

class projectile:
    def __init__(self,(x,y),(x0,y0),image,owner,dmg,speed,width=-1,height=-1): #(x,y):target,(x0,y0):source
        if width!=-1:
            image=pygame.transform.scale(width,height)
        self.owner=owner
        self.width=image.get_width()
        self.height=image.get_height()
        self.text=image
        self.rect = pygame.Rect((x0,y0),(self.width,self.height))
        self.x=float(x0)
        self.y=float(y0)
        self.dmg = dmg
        self.speed=speed
        if(abs(x-x0)>1):
            self.l=(y-y0)/float((x-x0))
            self.direction=(x-x0)/abs(x-x0)
            if abs(self.l)>1:
                self.direction=self.direction/float(abs(self.l))
            self.b=y-self.l*x
        else:
            self.direction=0
            self.l=0
            if (abs(y-y0)>1):
                self.b=(y-y0)/abs(y-y0)
            else:
                self.b=-1
            
    def move(self):
        self.x=self.x+self.direction*self.speed
        if self.direction==0:
            self.y=self.y+self.b*self.speed
        else:
            self.y=float(self.l)*self.x+self.b
        self.rect.x = self.x
        self.rect.y = self.y
        
    def getText(self):
        return self.text
