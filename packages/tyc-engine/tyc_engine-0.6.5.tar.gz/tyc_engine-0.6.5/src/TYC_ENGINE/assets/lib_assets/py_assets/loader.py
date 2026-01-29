import asyncio
import pygame
from rich.progress import Progress
from rich import print
from .core import Render


async def init_engine():
    await asyncio.sleep(0.3)


async def load_config():
    await asyncio.sleep(0.3)
    return {"width": 400, "height": 300, "title": "tyc_e"}


async def load_resources():
    await asyncio.sleep(0.3)
    return "ico.png"


async def init_pygame():
    pygame.init()


async def loading_app():
    print("[cyan]Starting application...")

    steps = [
        ("Initializing engine", init_engine),
        ("Loading config", load_config),
        ("Loading resources", load_resources),
        ("Initializing pygame", init_pygame),
    ]

    context = {}

    with Progress() as progress:
        task = progress.add_task("[cyan]Loading...", total=len(steps) + 1)

        for name, step in steps:
            progress.update(task, description=f"[yellow]{name}")
            result = await step()
            context[name] = result
            progress.advance(task)

        progress.update(task, description="[yellow]Creating window")

        renderer = Render()
        screen = renderer.display(
            context["Loading config"]["width"],
            context["Loading config"]["height"],
            context["Loading config"]["title"],
            context["Loading resources"]
        )

        progress.advance(task)

    print("[bold green]Loading complete!")
    return screen
