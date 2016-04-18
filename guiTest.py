import pygame
from pygame.locals import *
from sys import exit
from gui import *

class game():

    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        windowsize = (self.screen_width, self.screen_height)
        
        #Set the main surface, the "display"
        self.screen = pygame.display.set_mode(windowsize)
        textfont = pygame.font.SysFont("Arial",24)
        #Make button, blit it and test it out.
        b = button(100,100,[pygame.image.load("resources/unpressed.png"),pygame.image.load("resources/pressed.png"),pygame.image.load("resources/hover.png")],40,40)
        i = interface(200,200,pygame.image.load("resources/pressed.png"),400,400)

        #Key/Mouse
        self.mouse_pressed = False

        while 1:
            (x,y) = pygame.mouse.get_pos()
            self.screen.fill((0,0,0))
            temp = b.getText(self.mouse_pressed,x,y)
            self.screen.blit(temp,b.rect)
            temp = i.getText()
            self.screen.blit(temp,i.rect)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or ((event.type == KEYDOWN) and (event.key==K_ESCAPE)):
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    self.mouse_pressed = False

if __name__ == "__main__":
    new = game()
