import openalea.plantscan3d.serial as serial

from classes_code.Branch import Branch, get_next
from classes_code.Point import Point
from classes_code.Pruning import get_branch_length, get_branchpoint_by_distance, prune_branch, show_pruning_locations
from classes_code.Skeletonization import create_scene_and_skeletonize
from graphs.visual import *
from utilities.configuration_file import *

leader_threshold = 5

class Tree:
    """
    The tree class is used to load a point cloud, then skeletonize the point cloud.
    After that the created MTG file will be split into: root, leaders, branches and points.
    The tree class is a collection for these items.
    """

    def __init__(self, input_point_cloud_name, root=None, branches=None):
        # During the skeletonize a mtg file is created from a point cloud, both are saved for later use
        self.point_cloud_name = input_point_cloud_name
        self.point_cloud, self.mtg = create_scene_and_skeletonize(input_point_cloud_name)

        # Determine the root branch
        self.root_branch = root if root is not None else self.determine_root(self.mtg)

        self.tree_start = []
        for point in self.mtg.Sons(self.root_branch.points[-1].vertex_id):
            # # Determine the branch end points
            branch = Branch(branch_id="branch_{0}".format(point), depth=1,
                                     points=[],
                                     parent=self.root_branch)
            branch.determine_branch(self.mtg, point)
            self.tree_start.append(branch)

        self.determine_leaders()

        get_branch_length(self.get_branches()[5])

        print(get_branchpoint_by_distance(self.get_branches()[5], get_branch_length(self.get_branches()[5]) - 2))
        # get_pruning_type(self.get_branches()[2])
        self.determine_age()

        for branch in self.get_branches():
            prune_branch(branch)

        show_pruning_locations(self.point_cloud)


        # Export the generated skeleton as a mtg file and save it under the input file name
        serial.writeMTGfile(OUTPUT_MTG_DIR + input_point_cloud_name.split(".")[0] + '.mtg',
                            serial.convertToStdMTG(self.mtg))

        # Export a graph as a .html file
        plot(self.mtg, OUTPUT_GRAPHS_DIR + input_point_cloud_name.split(".")[0] + '.html')

    @staticmethod
    def determine_root(mtg):
        """
        This function determines the root of a tree
        If there is a small branch on the root this code wont work, in future we need to improve this method.
        :param mtg:
        """
        lowest_vertex, highest_vertex = Tree.determine_vertexes(mtg)
        root_branch = []
        branches_on_root = []
        temp_branch = []
        end_of_root = 0
        just_a_branch = 0
        for point in range(lowest_vertex, highest_vertex + 1):
            # Check if mtg has radius otherwise just say radius is 1
            try:
                radius = mtg.property('radius')[point]
            except Exception as e:
                # error_message(e)
                radius = 0
            try:
                parent = mtg.property('parent')[point]
            except Exception as e:
                # error_message(e)
                parent = -1
            # If a point has more than 1 son only append the last point then break out of the loop.
            if len(mtg.Sons(point)) == 1:
                # TODO direction TBD
                root_branch.append(Point.from_mtg(mtg, point))
            else:
                # TODO direction TBD
                root_branch.append(Point.from_mtg(mtg, point))
                # Check if the branch itself has more branches on it, if not it's just an extra branch on the root
                for cp in mtg.Sons(point):
                    current_point = cp
                    temp_branch.append(current_point)
                    while True:
                        if len(mtg.Sons(current_point)) == 1:
                            current_point = mtg.Sons(current_point)[0]
                            temp_branch.append(current_point)
                        elif len(mtg.Sons(current_point)) == 0:
                            temp_branch_on_root = []
                            for point in temp_branch:
                                temp_branch_on_root.append(Point.from_mtg(mtg, point))
                            branches_on_root.append(
                                Branch(branch_id="branch_" + str(temp_branch[0]), depth=1, points=temp_branch_on_root))
                            just_a_branch = 1
                            break
                        else:
                            end_of_root += 1
                            break
                    if just_a_branch:
                        break
            if end_of_root >= 2:
                break
            else:
                end_of_root = 0
                just_a_branch = 0

        branch = Branch(branch_id="branch_" + str(lowest_vertex), depth=0, points=root_branch)
        for child in branches_on_root:
            child.parent = branch
        branch.children = branches_on_root
        return branch

    @staticmethod
    def determine_vertexes(mtg):
        """
        This function determines the lowest and highest vertex point.
        :param mtg: a mtg file
        :return: lowest_vertex, highest_vertex
        """
        highest_vertex = 0
        lowest_vertex = float('inf')
        for point in mtg.property('position'):
            if point > highest_vertex:
                highest_vertex = point
            if point < lowest_vertex:
                lowest_vertex = point
        return lowest_vertex, highest_vertex

    def get_branch_ends(self):
        """
        This function gets the end vertexes of the tree.
        These endpoints will be used to determine branch age later.
        :return: end_points = [Point]
        """
        lowest_vertex, highest_vertex = Tree.determine_vertexes(self.mtg)
        end_points = []
        for vertex_id in range(lowest_vertex, highest_vertex + 1):
            if len(self.mtg.Sons(vertex_id)) == 0:
                # debug_message("End point found at {0}".format(vertex_id))
                end_points.append(Point.from_mtg(self.mtg, vertex_id))
        return end_points

    def determine_age(self):
        """
        This function determines the ages for each branch on the tree.
        TODO: the age needs to be determined until a leader is found instead of until the root is found.
        """
        sorted_branches = sorted(self.get_branches(), key=lambda branch: branch.depth, reverse=True)
        year_one_branch = filter(self.filter_children, sorted_branches)
        end_branches = []
        for branch in year_one_branch:
            end_branches.append(branch)

        for branch in end_branches:
            root_found = False
            age = 1
            while not root_found:
                if branch.parent is not None and branch.age == -1:
                    branch.age = age
                    if branch.parent is None:
                        root_found = True
                    else:
                        if branch.parent is not None:
                            branch = branch.parent
                            age += 1
                        else:
                            root_found = True
                else:
                    if branch.parent is not None:
                        branch = branch.parent
                    else:
                        root_found = True

    @staticmethod
    def filter_children(branch):
        """
        Filter the children for a branch
        :param branch: a branch
        :return:
        """
        return len(branch.children) == 0

    def get_branches(self):
        """
        gets the branches.
        :return: branches
        """
        all_branches = []
        for branches in self.tree_start:
            for branch in get_next(branches):
                all_branches.append(branch)

        return all_branches

    def get_root(self):
        """
        Get the root branch
        :return: root branch
        """
        return self.root_branch

    def determine_leaders(self, leader_count=0):
        """
        TODO: determine leaders is not yet implemented
        leider def:
            1. Heeft altijd 1 of meerdere kinderen
            2. Zit vast aan de stam(of dichtbij in iedergeval)
            3. Langst doorlopende tak(not sure of dit werkt vraag boer) de totale afstand die de punten afleggen
        """

        branches = sorted(self.get_branches(), key=lambda branch: branch.depth, reverse=True)

        for branch in branches:
            if branch.parent == self.root_branch:
                if(len(branch.points) > leader_threshold) and len(branch.children) > 1:
                    branch.is_leader = True
                    branch.age = 10
                else:
                    self.root_branch.points.extend(branch.points)
                    for child in branch.children:
                        if len(child.points) > leader_threshold and len(branch.children) > 1:
                            child.is_leader = True
                            branch.age = 10
                        child.parent = self.root_branch
                        self.tree_start.append(child)
                    self.tree_start.remove(branch)