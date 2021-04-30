import numpy as np

from classes_code.Point import Point


class Branch:
    def __init__(self, points: [], age: int, parent: 'Branch' = None):
        # First section is at the start of the branch, last section is at the end
        # vertex IDs of the connected points
        self.points = points
        self.children = []
        self.parent = parent
        self.age = age

    def next(self, point: Point):
        """
        Creates a new branch with age 1 and gives it the first section
        :rtype: Returns the newly generated branch
        """
        new_branch = Branch(age=1, parent=self)
        new_branch.points.append(point)
        self.children.append(new_branch)
        return new_branch

    def add_section(self):
        """
        Adds a new section to an existing branch
        """
        self.sections.append(self.get_last_section().next())


def get_next(node):
    yield node
    for child in node.children:
        yield from get_next(child)


class Section:
    def __init__(self, pos, direction, parent, thickness=1):
        self.pos: np.array = pos
        self.direction: np.array = direction
        self.thickness: int = thickness
        self.count: int = 0
        self.parent = parent

    def next(self):
        """
        This function is used to determine the next position of a section of the tree.
        :rtype: It returns a section with a position and a direction
        """
        # new_dir = self.direction + next_direction
        next_dir = self.direction * SECTION_LENGTH
        for count in range(0, 3):
            if next_dir[count] > THRESHOLD:
                next_dir[count] = THRESHOLD
            if next_dir[count] < -THRESHOLD:
                next_dir[count] = -THRESHOLD
        next_pos = self.pos + next_dir
        self.add_thickness()
        return Section(pos=next_pos, direction=self.direction, parent=self)

    def reset(self):
        """
        This function is used to reset the direction of a section
        """
        self.direction = self.orig_dir
        self.count = 0

    def add_thickness(self):
        """
        With this function the thickness of the previous section is increased so the older the branch to thicker it gets
        """
        self.thickness += ADD_THICKNESS_VALUE
        if self.parent is not None:
            self.parent.add_thickness()

    def __str__(self):
        return "Section; position: [%.2f, %.2f, %.2f]" % (self.pos[0], self.pos[1], self.pos[2])
