import math

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import src.map.levels as Level_info

from logging import getLogger

log = getLogger(__name__)


class Enemy:
    def __init__(self, x, y, z, obj):

        self.x = x
        self.y = y
        self.z = z
        self.real_x = None
        self.real_y = None
        self.x_floor = lambda: math.floor(self.x)
        self.y_floor = lambda: math.floor(self.y)
        self.z_floor = lambda: math.floor(self.z)
        self.obj = obj
        self.image = obj.image
        self.falling = False
        self.Matrix = []

    def __str__(self) -> str:
        return f"Enemy: {self.x}, {self.y}, {self.z}"

    def calculate_binary_grid(self, level):
        x, y = Level_info.Level.return_tile_grid(level)
        grid_before_rev = level.movement_manager.collision
        self.Matrix = [[1 for x in range(x)] for y in range(y)]
        for i, pos in enumerate(grid_before_rev[1]):
            if (i % 2) == 0:
                gy, gx = pos
                print(gy, gx)
                self.Matrix[gx][gy] = 0

    def calculate_path(self, level):
        self.calculate_binary_grid(self, level)
        grid = Grid(matrix=self.Matrix)

        start = grid.node(0, 0)
        end = grid.node(2, 9)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        print("operations:", runs, "path length:", len(path))
        print(grid.grid_str(path=path, start=start, end=end))

    def set_enemy_movement_properties(self, roam=True, speed=5):
        self.x = 1
