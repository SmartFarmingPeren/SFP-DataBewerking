from numpy import sqrt
from openalea.plantgl.math import Vector3


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

    direction = direction/length

    pyto = sqrt(direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2])

    return direction





calculate_point_direction([3,3,5], [1,3,0])