import pygame
from pygame.locals import *

pygame.init()

class Create:
    def screen(self, wh, he, title, icon):
        self.sc = pygame.display.set_mode((wh, he))
        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)\

    def fill(self, color):
        self.sc.fill(color)

    class draw:
        def rect(self, color, wh, he, screen, radius):
            pygame.draw.rect(screen, color, (wh, he))
        def circle(self, color, wh, he, screen, radius):
            pygame.draw.circle(screen, color, (wh, he), radius)
        def line(self, color, wh, he, screen, radius):
            pygame.draw.line(screen, color, (wh, he))



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            clock = pygame.time.Clock()
            pygame.display.update()
            clock.tick(60)