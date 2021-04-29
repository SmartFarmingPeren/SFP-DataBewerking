import numpy as np
from openalea.plantgl.math import Vector3


class Point:
    def __init__(self, vid: int, vector3: np.array, radius: float):
        self.vid = vid
        self.vector = Vector3(vector3) if vector3 is not None else Vector3(0.0, 0.0, 0.0)
        self.x = self.vector.x
        self.y = self.vector.y
        self.z = self.vector.z
        self.radius = radius

    def __str__(self):
        return "Point %d, [%.2f, %.2f, %.2f], radius %.2f" % (self.vid, self.z, self.y, self.z, self.radius)
