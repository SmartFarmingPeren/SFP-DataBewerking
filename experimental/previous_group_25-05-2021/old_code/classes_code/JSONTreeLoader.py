import json
import os.path

from classes_code.Branch import Branch, Section
from classes_code.Tree import Tree

directory = os.getcwd() + "\\outputs\\trees\\"


def write(tree: Tree):
    # TODO write write
    pass


def read(path: str = directory + "tree_format.json"):
    file = open(path)
    content = file.read()
    file.close()
    tree = json.loads(content)
    print(tree)
    branches = []
    for branch in tree['branches']:
        sections = []
        for section in branch['sections']:
            section = Section(section['section_id'], section['position'], section['direction'],
                              section['parent'] if section['parent'] != "" else None)
            sections.append(section)
        branch = Branch(branch['branch_id'], branch['age'], sections,
                        branch['parent'] if branch['parent'] != "" else None)
        branches.append(branch)

    for branch in branches:
        branch.parent = find_by_id(branch.parent, branches)

    # get and concatenate all sections from every branch
    sections = [section for branch_sections in [branch.sections for branch in branches] for section in branch_sections]

    for section in sections:
        section.parent = find_by_id(section.parent, sections)

    return Tree(input_point_cloud_name=tree['point_cloud'], root=tree['root'], branches=branches)


def find_by_id(object_id: str, args):
    for arg in args:
        if arg.id == object_id:
            return arg


if __name__ == "__main__":
    read()
    pass
