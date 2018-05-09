import pygame
import time
import random
import os

pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FULL_SCREEN = True

info = pygame.display.Info()

if FULL_SCREEN:
    MAX_HEIGHT = info.current_h
    MAX_WIDTH = info.current_w
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    MAX_HEIGHT = 600
    MAX_WIDTH = 400
    screen = pygame.display.set_mode((MAX_HEIGHT, MAX_WIDTH))

pygame.display.set_caption('Toddler Learner')
pygame.font.init()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)

screen.blit(background, (0, 0))
pygame.display.flip()
clock = pygame.time.Clock()


def get_max_font_size(font):
    for i in range(0, 5000):
        myfont = pygame.font.SysFont(font, i)
        if myfont.get_height() >= MAX_HEIGHT:
            return i
    return i


def display_text(text, color, loc=None, font='Comic Sans MS', size=32):
    x, y = pygame.display.get_surface().get_size()
    myfont = pygame.font.SysFont(font, size)

    background.fill(WHITE)

    render_text = myfont.render(text, True, color)
    if loc is None:
        text_rect = render_text.get_rect(center=(x/2, y/2))
        background.blit(render_text, text_rect)
    else:
        background.blit(render_text, loc)
    screen.blit(background, (0, 0))
    pygame.display.update()


running = True
correct = True
font_name = 'Comic Sans MS'
font_size = get_max_font_size(font_name)
print(font_size)
while running:
    clock.tick(60)

    if correct:
        char = random.randrange(65, 90)
        correct = False
    display_text(chr(char), BLACK, font=font_name, size=font_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == char + 32:
                display_text(chr(char), GREEN, font=font_name, size=font_size)
                correct = True
                pygame.mixer.quit()
                pygame.mixer.init(frequency=48000)
                pygame.mixer.music.load('resources' + os.sep + 'clap.mp3')
                pygame.mixer.music.play(0)
                time.sleep(2.5)
                pygame.mixer.music.stop()
            else:
                display_text(chr(char), RED, font=font_name, size=font_size)
                time.sleep(1)



