import os
import sys
import pygame

BASE_DIR = os.path.dirname(__file__)

class Render:

    def display(self, width=400, height=300, title="tyc_e", icon=None):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        if icon:
            try:
                pygame.display.set_icon(pygame.image.load(icon))
            except pygame.error:
             print("Icon not found")

            return self.screen

    def fill(self, screen, color):
        screen.fill(color)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        sys.exit()
