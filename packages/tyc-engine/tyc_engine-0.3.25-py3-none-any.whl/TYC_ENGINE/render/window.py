import pygame

pygame.init()

def render(w=200, h=200, name='tyce', icon_path='.res.ico.png'):
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(name)
    if icon_path:  # load icon if provided
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    return screen

def run(running):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()