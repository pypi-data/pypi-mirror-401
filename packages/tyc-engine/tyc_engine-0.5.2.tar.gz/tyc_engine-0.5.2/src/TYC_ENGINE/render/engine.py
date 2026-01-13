import sys
import pygame
from .loader import loading_app

class Engine:
    def __init__(self, width=400, height=300, title="tyce"):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None

    async def load(self):
        self.screen = await loading_app(self.width, self.height, self.title)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        sys.exit()
