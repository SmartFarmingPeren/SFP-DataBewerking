import numpy as np
import vedo
import pathlib

from ctypes import *
from Branch import Branch
from classes_code.Point import Point, points
from utilities.debug_log_functions import debug_message, warning_message

CUT_DISTANCE = 10

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
                #print('asdfasdfasdfa')
                pruning_locations[len(pruning_locations) - 1].pruning_rule = 2
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
                        pruning_locations[len(pruning_locations) - 1].pruning_rule = 1
                        child.is_pruned = True
                    else:
                        debug_message("RULE 3: Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                        pruning_locations.append(cut_close_to_fork(child))
                        pruning_locations[len(pruning_locations) - 1].pruning_rule = 3
                        child.is_pruned = True
            else:
                warning_message("Child already pruned")

    elif branch.age >= 3:
        for child in branch.children:
            if not child.is_pruned:
                if child.age == 1:
                    debug_message("RULE 4: Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                    pruning_locations.append(cut_close_to_fork(child))
                    pruning_locations[len(pruning_locations) - 1].pruning_rule = 4
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


def cut_point_cloud_points(branches: [Branch]):
    """
    1. Vergelijk mtg punten met de snoeilocaties
    2. voor alle punten remove self and children
    3. write voor de overgebleven punten een pointcloud.
    """

    for location in pruning_locations:
        for branch in branches:
            for point in branch.points:
                if point.position == location.position:
                    debug_message("MTG POINT NEEDS TO BE PRUNED")
                    cut_point(point)

    f = open("gesnoeidboompie.xyz", "w")
    for point in points:
        for pc_point in point.point_cloud_points:
            f.write("{0} {1} {2}\n".format(pc_point.x, pc_point.z, pc_point.y,))
    f.close()


def cut_point(point : Point):
    for child in point.children:
        cut_point(child)
    if Point.get_from_id(point.vertex_id) == point:
        points.remove(point)
    debug_message("removed point {0}".format(point.vertex_id))


# TODO, redo using Cython https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html
def align_point_cloud_with_mtg(point_cloud, points):
    libname = str(pathlib.Path().absolute()) + "\classes_code\DBL.dll"
    c_lib = CDLL(libname)
    countArr = []

    arr = []
    for p in points:
        arr.append([p.position[0], p.position[1], p.position[2]])
    sendArray = (c_float * len(arr[0]) * len(arr))(*(tuple(i) for i in arr))

    for point in point_cloud:
        pointNum = c_lib.CloserTo(c_float(point[0]), c_float(point[1]), c_float(point[2]), sendArray, c_int(len(points)))
        closest_point = points[pointNum]
        closest_point.point_cloud_points.append(point)


def show_pruning_locations(ply):
    tree = vedo.Points([np.array([p.x, p.y, p.z]) for p in ply])
    tree.color([0.4, 0.2, 0], .8)
    tree.pointSize(1)
    locations = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in pruning_locations])
    locations.pointSize(10)

    locations.color([0, 1, .5])

    vedo.show([tree, locations], bg="Gray")

def show_pruning_locations_color(ply):
    tree = vedo.Points([np.array([p.x, p.y, p.z]) for p in ply])
    tree.color([0.4, 0.2, 0], .8)
    tree.pointSize(1)
    locations = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in pruning_locations])
    rule1 = []
    rule2 = []
    rule3 = []
    rule4 = []
    rule5 = []
    for p in pruning_locations:
        if p.pruning_rule is 1:
            rule1.append(p)
        if p.pruning_rule is 2:
            rule2.append(p)
        if p.pruning_rule is 3:
            rule3.append(p)
        if p.pruning_rule is 4:
            rule4.append(p)
        if p.pruning_rule is 5:
            rule5.append(p)

    rule1P = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in rule1])
    rule1P.pointSize(10)
    rule1P.color([1, 0, 0], 1)

    rule2P = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in rule2])
    rule2P.pointSize(10)
    rule2P.color([0, 1, 0], 1)

    rule3P = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in rule3])
    rule3P.pointSize(10)
    rule3P.color([0, 0, 1], 1)

    rule4P = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in rule4])
    rule4P.pointSize(10)
    rule4P.color([1, 1, 0], 1)

    rule5P = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in rule5])
    rule5P.pointSize(10)
    rule5P.color([1, 0, 1], 1)

    vedo.show([tree, rule1P, rule2P, rule3P, rule4P, rule5P], bg="Gray")

def show_cut_tree(pc):
    tree = vedo.Points([np.array([p.x, p.y, p.z]) for p in pc])
    tree.color([0.4, 0.2, 0], .8)
    tree.pointSize(1)
    locations = vedo.Points([np.array([p.position.x, p.position.y, p.position.z]) for p in pruning_locations])
    locations.pointSize(10)
    locations.color([0, 1, .5])
    #
    # vedo.show([tree], bg="Gray")


def write_locations_to_xyz(path):
    f = open(path, "w")
    for p in pruning_locations:
        f.write("%f %f %f\n" % (p.position.x, p.position.y, p.position.z))
    f.close()