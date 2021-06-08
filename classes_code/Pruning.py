import numpy as np
import vedo

from Branch import Branch
from classes_code.Point import Point
from utilities.debug_log_functions import debug_message, warning_message

CUT_DISTANCE = 1.0

pruning_locations = []

'''
Pruning rules:
[1.] If a one year old branch comes from a two year old branch, 
        the  branch needs to be cut about 5 cm from the fork.

[2.] If a one year old branch forks from a leader, 
        the branch needs to be cut 5 cm from the top.

[3.] When more than one branch spring from a two year old branch, 
        the branch from the fork will be cut 5 cm from the fork and the others close to the branch it grown from.

[4.] If new branches spring from a 3+ year old branch, 
        the branch needs to be cut close to the fork as well.
'''


def prune_branch(branch: Branch):
    if branch.age == 1:
        if not branch.is_pruned:
            if branch.parent.is_leader:
                debug_message(
                    "RULE 2: Branch age:{0}, Parent is leader:{1}".format(branch.age, branch.parent.is_leader))
                pruning_locations.append(cut_distance_from_top(branch))
                branch.is_pruned = True
        else:
            warning_message("Child already pruned")

    elif branch.age == 2:
        first_child_found = False
        for child in branch.children:
            if not child.is_pruned:
                if child.age == 1:
                    if not first_child_found:
                        first_child_found = True
                        debug_message("RULE 1(RULE3): Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                        pruning_locations.append(cut_distance_from_fork(child))
                        child.is_pruned = True
                    else:
                        debug_message("RULE 3: Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                        pruning_locations.append(cut_close_to_fork(child))
                        child.is_pruned = True
            else:
                warning_message("Child already pruned")

    elif branch.age >= 3:
        for child in branch.children:
            if not child.is_pruned:
                if child.age == 1:
                    debug_message("RULE 4: Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                    pruning_locations.append(cut_close_to_fork(child))
                    child.is_pruned = True
            else:
                warning_message("Child already pruned")


def cut_close_to_fork(branch):
    return get_branchpoint_by_distance(branch, 0)
    # info_message("SAME AS 4: Branch cut close to the fork [RULE 3/4]")


def cut_distance_from_fork(branch):
    return get_branchpoint_by_distance(branch, CUT_DISTANCE)
    # info_message("Branch cut 5cm from the fork [RULE 1]")


def cut_distance_from_top(branch):
    return get_branchpoint_by_distance(branch, get_branch_length(branch) - CUT_DISTANCE)
    # info_message("Branch is 1 year and connected to a leader [RULE 2]")


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
            if length + p_dist >= distance:
                if abs(length - distance) < abs(length + p_dist - distance):
                    return prev_p
                else:
                    return p
            length += p_dist
        prev_p = p
    return prev_p


def show_pruning_locations(ply):
    tree = vedo.Points([np.array([p.x, p.y, p.z]) for p in ply])
    tree.color([0.4, 0.2, 0], .8)
    tree.pointSize(1)
    locations = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in pruning_locations])
    locations.pointSize(10)
    locations.color([0, 1, .5])

    vedo.show([tree, locations], bg="Gray")\

def cut_point_cloud_points(branches: [Branch]):
    """
    1. Vergelijk mtg punten met de snoeilocaties
    2. voor alle punten remove self and children
    3. write voor de overgebleven punten een pointcloud.
    """
    for location in pruning_locations:
        print(location)
        for branch in branches:
            print(branch.points.index(location))
            # for point in branch.points:
            #     print("\n\n\n")
            #     print(point)
            #     print(branch.points.index(point))
            #     print(branch.points[branch.points.index(point)])
            #     print("\n\n\n")
                # if point.position == location.position:




# TODO, redo using Cython https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html
def align_point_cloud_with_mtg(point_cloud, points):
    for point in point_cloud:
        closest_point = points[0]
        distance = 10000000000
        for mtg_point in points:
            new_distance = Point.vector_distance_to(point, mtg_point.position)
            if(new_distance < distance):
                distance = new_distance
                closest_point = mtg_point
        closest_point.point_cloud_points.append(point)
    for mtg_point in points:
        print(mtg_point.point_cloud_points)

    # """"TODO"""
    # pc: np.array = np.asarray(point_cloud).copy()
    #
    # pc = sorted(pc, key=lambda p: p[0], reverse=False)
    #
    # i = 0
    # while pc[i][0]:
    #     i += 1
    #
    #
    # print(pc)
    # # for point in point_cloud:
    # #     closest_point = points[0]
    # #     distance = 10000000000
    # #     for mtg_point in pts[0:10]:
    # #         new_distance = Point.vector_distance_to(point, mtg_point.position)
    # #         if(new_distance < distance):
    # #             distance = new_distance
    # #             closest_point = mtg_point
    # #     closest_point.point_cloud_points.append(point)
    # #     # print(closest_point)
    # # for mtg_point in points:
    # #     print(mtg_point.point_cloud_points)