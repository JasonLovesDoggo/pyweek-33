import math


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

    def __str__(self) -> str:
        return f"Enemy: {self.x}, {self.y}, {self.z}"
