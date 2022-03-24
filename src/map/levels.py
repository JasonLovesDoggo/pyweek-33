from logging import getLogger

from pytmx.util_pygame import load_pygame
import pytmx
import src.utils.tools as tools
import src.gameobjects.entity as entity
import src.gameobjects.enimies as enemy
import src.utils.input as input
import src.rendering.render as render
import src.gameobjects.player as player
import src.rendering.animations as animations
import src.utils.audio as audio

log = getLogger(__name__)


class Level:
    def __init__(self, filename, config, display) -> None:
        # Load map
        self.display = display
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
        self.entity_manager = entity.EntityManager(self.animations_manager)
        for layer in self.non_tile_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    try:
                        type = obj.type.lower()
                    except AttributeError:
                        type = ""

                    x, y, z = (
                        (obj.x - layer.offsetx) / 10 - 1,
                        (obj.y - layer.offsety) / 10,
                        layer.offsety * -1 / 14,
                    )

                    if type != "player":
                        self.entity_manager.add_entity(player.Player(x, y, z, obj))
                    elif type != "enemy":
                        self.entity_manager.add_entity(enemy.Enemy(x, y, z, obj))
                    else:
                        self.entity_manager.add_entity(entity.Entity(x, y, z, obj))
                    self.entity_count += 1

        log.info(
            f'Loaded {self.entity_count} entit{"y" if self.entity_count == 1 else "ies"}.'
        )

        self.movement_manager = input.MovementManager(self.entity_manager)

        self.audio_manager = audio.AudioManager()

        self.render_manager = render.TileManager(display)

    def switch_level(self, filename):
        log.debug(f"switching level to {filename} from {self.filename}")
        config = self.config
        display = self.display
        movementFuncs = self.movement_manager.func

        newClass = Level(filename, config, display)

        newClass.movement_manager.func = movementFuncs
        return newClass

    def update(self):
        self.renderer.surface = self.display
