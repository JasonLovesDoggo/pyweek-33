from utils import HiddenPrints

with HiddenPrints():
    import pygame
    from pygame.locals import *
import isometric
import configparser
import input
import levels
del HiddenPrints

# Get game configs.
config = configparser.ConfigParser()
config.read("assets/configs/config.ini")
config.sections()

# Setup pygame.
print("Successfully initialized %s pygame modules, %s failed." % (pygame.init()))
max_fps = int(config["WINDOW"]["MAXFPS"])
clock = pygame.time.Clock()

# Create windows and surfaces
print("Creating game displays.")
width, height = int(config["WINDOW"]["DEFAULTX"]), int(config["WINDOW"]["DEFAULTY"])
pygame.display.set_caption(config["WINDOW"]["TITLE"])
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
smaller = height if height < width else width
display = pygame.Surface((smaller / 3, smaller / 3))
debug_font = pygame.font.SysFont("Arial", 30)

offset = (150, 150)

level = levels.Level("assets/levels/example.tmx", config)
delta_time = 0

# Add key callbacks
level.movement.add(pygame.K_UP, input.Movement.UP)
level.movement.add(pygame.K_w, input.Movement.UP)
level.movement.add(pygame.K_DOWN, input.Movement.DOWN)
level.movement.add(pygame.K_s, input.Movement.DOWN)
level.movement.add(pygame.K_LEFT, input.Movement.LEFT)
level.movement.add(pygame.K_a, input.Movement.LEFT)
level.movement.add(pygame.K_RIGHT, input.Movement.RIGHT)
level.movement.add(pygame.K_d, input.Movement.RIGHT)

# Game loop.
print("Starting game loop.")
while True:
    # Content rendering.
    display.fill((0, 0, 0))

    # Draws out-of-bounds entities behind in-bounds geometry.
    for task in level.entity_manager.get_outside_back_entities():
        display.blit(
            task.image,
            isometric.isometric(task.x, task.y, task.z, offset[0], offset[1]),
        )

    for z, layer in enumerate(level.tile_layers):
        level.movement.collision.append([])
        for y, row in enumerate(layer.data):
            for x, tile in enumerate(row):
                tile = level.tmxdata.get_tile_image(x, y, z)

                # Draw in-bounds entities
                tasks = level.entity_manager.get_tasks(x, y, z)
                if len(tasks) > 0:
                    for task in tasks:
                        display.blit(
                            task.image,
                            isometric.isometric(
                                task.x, task.y, task.z, offset[0], offset[1]
                            ),
                        )

                if tile is not None:
                    display.blit(
                        tile,
                        isometric.isometric(x, y, z, offset[0], offset[1]),
                        (0, 0, 20, 24),
                    )

                    collider = level.tmxdata.get_tile_properties(x, y, z)["colliders"][
                        0
                    ]
                    if collider.type is not None:
                        level.movement.collision[z].append((x, y))
                        level.movement.collision[z].append(collider.type)

    # Draws out-of-bounds entities in front of in-bounds geometry.
    for task in level.entity_manager.get_outside_front_entities(
        len(level.tile_layers[0].data[0]),
        len(level.tile_layers[0].data),
        len(level.tile_layers),
    ):
        display.blit(
            task.image,
            isometric.isometric(task.x, task.y, task.z, offset[0], offset[1]),
        )

    for event in pygame.event.get():
        if event.type == QUIT:  # Quit routine.
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_F3:
                level.toggle_fps()
                # level = level.switch_level('assets/levels/example2.tmx')
        elif (
            event.type == pygame.WINDOWRESIZED
        ):  # If window is resized, resize the display surface.
            width, height = pygame.display.get_surface().get_size()
            smaller = height if height < width else width
            display = pygame.Surface((smaller / 3, smaller / 3))

    # Movement system
    level.movement.run(pygame.key.get_pressed(), level.entity_manager, delta_time)

    # Transform the screen so game content is always the same size, then update.
    screen.blit(pygame.transform.scale(display, (height, height)), (0, 0))

    if level.show_fps:
        fps_surface = debug_font.render(
            f"Fps: {int(clock.get_fps())}", False, (255, 255, 255)
        )
        screen.blit(fps_surface, (0, 0))

    pygame.display.update()
    delta_time = clock.tick(max_fps) / 1000
