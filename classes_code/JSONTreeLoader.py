import json
import os.path

from classes_code.Branch import Branch
from classes_code.Point import Point
from classes_code.Tree import Tree
from openalea.plantgl.math import Vector3

directory = os.getcwd() + "\\outputs\\trees\\"


# Write Tree object to JSON; returns the JSON dictionary
def write(tree):
    """
    Writes a tree object to a JSON format.
    :param tree: A tree object.
    :return: json data.
    """
    data = {'root': write_branch(tree.get_root()),
            'branches': [],
            'point_cloud': tree.point_cloud_name}

    for branch in tree.get_branches():
        b_data = write_branch(branch)

        data['branches'].append(b_data)

    file = open(directory + tree.point_cloud_name.split(".")[0] + ".json", 'w')
    file.write(json.dumps(data))
    file.close()
    return data


def read(path: str = "tree_format.json"):
    """
    Reads a json tree object and imports it as a tree object.
    :param path: path to json
    :return: tree object
    """
    file = open(directory + path)
    content = file.read()
    file.close()
    tree = json.loads(content)
    branches = []
    root = read_branch(tree['root'])
    for branch in tree['branches']:
        branches.append(read_branch(branch))

    for branch in branches:
        branch.parent = find_by_id(branch.parent, branches)

    # get and concatenate all points from every branch
    points = [point for branch_points in [branch.points for branch in branches] for point in branch_points]

    for point in points:
        point.parent = find_by_id(point.parent, points)

    return Tree(input_point_cloud_name=tree['point_cloud'], root=root, branches=branches)


def write_branch(branch):
    """
    Writes a branch as a json format.
    :param branch: A branch object.
    :return: json data.
    """

    b_data = {'branch_id': branch.id,
              'age': branch.age,
              'depth': branch.depth,
              'is_leader': branch.is_leader,
              'points': [],
              'children': [],
              'parent': branch.parent.id if branch.parent is not None else "null"}
    for point in branch.points:
        b_data['points'].append(write_point(point))

    for child in branch.children:
        b_data['children'].append(child.id)

    return b_data


def read_branch(b_data):
    """
    Writes a branch as a json format.
    :param branch: A branch object.
    :return: json data.
    """

    points = []
    for point in b_data['points']:
        points.append(read_point(point))
    is_leader = b_data['is_leader']
    branch = Branch(branch_id=b_data['branch_id'],
                    depth=b_data['depth'],
                    points=points,
                    parent=b_data['parent'] if b_data['parent'] != "" else None,
                    age=b_data['age'])
    branch.is_leader = is_leader
    return branch


def write_point(point):
    p_data = {'point_id': point.vertex_id,
              'position': [point.position.x, point.position.y, point.position.z],
              'direction': [point.direction[0], point.direction[1], point.direction[2]],
              'radius': point.radius,
              'parent': point.parent if point.parent is not None else "null",
              'point_cloud_points': []}
    for vector3 in point.point_cloud_points:
        p_data['point_cloud_points'].append([vector3.x, vector3.y, vector3.z])
    return p_data


def read_point(p_data):
    point = Point(vertex_id=p_data['point_id'],
                  position=p_data['position'],
                  direction=p_data['direction'],
                  parent=p_data['parent'] if p_data['parent'] != "" else None,
                  radius=p_data['radius'] if p_data['radius'] != "" else 0.0)
    for pc_point in p_data['point_cloud_points']:
        point.point_cloud_points.append(Vector3([pc_point.x, pc_point.y, pc_point.z]))
    return point


def find_by_id(object_id: str, args):
    """
    finds a point/branch object by the given id.
    :param object_id: object id.
    :param args: objects
    :return: object.
    """
    for arg in args:
        if isinstance(arg, Branch):
            if arg.id == object_id:
                return arg
        elif isinstance(arg, Point):
            if arg.vertex_id == object_id:
                return arg


if __name__ == "__main__":
    read()
    pass
