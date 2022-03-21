from pytmx.util_pygame import load_pygame
import pytmx
from src.utils.tools import instance_getter
import src.gameobjects.entity as entity
import src.utils.input as input

class Level:
    def __init__(self, filename, config) -> None:
        # Load map
        self.config = config
        self.filename = filename
        self.tmxdata = load_pygame(self.filename)
        self.print_info = self.config['LOGGING']['PRINTLEVELINFO'].lower() == 'true'
        self.tile_layers, self.non_tile_layers = instance_getter(self.tmxdata.layers, pytmx.TiledTileLayer)
        if self.print_info:
            print(f'''Loaded map: {self.tmxdata.filename}
            - Tile size: {self.tmxdata.tilewidth}x{self.tmxdata.tileheight}
            - Map size: {self.tmxdata.width}x{self.tmxdata.height}x{len(self.tile_layers)}
            - Map version: {self.tmxdata.version}
            - Tiled version: {self.tmxdata.tiledversion}\n''')

        # Load entities
        self.entity_count = 0
        self.entity_manager = entity.EntityManager()
        for layer in self.non_tile_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    self.entity_manager.add_entity(entity.Entity((obj.x + 5) / 10, obj.y/10, (layer.offsety * -1 / 14) + 1, obj))
                    self.entity_count += 1
        if self.print_info:
            print(f'Loaded {self.entity_count} entit{"y" if self.entity_count == 1 else "ies"}.')

        self.movement = input.Movement(self.entity_manager)

    def switch_level(self, filename):
        config = self.config
        return Level(filename, config)