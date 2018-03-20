import pygame
import time
import random

pygame.init()


BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My First Game')
pygame.font.init()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)

screen.blit(background, (0, 0))
pygame.display.flip()
clock = pygame.time.Clock()


def display_text(text, color, loc=None, font='Comic Sans MS', size=150):
    x, y = pygame.display.get_surface().get_size()
    if size is None:
        size=150

    background.fill(WHITE)
    myfont = pygame.font.SysFont(font, size)
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
while running:
    clock.tick(60)

    if correct:
        char = random.randrange(65, 90)
        correct = False
    display_text(chr(char), BLACK, size=None)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == char + 32:
                display_text(chr(char), GREEN, size=None)
                correct = True
                print('sleeping')
                time.sleep(2)
            else:
                display_text(chr(char), RED, size=None)
                print('sleeping')
                time.sleep(1)



