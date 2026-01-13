import os
import sys
import pygame

BASE_DIR = os.path.dirname(__file__)

def render(width=400, height=300, title="tyce", icon="ico.png"):
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    if icon:
        icon_path = os.path.join(BASE_DIR, "render", "res", icon)
        try:
            pygame.display.set_icon(pygame.image.load(icon_path))
        except pygame.error:
            print("Icon not found")

    return screen


def run():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()
