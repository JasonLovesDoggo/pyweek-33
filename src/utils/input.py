import math

# Reactivate this when death screen is done.
# from src.utils.tools import is_negative
from logging import getLogger

log = getLogger(__name__)


class MovementManager:
    def __init__(self, entity_manager, collisions=[], speed=10, gravity=3):
        self.func = []
        self.entity_manager = entity_manager
        self.collision = collisions
        self.player_id = entity_manager.find_player_index()
        self.player = entity_manager.entities[self.player_id]

        try:
            self.player_ground_collision_layer = self.collision[
                self.player.z_floor() - 1
            ]
        except IndexError:
            self.player_ground_collision_layer = []
        try:
            self.player_collision_layer = self.collision[self.player.z_floor()]
        except IndexError:
            self.player_collision_layer = []

        self.player_speed = speed
        self.gravity_speed = gravity

    def add(self, code, func):
        self.func.append({"code": code, "func": func})

    def update(self, entity_manager):
        self.entity_manager = entity_manager
        self.player_id = entity_manager.find_player_index()
        self.player = entity_manager.entities[self.player_id]
        try:
            self.player_ground_collision_layer = self.collision[
                self.player.z_floor() - 1
            ]
        except IndexError:
            self.player_ground_collision_layer = []
        try:
            self.player_collision_layer = self.collision[self.player.z_floor()]
        except IndexError:
            self.player_collision_layer = []

    def run(self, keys, entity_manager, delta_time, offset):
        self.update(entity_manager)

        used = []
        for func in self.func:
            if keys[func["code"]] and func["func"] not in used:
                used.append(func["func"])
                if self.player.falling:
                    continue
                func["func"](delta_time)

        self.gravity(delta_time)

        return offset

    def gravity(self, delta_time):
        if (
            self.player.x_floor(),
            self.player.y_floor(),
        ) not in self.player_ground_collision_layer:
            self.player.falling = True
            self.player.z -= self.gravity_speed * delta_time
            # Reactivate this when death screen is done.
            # if is_negative(self.player.z):
            #     self.player.deadcount += 1
            #     if self.player.deadcount > 40:
            #         pass  # implement death/title screen
            #     pass
        else:
            self.player.falling = False

    def UP(self, delta_time):
        local_speed = self.player_speed * delta_time
        target = (self.player.x_floor(), math.floor(self.player.y - local_speed))
        if target not in self.player_collision_layer:
            self.player.y -= local_speed
        else:
            target_type = self.player_collision_layer[
                self.player_collision_layer.index(target) + 1
            ]
            if target_type == "solid":
                pass
            elif target_type == "stairs_north":
                # go up stairs
                pass
            elif "stairs" in target_type:
                pass

    def DOWN(self, delta_time):
        local_speed = self.player_speed * delta_time
        target = (self.player.x_floor(), math.floor(self.player.y + local_speed))
        if target not in self.player_collision_layer:
            self.player.y += local_speed
        else:
            target_type = self.player_collision_layer[
                self.player_collision_layer.index(target) + 1
            ]
            if target_type == "solid":
                pass
            elif target_type == "stairs_south":
                # go up stairs
                pass
            elif "stairs" in target_type:
                pass

    def LEFT(self, delta_time):
        local_speed = self.player_speed * delta_time
        target = (math.floor(self.player.x - local_speed), self.player.y_floor())
        if target not in self.player_collision_layer:
            self.player.x -= local_speed
        else:
            target_type = self.player_collision_layer[
                self.player_collision_layer.index(target) + 1
            ]
            if target_type == "solid":
                pass
            elif target_type == "stairs_east":
                # go up stairs
                pass
            elif "stairs" in target_type:
                pass

    def RIGHT(self, delta_time):
        local_speed = self.player_speed * delta_time
        target = (math.floor(self.player.x + local_speed), self.player.y_floor())
        if target not in self.player_collision_layer:
            self.player.x += local_speed
        else:
            target_type = self.player_collision_layer[
                self.player_collision_layer.index(target) + 1
            ]
            if target_type == "solid":
                pass
            elif target_type == "stairs_west":
                # go up stairs
                pass
            elif "stairs" in target_type:
                pass