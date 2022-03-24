import pygame
from logging import getLogger

log = getLogger(__name__)


class ScreenManager:
    def __init__(self, target) -> None:
        self.target = target
        self.screens = []
        self.current = None
        self.currentIndex = None
        self.fpsFont = pygame.font.SysFont("Arial", 30)
        self.clock = pygame.time.Clock()

    def add(self, surface: pygame.surface, name: str, callback=None):
        base = {"name": name, "surface": surface}
        self.screens.append(Screen(surface, name, callback=callback))

        if len(self.screens) == 1:
            self.current = self.screens[0]
            self.currentIndex = 0

    def switch(self, target):
        if type(target) == str:
            log.log(f'Switched to screen "{target}".')
            index = self.getByName(self, target)
        else:
            index = target
        self.currentIndex = index
        self.current = self.screens[index]
        if self.current.callback is not None:
            self.current.callback()

    def getByName(self, name):
        for index, screen in enumerate(self.screens):
            if screen.name == name:
                return index

    def update(self, config):
        self.target.blit(
            pygame.transform.scale(self.current.surface, self.target.get_size()),
            (0, 0),
        )

        if config["SETTINGS"]["SHOWFPS"].lower() == "true":
            fps_surface = self.fpsFont.render(
                f"Fps: {int(self.clock.get_fps())}", False, (255, 255, 255)
            )
            self.target.blit(fps_surface, (0, 0))

        pygame.display.update()
        return self.clock.tick(int(config["WINDOW"]["MAXFPS"])) / 1000


class Screen:
    def __init__(self, surface, name, callback=None) -> None:
        self.surface = surface
        self.name = name
        self.callback = callback
