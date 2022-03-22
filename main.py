from sys import stdout
from src.utils.tools import HiddenPrints, sizeString

with HiddenPrints():
    import pygame
    from pygame.locals import *
import configparser
import src.map.levels as levels
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
    clock = pygame.time.Clock()

    # Create windows and surfaces
    size = (int(config["WINDOW"]["DEFAULTX"]), int(config["WINDOW"]["DEFAULTY"]))

    log.info(f"Creating game displays, window size: {sizeString(size)}")
    pygame.display.set_caption(config["WINDOW"]["TITLE"])
    screen = pygame.display.set_mode(
        size
    )  # ad , pygame.RESIZABLE if you want it to be resizeable NOTE causes problems
    smaller = size[1] if size[1] < size[0] else size[0]
    display = pygame.Surface((smaller / 3, smaller / 3))
    debug_font = pygame.font.SysFont("Arial", 30)

    return clock, size, screen, display, debug_font


def update_screen(screen, level, font, clock):
    screen.blit(pygame.transform.scale(level.display, screen.get_size()), (0, 0))

    if config["SETTINGS"]["SHOWFPS"].lower() == "true":
        fps_surface = font.render(
            f"Fps: {int(clock.get_fps())}", False, (255, 255, 255)
        )
        screen.blit(fps_surface, (0, 0))

    pygame.display.update()
    return clock.tick(int(config["WINDOW"]["MAXFPS"])) / 1000


def run_game(level, clock, size, screen, debug_font, delta_time):
    offset = (150, 150)
    log.info("Starting game loop.")
    while True:
        offset = level.render_manager.render_tiles_and_entities(
            level, offset, int(config["SETTINGS"]["BOXCAMERAPADDING"])
        )

        for event in pygame.event.get():
            if event.type == QUIT:  # Quit routine.
                log.info("Quitting game.")
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_F1:
                    level = level.switch_level(level.filename)
                elif event.key == K_F2:
                    if config["SETTINGS"]["SHOWFPS"].lower() == "true":
                        config["SETTINGS"]["SHOWFPS"] = "false"
                    else:
                        config["SETTINGS"]["SHOWFPS"] = "true"
            elif (
                event.type == pygame.WINDOWRESIZED
            ):  # If window is resized, resize the display surface.
                size = pygame.display.get_surface().get_size()
                smaller = size[1] if size[1] < size[0] else size[0]
                level.display = pygame.Surface((smaller / 3, smaller / 3))
                level.update()

        if config['DEBUG']['RELOADONFALL'].lower() == 'true':
            if level.movement_manager.player.z < -5:
                level = level.switch_level(level.filename)

        # Movement system
        level.movement_manager.run(
            pygame.key.get_pressed(), level.entity_manager, delta_time, offset
        )

        delta_time = update_screen(screen, level, debug_font, clock)


def main():
    clock, size, screen, display, debug_font = setup()

    level = levels.Level("assets/levels/example.tmx", config, display)

    # offset = level.movement_manager.player

    delta_time = 0

    # Add key callbacks
    level.movement_manager.add(pygame.K_UP, level.movement_manager.UP)
    level.movement_manager.add(pygame.K_w, level.movement_manager.UP)
    level.movement_manager.add(pygame.K_DOWN, level.movement_manager.DOWN)
    level.movement_manager.add(pygame.K_s, level.movement_manager.DOWN)
    level.movement_manager.add(pygame.K_LEFT, level.movement_manager.LEFT)
    level.movement_manager.add(pygame.K_a, level.movement_manager.LEFT)
    level.movement_manager.add(pygame.K_RIGHT, level.movement_manager.RIGHT)
    level.movement_manager.add(pygame.K_d, level.movement_manager.RIGHT)

    run_game(level, clock, size, screen, debug_font, delta_time)


if __name__ == "__main__":
    main()
