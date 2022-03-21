import src.utils.isometric as isometric


class Tile_Manager:
    def __init__(self, surface) -> None:
        self.surface = surface
        pass

    def render_tiles_and_entities(self, level, offset):
        self.surface.fill((0, 0, 0))

        # Draws out-of-bounds entities behind in-bounds geometry.
        for task in level.entity_manager.get_outside_back_entities():
            self.surface.blit(
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
                            self.surface.blit(
                                task.image,
                                isometric.isometric(
                                    task.x, task.y, task.z, offset[0], offset[1]
                                ),
                            )

                    if tile is not None:
                        self.surface.blit(
                            tile,
                            isometric.isometric(x, y, z, offset[0], offset[1]),
                            (0, 0, 20, 24),
                        )

                        try:
                            collider = level.tmxdata.get_tile_properties(x, y, z)[
                                "colliders"
                            ][0]
                            # print(level.tmxdata.get_tile_properties(x, y, z)['frames'])
                            if collider.type is not None:
                                level.movement.collision[z].append((x, y))
                                level.movement.collision[z].append(collider.type)
                        except TypeError:
                            pass

        # Draws out-of-bounds entities in front of in-bounds geometry.
        for task in level.entity_manager.get_outside_front_entities(
            len(level.tile_layers[0].data[0]),
            len(level.tile_layers[0].data),
            len(level.tile_layers),
        ):
            self.surface.blit(
                task.image,
                isometric.isometric(task.x, task.y, task.z, offset[0], offset[1]),
            )
