from sys import stdout
from src.utils.tools import HiddenPrints, sizeString

with HiddenPrints():
    import pygame
import configparser
import src.map.levels as levels
import src.utils.input as input
import src.rendering.screens as screens
import logging
import game


# Get game configs.
config = configparser.ConfigParser()
config.read("assets/configs/config.ini")
config.sections()

# Configure the logger
logging.basicConfig(
    format="%(asctime)s - [%(name)s | %(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
    filename="game.log",
    filemode="w",
    level=getattr(logging, str(config["DEBUG"]["LOGGINGLEVEL"]).upper()),
)
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(stdout))

log.info("Starting game.")
log.info("Loaded configs.")


def setup():
    log.info("Successfully initialized %s pygame modules, %s failed." % (pygame.init()))
    # Create windows and surfaces
    size = (int(config["WINDOW"]["DEFAULTX"]), int(config["WINDOW"]["DEFAULTY"]))

    log.info(f"Creating game displays, window size: {sizeString(size)}")
    pygame.display.set_caption(config["WINDOW"]["TITLE"])
    screen = pygame.display.set_mode(
        size
    )  # add pygame.RESIZABLE if you want it to be resizeable NOTE causes problems

    screen_manager = screens.ScreenManager(screen)

    return screen_manager


def run(screen_manager):
    level = levels.Level("assets/levels/example.tmx", config, screen_manager)

    level.movement_manager.add(pygame.K_UP, input.UP)
    level.movement_manager.add(pygame.K_w, input.UP)
    level.movement_manager.add(pygame.K_DOWN, input.DOWN)
    level.movement_manager.add(pygame.K_s, input.DOWN)
    level.movement_manager.add(pygame.K_LEFT, input.LEFT)
    level.movement_manager.add(pygame.K_a, input.LEFT)
    level.movement_manager.add(pygame.K_RIGHT, input.RIGHT)
    level.movement_manager.add(pygame.K_d, input.RIGHT)

    delta_time = screen_manager.update(config)

    offset = (150, 150)

    log.info("Starting update loop.")
    while True:
        if screen_manager.current.name == "world":
            res = game.run_world(level, screen_manager, config, delta_time, offset)
            if res is not None:
                target, level, offset = res
                screen_manager.switch(screen_manager.getByName(target))
                del target

        elif screen_manager.current.name == "menu":
            res = game.run_world(
                level, screen_manager, config, delta_time, offset, pause=True
            )
            if res is not None:
                target, level, offset = res
                screen_manager.switch(screen_manager.getByName(target))
                del target

        delta_time = screen_manager.update(config)


def main():
    screen_manager = setup()

    world = pygame.Surface(
        (
            screen_manager.target.get_size()[0] / 3,
            screen_manager.target.get_size()[1] / 3,
        )
    )
    screen_manager.add(world, "world")

    display = pygame.Surface(
        (
            screen_manager.target.get_size()[0] / 3,
            screen_manager.target.get_size()[1] / 3,
        )
    )
    screen_manager.add(display, "menu")

    run(screen_manager)


if __name__ == "__main__":
    main()
