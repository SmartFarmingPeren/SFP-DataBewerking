from openalea.plantgl.math import Vector3
from math import sqrt


class Point:
    """
    The point class is used to store the vertex information from a mtg vertex.
    """

    def __init__(self, vertex_id: int, position, direction, parent, radius: float):
        self.vertex_id = vertex_id
        self.position = Vector3(position) if position is not None else Vector3(0.0, 0.0, 0.0)
        self.direction = Vector3(direction) if direction is not None else Vector3(0.0, 0.0, 0.0)
        self.radius = radius
        self.parent = parent

    def __str__(self):
        return "Point(Id: %d, Pos: %s, Dir: %s, Parent: %s, Radius: %f)" % (self.vertex_id,
                                                                            self.position,
                                                                            self.direction,
                                                                            self.parent,
                                                                            self.radius)

    @staticmethod
    def from_mtg(mtg, vertex_id):
        """
        :param mtg: a mtg
        :param vertex_id: A vertex from the mtg.
        :return: a Point object created from the vertex data.
        """
        vertex_obj = mtg.__getitem__(vertex_id)
        # Check if mtg has radius otherwise just say radius is 1
        if vertex_obj.get('radius') is None:
            radius = 0
        else:
            radius = vertex_obj.get('radius')
        parent = mtg.__getitem__(vertex_obj.get('parent'))
        if parent.get('vid') is not None:
            direction = Point.calculate_point_direction(vertex_obj.get('position'), parent.get('position'))
        else:
            direction = None
        point = Point(vertex_id=vertex_obj.get('vid'),
                      position=vertex_obj.get('position'),
                      direction=direction,
                      parent=parent.get('vid'),
                      radius=radius)
        return point

    @staticmethod
    def calculate_point_direction(vertex, parent):
        """
        Source: https://stackoverflow.com/questions/40077594/find-direction-of-given-x-y-z-cordinates

        The direction of a vector is usually defined by ignoring its length,
        or alternatively by setting its length to one.
        So we need to first define the length, which is

        L = √(x*x + y*y + z*z).

        We can define the vector

        x/L, y/L, z/L

        which points in the same direction as x,y,z but with length one.
        """
        vertex_x = vertex[0]
        vertex_y = vertex[1]
        vertex_z = vertex[2]

        parent_x = parent[0]
        parent_y = parent[1]
        parent_z = parent[2]

        direction = Vector3(vertex_x - parent_x, vertex_y - parent_y, vertex_z - parent_z)
        length = sqrt(direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2])

        return direction / length

