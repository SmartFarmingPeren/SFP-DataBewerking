from classes_code.Point import Point


class Branch:
    """
    The branch class is used to contain all points connected to a branch.
    """

    def __init__(self, branch_id, depth: int, points: [], parent: 'Branch' = None, age: int = -1, is_leader=False):
        # First section is at the start of the branch, last section is at the end
        # vertex IDs of the connected points
        self.id = branch_id
        self.points = points
        self.children = []
        self.parent = parent
        self.depth = depth
        self.age = age
        self.is_leader = is_leader

    def next(self, point: Point):
        """
        TODO: not implemented yet.
        Gets the next point connected to a point.
        :param point: a point object.
        """
        pass

    def __str__(self):
        """
        This function makes it possible to do a print(branch).
        :return: a string.
        """
        return "%s: \n" \
               "Age: %d \n" \
               "Parent: %s \n" \
               "Children" "%s \n" \
               "Points: \n \t %s" % (
                   self.id, self.age, self.parent, self.children, [section.__str__() for section in self.points])
        pass

    # start_point is always a +N point of the branch
    def determine_branch(self, mtg, start_point):
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
        self.points = [Point.from_mtg(mtg, start_point)]
        # self.points = []
        current_point = start_point

        # glorious while True by Luca
        while True:
            # get all children of start_point
            children = [mtg.__getitem__(child) for child in mtg.Sons(current_point)]
            # if point is the last
            if len(children) <= 0:
                break
            # if point has single child
            elif len(children) == 1:
                # create point from child, move up
                child = children[0]
                self.points.append(Point.from_mtg(mtg, child.get('vid')))
                current_point = child.get('vid')
                continue
            # if point has more than 1 child
            elif len(children) >= 1:
                old_point = current_point
                for child in children:
                    # if child is a new start_point
                    if child.get('edge_type') == '+':
                        # print(child)
                        branch = Branch(branch_id="branch_{0}".format(child.get('vid')),
                                        depth=self.depth + 1,
                                        points=[],
                                        parent=self)
                        branch.determine_branch(mtg, child.get('vid'))
                        self.children.append(branch)
                    # if child is a continuation (same as for single children)
                    else:
                        # create point from child, move up
                        self.points.append(Point.from_mtg(mtg, child.get('vid')))
                        current_point = child.get('vid')
                        continue
                if old_point == current_point:
                    break


def get_next(node):
    """
    Gets the next points.
    :param node: Point.
    """
    yield node
    for child in node.children:
        yield from get_next(child)
