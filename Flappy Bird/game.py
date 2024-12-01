import pygame
import random
from pygame.locals import *

pygame.init()

# Screen settings
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Colors and fonts
white = (255, 255, 255)
font = pygame.font.SysFont("Arial", 50)

# Game variables
clock = pygame.time.Clock()
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pass_pipe = False
pipe_gap = 150
score = 0
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
fps = 60

# Load images
bg = pygame.image.load("bg.png")
ground = pygame.image.load("floor.png")
restart = pygame.image.load("restart.png")

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        # Position determines top or bottom pipe
        if position == 1:  # Top pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        elif position == -1:  # Bottom pipe
            self.rect.topleft = [x, y + pipe_gap // 2]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        # Check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f"bird{i}.png") for i in range(1, 3)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.counter = 0

    def update(self):
        global flying, game_over
        if flying:
            # Apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < screen_height - 168:
                self.rect.y += int(self.vel)

        if not game_over:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animate bird
            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

              #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            #point the bird at the ground
            self.image = pygame.transform.rotate(self.images[self.index], -90)

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height // 2
    return 0

# Sprite groups
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 50, restart)

# Game loop
run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    # Check game over
    if game_over:
        if restart_button.draw():
            game_over = False
            score = reset_game()
    else:
        # Spawn pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, -1)
            top_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Update pipes
        pipe_group.update()

        # Scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # Check for collisions
    if pygame.sprite.groupcollide(pipe_group, bird_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= screen_height - 168:
        game_over = True
        flying = False

    # Check if passed pipe
    if len(pipe_group) > 0:
        first_pipe = pipe_group.sprites()[0]
        if bird_group.sprites()[0].rect.left > first_pipe.rect.left and \
           bird_group.sprites()[0].rect.right < first_pipe.rect.right and not pass_pipe:
            pass_pipe = True
        if pass_pipe and bird_group.sprites()[0].rect.left > first_pipe.rect.right:
            score += 1
            pass_pipe = False

    draw_text(str(score), font, white, screen_width // 2, 20)
    screen.blit(ground, (ground_scroll, screen_height - 168))

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
