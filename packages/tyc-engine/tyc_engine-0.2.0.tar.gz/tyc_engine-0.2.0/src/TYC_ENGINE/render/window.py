import pygame

pygame.init()

def render(self, w, h, name):
    self.screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(name)

def run(running):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False