import numpy as np

from classes_code.Point import Point


class Branch:
    def __init__(self, branch_id, age: int, points: [], parent: 'Branch' = None):
        # First section is at the start of the branch, last section is at the end
        # vertex IDs of the connected points
        self.id = branch_id
        self.points = points
        self.children = []
        self.parent = parent
        self.age = age
        # TODO add branch direction(17-05-2021)

    def next(self, point: Point):
        pass

    def __str__(self):
        return "%s: \n" \
               "Age: %d \n" \
               "Parent: %s \n" \
               "Children" "%s \n"\
               "Points: \n \t %s" % (self.id, self.age, self.parent, self.children, [section.__str__() for section in self.points])
        pass

    # start_point is always a +N point of the branch
    def determine_branch(self, mtg, start_point):
        print(start_point)
        """
        Start from root
        Branch start = root point
        for each point with 1 child, save point
        if point > 1 child end root branch
        save +N branches

        for n+ branch in n+ branches:
            save each point with 1 child
            save n+ points

        This needs to be done recursively until the end points are reached
            for n+ branch in n+ branches:
                save each point with 1 child
                save n+ points
        """

        # Create branch points, first one being the start_point
        branch_points = [Point.from_mtg(mtg.__getitem__(start_point))]
        next_point = start_point

        # glorious while True by Luca
        while True:
            # get all children of start_point
            children = [mtg.__getitem__(child) for child in mtg.Sons(next_point)]
            # if point is the last
            if len(children) <= 0:
                break
            # if point has single child
            elif len(children) == 1:
                # create point from child, move up
                child = children[0]
                branch_points.append(Point.from_mtg(child))
                next_point = child.get('vid')
            # if point has more than 1 child
            elif len(children) >= 1:
                has_single_child = False
                for child in children:
                    # print("for children: %d, %d" % (next_point, start_point))
                    # print("child of child %s" % (mtg.Sons(child.get('vid'))))
                    # if child is a new start_point
                    if child.get('edge_type') == '+':
                        # print(child)
                        self.children.append(self.determine_branch(mtg, child.get('vid')))
                    # if child is a continuation (same as for single children)
                    else:
                        # create point from child, move up
                        branch_points.append(Point.from_mtg(child))
                        next_point = child.get('vid')
                        has_single_child = True
                if not has_single_child:
                    break

        branch = Branch(branch_id="branch_" + str(start_point), age=self.age + 1, points=branch_points,
                        parent=branch_points[0].parent)
        print("\n {0} \n".format(branch))
        return branch


def get_next(node):
    yield node
    for child in node.children:
        yield from get_next(child)
