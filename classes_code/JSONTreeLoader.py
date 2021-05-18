import json
import os.path

from classes_code.Branch import Branch
from classes_code.Point import Point
from classes_code.Tree import Tree

directory = os.getcwd() + "\\outputs\\trees\\"


# Write Tree object to JSON; returns the JOSN dictionary
def write(tree):
    data = {'root': get_json_root_data(tree),
            'branches': [],
            'point_cloud': tree.point_cloud_name}

    for branch in tree.get_branches():
        b_data = write_branch(branch)

        data['branches'].append(b_data)

    file = open(directory + "tree0.json", 'w')  # TODO add dynamic writing
    file.write(json.dumps(data))
    file.close()
    return data


def write_branch(branch):
    b_data = {'branch_id': branch.id,
              'age': branch.age,
              'points': [],
              'children': [],
              'parent': branch.parent.id if branch.parent is not None else "null"}
    for point in branch.points:
        p_data = {'point_id': point.vertex_id,
                  'position': [point.position.x, point.position.y, point.position.z],
                  'direction': [point.direction.x, point.direction.y, point.direction.z],
                  'radius': point.radius,
                  'parent': point.parent if point.parent is not None else "null"}
        b_data['points'].append(p_data)

    for child in branch.children:
        b_data['children'].append(child.id)

    return b_data


def get_json_root_data(tree):
    root = tree.get_root()
    r_data = {
        'root_id': root.id,
        'age': root.age,
        'points': [],
        'children': []}
    for root_point in root.points:
        rp_data = {
            'point_id': root_point.vertex_id,
            'position': [root_point.position.x, root_point.position.y, root_point.position.z],
            'direction': [root_point.direction.x, root_point.direction.y, root_point.direction.z],
            'radius': root_point.radius,
            'parent': root_point.parent if root_point.parent is not None else "null"
        }
        r_data['points'].append(rp_data)
    for child in root.children:
        r_data['children'].append(child.id)
    return r_data


def read(path: str = directory + "tree_format.json"):
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
        branch = Branch(branch['branch_id'], branch['age'], points,
                        branch['parent'] if branch['parent'] != "" else None)
        branches.append(branch)

    for branch in branches:
        branch.parent = find_by_id(branch.parent.id, branches)

    # get and concatenate all points from every branch
    points = [point for branch_points in [branch.points for branch in branches] for point in branch_points]

    for point in points:
        point.parent = find_by_id(point.parent, points)

    return Tree(input_point_cloud_name=tree['point_cloud'], root=tree['root'], branches=branches)


def find_by_id(object_id: str, args):
    for arg in args:
        if arg.id == object_id:
            return arg


if __name__ == "__main__":
    read()
    pass
