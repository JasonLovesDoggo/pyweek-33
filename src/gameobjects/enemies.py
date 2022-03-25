import math

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from logging import getLogger

log = getLogger(__name__)


class Enemy:
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
        self.path_finding_matrix = []
        self.target = (4, 9, 1)

    def __str__(self) -> str:
        return f"Enemy: {self.x}, {self.y}, {self.z}"

    def calculate_binary_grid(self, level):
        collisions = level.movement_manager.collision[0]
        binary_grid = [
            [
                1 if (x, y) in collisions else 0
                for x in range(level.return_tile_grid()[0])
            ]
            for y in range(level.return_tile_grid()[1])
        ]

        return binary_grid

    def calculate_path(self, level):
        binary_grid = self.calculate_binary_grid(level)
        grid = Grid(matrix=binary_grid)

        if self.z_floor == math.floor(
            self.target[2]
        ):  # Path does not need to take stairs
            start = grid.node(self.x_floor(), self.y_floor())
            end = grid.node(self.target[0], self.target[1])
        else:  # Path does need to use stairs
            # Changeme!
            start = grid.node(self.x_floor(), self.y_floor())
            end = grid.node(self.target[0], self.target[1])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path = finder.find_path(start, end, grid)[0]
        print("path length:", len(path))
        print(grid.grid_str(path=path, start=start, end=end))

    def find_closest_elevator(level):
        for z, layer in enumerate(level.tile_layers):
            for y, row in enumerate(layer.data):
                for x in range(len(row)):
                    try:
                        if level.tmxdata.get_tile_properties(x, y, z)["elevator"]:
                            return (x, y, z)
                    except TypeError:
                        pass


def pathfind(level):
    for enemy in level.entity_manager.find_all_enemies():
        enemy.calculate_path(level)
