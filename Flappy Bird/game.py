import pygame
import random
from pygame.locals import *

pygame.init()

screen_height = 936
screen_width = 864

screen = pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont("Arial",50)

white = (255,255,255)

#game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pass_pipe = False
pipe_gap = 150
score = 0
pipe_frequency = 1500 #milliseconds

#load images
bg = pygame.image.load("bg.png")
ground = pygame.image.load("floor.png")
restart = pygame.image.load("restart.png")

def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(img,(x,y))

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self.__init__)
        self.rect = self.image.get_rect()
        #position variable determines if the pipe is coming from the bottom or top
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw():
        action = False
        pos = pygame.mouse.get_pos()
        
        #check mouse over and click condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


