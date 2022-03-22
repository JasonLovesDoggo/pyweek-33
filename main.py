from sys import stdout

from pygame import mixer

from src.utils.tools import HiddenPrints

with HiddenPrints():
    import pygame
    from pygame.locals import *
import configparser
import src.utils.input as game_input
import src.map.levels as levels
import logging

del HiddenPrints

# Configure the logger

logging.basicConfig(
    format="%(asctime)s - [%(name)s | %(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
    filename="game.log",
    filemode="a",
    level=logging.INFO,  # Keep at logging.INFO unless you want to see all events then change to LOGGING.DEBUG
)

log = logging.getLogger(__name__)

log.addHandler(logging.StreamHandler(stdout))

# Get game configs.
config = configparser.ConfigParser()
config.read("assets/configs/config.ini")
config.sections()


# mixer.music.load('Music File.mp3')
# mixer.music.play()
# mixer.music.pause()
# mixer.music.stop()

"""

Valid cmds are 
load
unload
play
rewind
stop
pause
unpause
fadeout
set_volume
get_volume
get_busy
set_pos
get_pos
queue
set_endevent
get_endevent"""


def setup():
    log.info("Loaded configs.")
    log.info("Successfully initialized %s pygame modules, %s failed." % (pygame.init()))
    clock = pygame.time.Clock()

    # Create windows and surfaces
    size = (int(config["WINDOW"]["DEFAULTX"]), int(config["WINDOW"]["DEFAULTY"]))

    log.info(f"Creating game displays. \tWindow size: {size}")
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
        offset = level.renderer.render_tiles_and_entities(
            level, offset, int(config["SETTINGS"]["BOXCAMERAPADDING"])
        )

        for event in pygame.event.get():
            if event.type == QUIT:  # Quit routine.
                log.info("Quitting...")
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

        # Movement system
        level.movement.run(
            pygame.key.get_pressed(), level.entity_manager, delta_time, offset
        )

        delta_time = update_screen(screen, level, debug_font, clock)


def main():
    clock, size, screen, display, debug_font = setup()

    level = levels.Level("assets/levels/example.tmx", config, display)

    delta_time = 0

    # inititailize the audio mixer

    log.info("initializing audio mixer...")
    mixer.init()

    # Add key callbacks
    level.movement.add(pygame.K_UP, game_input.Movement.UP)
    level.movement.add(pygame.K_w, game_input.Movement.UP)
    level.movement.add(pygame.K_DOWN, game_input.Movement.DOWN)
    level.movement.add(pygame.K_s, game_input.Movement.DOWN)
    level.movement.add(pygame.K_LEFT, game_input.Movement.LEFT)
    level.movement.add(pygame.K_a, game_input.Movement.LEFT)
    level.movement.add(pygame.K_RIGHT, game_input.Movement.RIGHT)
    level.movement.add(pygame.K_d, game_input.Movement.RIGHT)

    run_game(level, clock, size, screen, debug_font, delta_time)


if __name__ == "__main__":
    main()
