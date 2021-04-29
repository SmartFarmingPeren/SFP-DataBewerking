from openalea.plantgl.math import Vector3


class Point:
    def __init__(self, vid, vector3, radius):
        self.vid = vid
        self.vector = Vector3(vector3)
        self.x = self.vector.x
        self.y = self.vector.y
        self.z = self.vector.z
        self.radius = radius
