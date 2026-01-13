import os
import pygame

pygame.init()


def render(w=200, h=200, name='tyce', icon_path=None):
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(name)

    if icon_path:
        try:
            # Полный путь к иконке относительно текущего файла
            base_path = os.path.dirname(__file__)
            full_icon_path = os.path.join(base_path, 'render', 'res', icon_path)
            icon = pygame.image.load(full_icon_path)
            pygame.display.set_icon(icon)
        except pygame.error:
            print("Non icon")
    return screen


def run(running):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

from rich.progress import Progress
import time

def loading_app():
    print("Starting application...")

    # Create a progress bar
    with Progress() as progress:
        task = progress.add_task("[cyan]Loading application...", total=100)

        while not progress.finished:
            # Simulate loading
            time.sleep(0.05)  # short delay for effect
            progress.update(task, advance=1)  # move the progress by 1%

    print("[bold green]Loading complete! Application is ready to use.")

loading_app()
