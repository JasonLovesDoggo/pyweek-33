import math
from logging import getLogger

import src.gameobjects.player as player

log = getLogger(__name__)


class EntityManager:
    def __init__(self):
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
        log.debug(f"adding entity: {entity}")
        for existing_entity in self.entities:
            if existing_entity.z < entity.z:
                self.entities.insert(self.entities.index(existing_entity), entity)
                copy = self.entities
                copy.reverse()
                self.find_player_index()
                return self.entities
            elif existing_entity.z == entity.z:
                if existing_entity.y < entity.y:
                    self.entities.insert(self.entities.index(existing_entity), entity)
                    self.find_player_index()
                    return self.entities
                elif existing_entity.y == entity.y:
                    if existing_entity.x <= entity.x:
                        self.entities.insert(
                            self.entities.index(existing_entity), entity
                        )
                        self.find_player_index()
                        return self.entities
        # If it reaches this point, append to end.
        self.entities.append(entity)

    def remove_entity(self, entity):
        log.debug(f"removing entity: {entity}")
        self.entities.remove(entity)
        self.find_player_index()
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
