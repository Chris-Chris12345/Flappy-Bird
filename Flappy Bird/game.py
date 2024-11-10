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
last_pipe = pygame.time.get_ticks() - pipe_frequency
fps = 60

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

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,3):
            img = pygame.image.load(f"bird{i}.png")
            self.images.append(img)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect
        self.rect.center = [x,y]
        self.vel = 0
        self.click = False

    def update(self):
        if flying == True:
            #apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        
        if game_over == False:
            #jump effect
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                self.vel -= 10
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

            #animation
            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                    self.image = self.images[self.index]

            #rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    score = 0
    return score

pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100,int(screen_height/2))
restart_button = Button(screen_width/2, screen_height/2, restart)
run = True

while 1:
    screen.blit(bg,(0,0))

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    if game_over == True:
        if restart_button.draw():
            game_over = False
            score = reset_game()

    screen.blit(ground,(ground_scroll, 768))

    #score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
        
    draw_text(str(score), font, white, int(screen_width/2), 20)

    #collision
    if pygame.sprite.groupcollide(pipe_group, bird_group) or flappy.rect.top < 0:
        game_over = True
    
    if flappy.rect.bottom < 768:
        game_over = True
        flying = False

    if flying == True and game_over == False:
        time_now = pygame.time.get_ticks() 
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1) 
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        pipe_group.update()

        ground_scroll -= scroll_speed
        
        if abs(ground_scroll) > 35:
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over ==False:
            flying = True
    
    clock.tick = fps
    pygame.display.update()

pygame.quit()



            
    
