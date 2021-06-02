import json
import os.path

from classes_code.Branch import Branch
from classes_code.Point import Point
from classes_code.Tree import Tree

directory = os.getcwd() + "\\outputs\\trees\\"


# Write Tree object to JSON; returns the JSON dictionary
def write(tree):
    """
    Writes a tree object to a JSON format.
    :param tree: A tree object.
    :return: json data.
    """
    data = {'root': write_branch(tree.get_root()),
            'leaders': [],
            'branches': [],
            'point_cloud': tree.point_cloud_name}

    for leader in tree.get_leaders():
        l_data = write_branch(leader)

        data['leaders'].append(l_data)

    for branch in tree.get_non_leaders():
        b_data = write_branch(branch)

        data['branches'].append(b_data)

    file = open(directory + tree.point_cloud_name.split(".")[0] + ".json", 'w')
    file.write(json.dumps(data))
    file.close()
    return data


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
        p_data = {'point_id': point.vertex_id,
                  'position': [point.position.x, point.position.y, point.position.z],
                  'direction': [point.direction[0], point.direction[1], point.direction[2]],
                  'radius': point.radius,
                  'parent': point.parent if point.parent is not None else "null"}
        b_data['points'].append(p_data)

    for child in branch.children:
        b_data['children'].append(child.id)

    return b_data


def read(path: str = directory + "tree_format.json"):
    """
    Reads a json tree object and imports it as a tree object.
    :param path: path to json
    :return: tree object
    """
    file = open(path)
    content = file.read()
    file.close()
    tree = json.loads(content)
    print(tree)
    branches = []
    for branch in tree['branches']:
        points = []
        for point in branch['points']:
            point = Point(vertex_id=point['point_id'],
                          position=point['position'],
                          direction=point['direction'],
                          parent=point['parent'] if point['parent'] != "" else None,
                          radius=point['radius'] if point['radius'] != "" else 0.0)
            points.append(point)
        is_leader = branch['is_leader']
        branch = Branch(branch_id=branch['branch_id'],
                        depth=branch['depth'],
                        points=points,
                        parent=branch['parent'] if branch['parent'] != "" else None,
                        age=branch['age'])
        branch.is_leader = is_leader
        branches.append(branch)

    for branch in branches:
        branch.parent = find_by_id(branch.parent.id, branches)

    # get and concatenate all points from every branch
    points = [point for branch_points in [branch.points for branch in branches] for point in branch_points]

    for point in points:
        point.parent = find_by_id(point.parent, points)

    return Tree(input_point_cloud_name=tree['point_cloud'], root=tree['root'], branches=branches)


def find_by_id(object_id: str, args):
    """
    finds a point/branch object by the given id.
    :param object_id: object id.
    :param args: objects
    :return: object.
    """
    for arg in args:
        if arg.id == object_id:
            return arg


if __name__ == "__main__":
    read()
    pass
