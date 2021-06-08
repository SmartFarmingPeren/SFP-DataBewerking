import numpy as np
from openalea.plantgl.math import Vector3

# List of all points in tree
points = []


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
        self.children = []
        self.point_cloud_points = []
        check = True
        # Checks to see if current point already exists
        for point in points:
            if point.vertex_id == self.vertex_id:
                check = False
        # If point does not exist
        if check:
            # Parent can be None if it is the first point
            if self.parent != None:
                # Add point_id to parents child list
                Point.get_from_id(self.parent).children.append(self)
            # Add current point to all point list
            points.append(self)

    def __str__(self):
        return "Point(Id: %d, Pos: %s, Dir: %s, Parent: %s, Radius: %f)" % (self.vertex_id,
                                                                            self.position,
                                                                            self.direction,
                                                                            self.parent,
                                                                            self.radius)

    @staticmethod
    def get_from_id(id):
        """
        Gets point object from id
        :param id: id of point
        :return: a Point object from points array
        """
        for point in points:
            if point.vertex_id == id:
                return point
        return None

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

    def distance_to(self, other_point: 'Point'):
        length = np.linalg.norm(self.position - other_point.position)
        return length

    @staticmethod
    def vector_distance_to(v1, v2):
        return np.linalg.norm(v1 - v2)

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
        # <<<<<<< HEAD
        #         vertex_x = vertex[0]
        #         vertex_y = vertex[1]
        #         vertex_z = vertex[2]
        #
        #         parent_x = parent[0]
        #         parent_y = parent[1]
        #         parent_z = parent[2]
        #
        #         direction = Vector3(vertex_x - parent_x, vertex_y - parent_y, vertex_z - parent_z)
        #         length = sqrt(direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2])
        #
        #         return direction / length
        # =======
        direction = Vector3(vertex - parent)
        direction.normalize()

        return direction
