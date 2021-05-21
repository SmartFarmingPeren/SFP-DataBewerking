import numpy as np
from openalea.plantgl.math import Vector3


class Point:
    """
    The point class is used to store the vertex information from a mtg vertex.
    """

    def __init__(self, vertex_id: int, position, direction, parent, radius: float):
        self.vertex_id = vertex_id
        self.position = Vector3(position) if position is not None else Vector3(0.0, 0.0, 0.0)
        self.parent_direction = Vector3(direction) if direction is not None else Vector3(0.0, 0.0, 0.0)
        self.child_direction = None
        self.radius = radius
        self.parent = parent
        self.child = None

    def __str__(self):
        return "Point(Id: %d, Pos: %s, Par_Dir: %s, Chi_Dir: %s Parent: %s, Child : %s, Radius: %f)" % (self.vertex_id,
                                                                        self.position,
                                                                        self.parent_direction,
                                                                        self.child_direction,
                                                                        self.parent,
                                                                        self.child,
                                                                        self.radius)

    def calculate_direction(self):


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

        return Point(vertex_id=vertex.get('vid'),
                     position=vertex.get('position'),
                     direction=None,
                     parent=vertex.get('parent'),
                     radius=radius)
