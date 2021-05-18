import openalea.plantscan3d.serial as serial
from openalea.plantgl.all import *

from classes_code.Branch import Branch
from classes_code.Point import Point
from classes_code.Skeletonization import create_scene_and_skeletonize
from graphs.visual import *
from utilities.configuration_file import *


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
        # TODO A root branch is fucked at this time. Ask Luca(17-05-2021). Is it still though? (18-05-2021) Brandon
        self.root_branch = root if root is not None else self.determine_root(self.mtg)

        # Determine the branch end points
        self.end_points = self.get_branch_ends()

        branches = self.root_branch.determine_branch(self.mtg, 2)

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
                root_branch.append(Point.from_mtg(mtg.__getitem__(point)))
            else:
                # TODO direction TBD
                root_branch.append(Point.from_mtg(mtg.__getitem__(point)))
                # Check if the branch itself has more branches on it, if not it's just an extra branch on the root
                for cp in mtg.Sons(point):
                    current_point = cp
                    while True:
                        if len(mtg.Sons(current_point)) == 1:
                            current_point = mtg.Sons(current_point)[0]
                        elif len(mtg.Sons(current_point)) == 0:
                            just_a_branch = 1
                            break
                        else:
                            end_of_root = end_of_root + 1
                            break
                    if just_a_branch == 1:
                        break
            if end_of_root >= 2:
                break
            else:
                end_of_root = 0
                just_a_branch = 0

        branch = Branch(branch_id="branch_" + str(lowest_vertex), age=1, points=root_branch)
        return branch

    @staticmethod
    def determine_vertexes(mtg):
        """
        This function determines the lowest and highest vertex point.
        :param mtg:
        :return:
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
                end_points.append(Point.from_mtg(self.mtg.__getitem__(vertex_id)))
        return end_points
