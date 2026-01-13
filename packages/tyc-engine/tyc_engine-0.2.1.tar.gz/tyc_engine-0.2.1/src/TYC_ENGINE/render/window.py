import pygame

pygame.init()

def render(w, h, name):
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(name)

def run(running):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False