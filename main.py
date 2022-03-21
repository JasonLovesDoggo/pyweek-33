from src.utils.tools import HiddenPrints

with HiddenPrints():
    import pygame
    from pygame.locals import *
import configparser
import src.utils.input as game_input
import src.map.levels as levels

del HiddenPrints

offset = (150, 150)

# Get game configs.
config = configparser.ConfigParser()
config.read("assets/configs/config.ini")
config.sections()


def setup():
    print_setup = config["LOGGING"]["PRINTSETUPINFO"].lower() == "true"
    if print_setup:
        print("Loaded configs.")
        print(
            "Successfully initialized %s pygame modules, %s failed." % (pygame.init())
        )
    clock = pygame.time.Clock()

    # Create windows and surfaces
    size = (int(config["WINDOW"]["DEFAULTX"]), int(config["WINDOW"]["DEFAULTY"]))
    if print_setup:
        print("Creating game displays. \nWindow size: %sx%s" % size)
    pygame.display.set_caption(config["WINDOW"]["TITLE"])
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    smaller = size[1] if size[1] < size[0] else size[0]
    display = pygame.Surface((smaller / 3, smaller / 3))
    debug_font = pygame.font.SysFont("Arial", 30)

    return clock, size, screen, display, debug_font


def update_screen(screen, display, font, clock):
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))

    if config["DEBUG"]["SHOWFPS"].lower() == "true":
        fps_surface = font.render(
            f"Fps: {int(clock.get_fps())}", False, (255, 255, 255)
        )
        screen.blit(fps_surface, (0, 0))

    pygame.display.update()
    return clock.tick(int(config["WINDOW"]["MAXFPS"])) / 1000


def run_game(level, clock, size, screen, debug_font, delta_time):
    print("Starting game loop.")
    while True:
        level.renderer.render_tiles_and_entities(level, offset)

        for event in pygame.event.get():
            if event.type == QUIT:  # Quit routine.
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_F3:
                    level = level.switch_level("assets/levels/example2.tmx")
            elif (
                event.type == pygame.WINDOWRESIZED
            ):  # If window is resized, resize the display surface.
                size = pygame.display.get_surface().get_size()
                smaller = size[1] if size[1] < size[0] else size[0]
                level.display = pygame.Surface((smaller / 3, smaller / 3))

        # Movement system
        level.movement.run(
            pygame.key.get_pressed(), level.entity_manager, delta_time, offset
        )

        delta_time = update_screen(screen, level.display, debug_font, clock)


def main():
    clock, size, screen, display, debug_font = setup()

    level = levels.Level("assets/levels/example.tmx", config, display)

    delta_time = 0

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
