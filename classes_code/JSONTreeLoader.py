import json
import os.path

from classes_code.Branch import Branch
import json

directory = os.getcwd() + "\\outputs\\trees\\"


# Write Tree object to JSON; returns the JOSN dictionary
def write(tree):
    data = {'root': '32',
            'branches': [],
            'point_cloud': tree.point_cloud_name}
    for branch in tree.branches:
        b_data = {'branch_id': branch.id,
                  'age': branch.age,
                  'points': [],
                  'children': [],
                  'parent': branch.parent}
        for point in branch:
            p_data = {'id': point.vid,
                      'position': [],
                      'direction': [],
                      'radius': point.radius,
                      'parent': point.parent}
            b_data['points'].append(p_data)

        data['branches'].append(b_data)
    print(json.dumps(data))
    return data


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
            point = Section(point['point_id'], point['position'], point['direction'],
                              point['parent'] if point['parent'] != "" else None)
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
