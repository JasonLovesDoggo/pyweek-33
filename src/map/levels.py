from logging import getLogger

from pytmx.util_pygame import load_pygame
import pytmx
import src.utils.tools as tools
import src.gameobjects.entity as entity
import src.gameobjects.enemies as enemy
import src.utils.basic_controls as basic_controls
import src.rendering.render as render
import src.gameobjects.player as player
import src.rendering.animations as animations
import src.utils.audio as audio
import src.utils.isometric as isometric

log = getLogger(__name__)


class Level:
    def __init__(self, filename, config, screen_manager) -> None:
        # Load map
        self.current = screen_manager.current
        self.display = screen_manager.current.surface
        self.config = config
        self.filename = filename
        self.animations_manager = animations.Animation_manager()
        self.tmxdata = load_pygame(self.filename)
        self.tile_layers, self.non_tile_layers = tools.instance_getter(
            self.tmxdata.layers, pytmx.TiledTileLayer
        )

        log.info(
            f"""Loaded map: {self.tmxdata.filename}
            - Tile size: {self.tmxdata.tilewidth}x{self.tmxdata.tileheight}
            - Map size: {self.tmxdata.width}x{self.tmxdata.height}x{len(self.tile_layers)}
            - Map version: {self.tmxdata.version}
            - Tiled version: {self.tmxdata.tiledversion}\n"""
        )

        self.tiles_sorted = tools.sortFartestToClosest(self.tile_layers, self.tmxdata)

        # Load entities
        self.entity_count = 0
        self.player_pos = (0, 0)
        self.entity_manager = entity.EntityManager(self.animations_manager)
        for layer in self.non_tile_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    try:
                        ent_type = obj.type.lower()
                    except AttributeError:
                        ent_type = ""

                    x, y, z = (
                        (obj.x - layer.offsetx) / 10 - 1,
                        (obj.y - layer.offsety) / 10,
                        layer.offsety * -1 / 14,
                    )

                    if ent_type == "player":
                        self.entity_manager.add_entity(player.Player(x, y, z, obj))
                        self.player_pos = isometric.isometric(x, y, z)
                    elif ent_type == "enemy":
                        self.entity_manager.add_entity(enemy.Enemy(x, y, z, obj))
                    else:
                        self.entity_manager.add_entity(entity.Entity(x, y, z, obj))
                    self.entity_count += 1

        log.info(
            f'Loaded {self.entity_count} entit{"y" if self.entity_count == 1 else "ies"}.'
        )

        self.movement_manager = basic_controls.MovementManager(self.entity_manager)

        self.audio_manager = audio.AudioManager()

        self.render_manager = render.TileManager(self.display)

    def return_tile_grid(self):
        y = self.tmxdata.height
        x = self.tmxdata.width
        return x, y

    def switch_level(self, filename, screen_manager):
        log.debug(f"switching level to {filename} from {self.filename}")
        config = self.config
        movementFuncs = self.movement_manager.func

        newClass = Level(filename, config, screen_manager)

        newClass.movement_manager.func = movementFuncs
        return newClass

    def update(self):
        self.display = self.current.surface
        self.render_manager.surface = self.display
