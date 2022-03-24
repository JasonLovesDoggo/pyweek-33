from src.utils.tools import HiddenPrints
with HiddenPrints():
    import pygame
    from pygame.locals import *
from logging import getLogger

log = getLogger(__name__)


def end(code = None):
    log.info(f"Quitting game{f' with code: {code}' if code is not None else ''}.")
    pygame.quit()
    quit()


def run_world(level, screen_manager, config, delta_time, offset, pause=False):
    level.current = screen_manager.current
    level.update()

    keys = pygame.key.get_pressed()
    offset = level.render_manager.render_tiles_and_entities(
        level, offset, int(config["SETTINGS"]["BOXCAMERAPADDING"])
    )

    for event in pygame.event.get():
        if event.type == QUIT:  # Quit routine.
            end()
        elif event.type == KEYDOWN:
            if event.key == K_F1 and not pause:
                level = level.switch_level(level.filename)
            elif event.key == K_F2:
                if config["SETTINGS"]["SHOWFPS"].lower() == "true":
                    config["SETTINGS"]["SHOWFPS"] = "false"
                else:
                    config["SETTINGS"]["SHOWFPS"] = "true"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return 'world' if pause else 'menu', level, offset
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
    if not pause:
        level.movement_manager.run(keys, level.entity_manager, delta_time, offset)