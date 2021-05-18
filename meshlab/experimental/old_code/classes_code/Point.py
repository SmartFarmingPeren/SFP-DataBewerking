import numpy as np
from openalea.plantgl.math import Vector3


class Point:
    """
    The point class is used to store the vertex information from a mtg vertex.
    """

    def __init__(self, vertex_id: int, vector3: np.array, parent, radius: float):
        self.vertex_id = vertex_id
        self.vector = Vector3(vector3) if vector3 is not None else Vector3(0.0, 0.0, 0.0)
        self.x = self.vector.x
        self.y = self.vector.y
        self.z = self.vector.z
        self.radius = radius
        self.parent = parent

    def __str__(self):
        return "Point(Vertex id = {0}, [x = {1}, y = {2}," \
               " z = {3}], parent = {4},  radius = {5})".format(self.vertex_id,
                                                                self.x,
                                                                self.y,
                                                                self.z,
                                                                self.parent,
                                                                self.radius)
        # return "Point %d, [%.2f, %.2f, %.2f], radius %.2f" % (self.vertex_id, self.z, self.y, self.z, self.radius)

    @staticmethod
    def from_mtg(vertex):
        """
        :param vertex: A vertex from the mtg.
        :return: a Point object created from the vertex data.
        """

        # Check if mtg has radius otherwise just say radius is 1
        if vertex.get('radius') is None:
            radius = 0
        else:
            radius = vertex.get('radius')

        return Point(vertex.get('vid'), vertex.get('position'), vertex.get('parent'), radius)
