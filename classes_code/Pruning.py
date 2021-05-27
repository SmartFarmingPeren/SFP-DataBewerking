from classes_code.Branch import Branch

# zoeken naar snoeiacties per tak

# knip takken bij het eind

# knip takken bij het begin

# return positions as ply?

# krijg de lengte van een tak

# krijg een punt op de tak vanaf lengte
from classes_code.Point import Point, points


def get_branch_length(branch: Branch):
    length = 0.0
    p: Point
    prev_p = None
    for p in branch.points:
        if prev_p is not None:
            length += p.distance_to(prev_p)
        prev_p = p
    return length

