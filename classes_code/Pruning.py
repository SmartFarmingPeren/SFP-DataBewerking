from classes_code.Branch import Branch

# zoeken naar snoeiacties per tak

# knip takken bij het eind

# knip takken bij het begin

# return positions as ply?

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


# returns the closest point to distance from the first point of the branch
def get_branchpoint_by_distance(branch, distance):
    length = 0.0
    p: Point
    prev_p = None
    for p in branch.points:
        if prev_p is not None:
            # p_dist distance between 2 points
            p_dist = p.distance_to(prev_p)
            print("len_prev: %f, length_curr: %f" % (length, length + p_dist))
            if length + p_dist >= distance:
                if abs(length - distance) < abs(length + p_dist - distance):
                    return prev_p
                else:
                    return p
            length += p_dist
        prev_p = p
    return prev_p

def show_pruning_locations(ply, pruning_points):
    pass

