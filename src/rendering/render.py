import src.utils.isometric as isometric
import src.gameobjects.player as player


class TileManager:
    def __init__(self, surface) -> None:
        self.surface = surface
        pass

    def render_tiles_and_entities(self, level, offset, padding):
        self.surface.fill((0, 0, 0))

        # Draws out-of-bounds entities behind in-bounds geometry.
        for task in level.entity_manager.get_outside_back_entities():
            pos = isometric.isometric(task.x, task.y, task.z, offset[0], offset[1])
            if isinstance(task, player.Player):
                task.real_x = pos[0]
                task.real_y = pos[1]

            try:
                animation = task.obj.properties["frames"]
                if animation == []:
                    animation = None
            except (TypeError, AttributeError, KeyError):
                animation = None

            image = task.image
            if animation is not None:
                image = level.animations_manager.tile(
                    animation, str(task.obj.id), level.tmxdata, task.image
                )
            self.surface.blit(image, pos)

        for z, layer in enumerate(level.tile_layers):
            level.movement_manager.collision.append([])
            for y, row in enumerate(layer.data):
                for x, tile in enumerate(row):
                    try:
                        animation = level.tmxdata.get_tile_properties(x, y, z)["frames"]
                        if animation == []:
                            animation = None
                    except TypeError:
                        animation = None

                    tile = level.tmxdata.get_tile_image(x, y, z)
                    if animation is not None:
                        tile = level.animations_manager.tile(
                            animation, f"{x}:{y}:{z}", level.tmxdata, tile
                        )

                    # Draw in-bounds entities
                    tasks = level.entity_manager.get_tasks(x, y, z)
                    if len(tasks) > 0:
                        for task in tasks:
                            pos = isometric.isometric(
                                task.x, task.y, task.z, offset[0], offset[1]
                            )
                            if isinstance(task, player.Player):
                                task.real_x = pos[0]
                                task.real_y = pos[1]

                            try:
                                animation = task.obj.properties["frames"]
                                if animation == []:
                                    animation = None
                            except (TypeError, AttributeError, KeyError):
                                animation = None

                            image = task.image
                            if animation is not None:
                                image = level.animations_manager.tile(
                                    animation,
                                    str(task.obj.id),
                                    level.tmxdata,
                                    task.image,
                                )
                            self.surface.blit(image, pos)

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

                            if collider.type is not None:
                                level.movement_manager.collision[z].append((x, y))
                                level.movement_manager.collision[z].append(
                                    collider.type
                                )
                        except (KeyError, TypeError):
                            pass

        # Draws out-of-bounds entities in front of in-bounds geometry.
        for task in level.entity_manager.get_outside_front_entities(
            len(level.tile_layers[0].data[0]),
            len(level.tile_layers[0].data),
            len(level.tile_layers),
        ):
            pos = isometric.isometric(task.x, task.y, task.z, offset[0], offset[1])
            if isinstance(task, player.Player):
                task.real_x = pos[0]
                task.real_y = pos[1]

            try:
                animation = task.obj.properties["frames"]
                if animation == []:
                    animation = None
            except (TypeError, AttributeError, KeyError):
                animation = None

            image = task.image
            if animation is not None:
                image = level.animations_manager.tile(
                    animation, str(task.obj.id), level.tmxdata, task.image
                )
            self.surface.blit(image, pos)

        player_obj = level.entity_manager.entities[level.entity_manager.player]
        size = level.display.get_size()
        if player_obj.real_x <= padding:
            offset = (offset[0] + padding - player_obj.real_x, offset[1])
        elif player_obj.real_x >= size[0] - padding:
            offset = (offset[0] + size[0] - padding - player_obj.real_x, offset[1])
        if player_obj.real_y <= padding:
            offset = (offset[0], offset[1] + padding - player_obj.real_y)
        elif player_obj.real_y >= size[1] - padding:
            offset = (offset[0], offset[1] + size[1] - padding - player_obj.real_y)

        return offset
