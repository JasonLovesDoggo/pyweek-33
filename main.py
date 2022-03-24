from sys import stdout
from src.utils.tools import HiddenPrints, sizeString

with HiddenPrints():
    import pygame
    from pygame.locals import *
import configparser
import src.map.levels as levels
import src.utils.input as input
import src.rendering.screens as screens
import logging


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


def end():
    log.info("Quitting game.")
    pygame.quit()
    quit()


def run(screen_manager):
    level = levels.Level("assets/levels/example.tmx", config, screen_manager.current)

    level.movement_manager.add(pygame.K_UP, input.UP)
    level.movement_manager.add(pygame.K_w, input.UP)
    level.movement_manager.add(pygame.K_DOWN, input.DOWN)
    level.movement_manager.add(pygame.K_s, input.DOWN)
    level.movement_manager.add(pygame.K_LEFT, input.LEFT)
    level.movement_manager.add(pygame.K_a, input.LEFT)
    level.movement_manager.add(pygame.K_RIGHT, input.RIGHT)
    level.movement_manager.add(pygame.K_d, input.RIGHT)

    offset = (150, 150)
    delta_time = screen_manager.update(config)

    log.info("Starting update loop.")
    while True:
        keys = pygame.key.get_pressed()
        if screen_manager.current["name"] == "world":
            offset = level.render_manager.render_tiles_and_entities(
                level, offset, int(config["SETTINGS"]["BOXCAMERAPADDING"])
            )

            for event in pygame.event.get():
                if event.type == QUIT:  # Quit routine.
                    end()
                elif event.type == KEYDOWN:
                    if event.key == K_F1:
                        level = level.switch_level(level.filename)
                    elif event.key == K_F2:
                        if config["SETTINGS"]["SHOWFPS"].lower() == "true":
                            config["SETTINGS"]["SHOWFPS"] = "false"
                        else:
                            config["SETTINGS"]["SHOWFPS"] = "true"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        screen_manager.switch(screen_manager.getByName("menu"))
                elif (
                    event.type == pygame.WINDOWRESIZED
                ):  # If window is resized, resize the display surface.
                    size = pygame.display.get_surface().get_size()
                    smaller = size[1] if size[1] < size[0] else size[0]
                    level.current = pygame.Surface((smaller / 3, smaller / 3))
                    level.update()
                    del size, smaller

            if config["DEBUG"]["RELOADONFALL"].lower() == "true":
                if level.movement_manager.player.z < -5:
                    level = level.switch_level(level.filename)

            # Movement system
            level.movement_manager.run(keys, level.entity_manager, delta_time, offset)

        elif screen_manager.current["name"] == "menu":
            for event in pygame.event.get():
                if event.type == QUIT:  # Quit routine.
                    end()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        screen_manager.switch(screen_manager.getByName("world"))

        # Take care of chores
        for event in pygame.event.get():
            if event.type == QUIT:  # Quit routine.
                log.info("Quitting game.")
                pygame.quit()
                quit()

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
    pygame.draw.circle(display, (200, 200, 30), (100, 100), 20)
    screen_manager.add(display, "menu")

    run(screen_manager)


if __name__ == "__main__":
    main()
