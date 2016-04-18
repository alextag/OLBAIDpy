import pygame
class button():

    def __init__(self,x,y,images,width=-1,height=-1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.txt = None
        self.txtw = 0
        self.txth = 0
        self.pressed = False
        tempim = [None,None,None]
        self._notpressed = None
        self._pressed = None
        self._hover = None
        self.rect = pygame.Rect((x,y),(self.width,self.height))
        if width==-1 and height==-1:
            self.width = images[0].get_width()
            self.height = images[0].get_height()
            self._notpressed = images[0]
            self._pressed = images[1]
            if len(images)>2:
                self._hover = images[2]
        else:
            if width==-1:
                self.width = images[0].get_width()
            if height==-1:
                self.height = images[0].get_height()
            for i in range(len(images)):
                tempim[i] = pygame.transform.scale(images[i],(self.width,self.height))
            self._notpressed = tempim[0]
            self._pressed = tempim[1]
            if len(images)>2:
                self._hover = tempim[2]
        return
    
    def getText(self,pressed,x=-1,y=-1):
        self.pressed = False
        if x>=self.x and x<=self.x+self.width:
                if y>=self.y and y<=self.y+self.height: 
                    if pressed:
                        self.pressed = True
                        temp = self._pressed.copy()
                        if not self.txt is None:
                            temp.blit(self.txt,(self.width/2-self.txtw/2,self.height/2-self.txth/2))
                        return temp
                    elif not self._hover is None:
                        temp = self._hover.copy()
                        if not self.txt is None:
                            temp.blit(self.txt,(self.width/2-self.txtw/2,self.height/2-self.txth/2))
                        return temp

        temp = self._notpressed.copy()
        if not self.txt is None:
            temp.blit(self.txt,(self.width/2-self.txtw/2,self.height/2-self.txth/2))
        return temp

    def setTxt(self, txt):
        self.txt = txt
        self.txtw = txt.get_width()
        self.txth = txt.get_height()

    def getPressed(self):
        return self.pressed

class interface():

    def __init__(self,x,y,image,width=-1,height=-1):
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        if width==-1:
            self.width = image.get_width()
            self.height = image.get_height()
        else:
            image = pygame.transform.scale(image,(width,height))

        self.text = image
        self.rect = pygame.Rect((x,y),(self.width,self.height))

    def getText(self):
        return self.text
