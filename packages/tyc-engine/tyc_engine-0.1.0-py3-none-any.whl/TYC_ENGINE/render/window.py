import pygame

pygame.init()

def render(self, w, h, name):
    self.screen = pygame.display.set_mode((w, h)), pygame.display.set_caption(name)