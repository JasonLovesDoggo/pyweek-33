import math
from logging import getLogger

import src.gameobjects.player as player

log = getLogger(__name__)


class EntityManager:
    def __init__(self, animations_manager):
        self.animations_manager = animations_manager
        self.entities = []
        self.player = None

    def get_tasks(self, x, y, z):
        found = False
        tasks = []
        for entity in self.entities:
            if (
                math.floor(entity.x) == x
                and math.floor(entity.y) == y
                and math.floor(entity.z) == z
            ):
                found = True
                tasks.append(entity)
            elif found:
                break
        return tasks

    def find_player_index(self):
        for index, entity in enumerate(self.entities):
            if isinstance(entity, player.Player):
                self.player = index
                return index
        return 0

    def get_outside_back_entities(self):
        outside_tiles = []
        for entity in self.entities:
            if entity.x < 0 or entity.y < 0 or entity.z < 0:
                outside_tiles.append(entity)
        return outside_tiles

    def get_outside_front_entities(self, x, y, z):
        outside_tiles = []
        for entity in self.entities:
            if entity.x > x or entity.y > y or entity.z > z:
                outside_tiles.append(entity)
        return outside_tiles

    def add_entity(self, entity):
        self.entities.append(entity)
        self.find_player_index()
        log.debug(f"Added entity: {entity}")

        return self.entities

    def remove_entity(self, entity):
        self.animations_manager.z_dict.pop(str(self.obj.id))
        self.entities.remove(entity)
        self.find_player_index()
        log.debug(f"Removed entity: {entity}")

        return self.entities


class Entity:
    def __init__(self, x, y, z, obj):
        self.x = x
        self.y = y
        self.z = z
        self.x_floor = lambda: math.floor(self.x)
        self.y_floor = lambda: math.floor(self.y)
        self.z_floor = lambda: math.floor(self.z)

        self.obj = obj
        self.image = obj.image
        self.falling = False

    def __str__(self) -> str:
        return f"Entity: {self.x}, {self.y}, {self.z}"
