import openalea.plantscan3d.mtgmanip as mm
import openalea.plantscan3d.serial as serial
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method
from classes_code.Point import Point
from graphs.visual import *
from utilities.configuration_file import *


class Tree:
    """
    The tree class is used to load a point cloud, then skeletonize the point cloud.
    After that the created MTG file will be split into: root, leaders, branches and points.
    The tree class is a collection for these items.
    """

    def __init__(self, input_point_cloud_name):
        # During the skeletonize a mtg file is created from a point cloud, both are saved for later use
        self.point_cloud, self.mtg = self.create_scene_and_skeletonize(input_point_cloud_name)

        # Determine the root branch
        self.root_branch = self.determine_root(self.mtg)
        # A tree consists of branches and leaders
        self.branches = []  # TODO implement
        self.leaders = []  # TODO implement

        self.end_points = self.get_branch_ends()
        for end_point in self.end_points:
            print(end_point)

        # Export the generated skeleton as a mtg file and save it under the input file name
        serial.writeMTGfile(OUTPUT_MTG_DIR + input_point_cloud_name.split()[0] + '.mtg',
                            serial.convertToStdMTG(self.mtg))

        # Export a graph as a .html file
        plot(self.mtg, OUTPUT_GRAPHS_DIR + input_point_cloud_name.split()[0] + '.html')

    @staticmethod
    def create_scene_and_skeletonize(input_point_cloud_name):
        """
        This function creates a scene > points and then converts it to a mtg file.
        :param input_point_cloud_name: name of the point cloud stored in the input point clouds dir
        :return: point_cloud, mtg
        """
        scene = Scene(INPUT_POINT_CLOUDS_DIR + input_point_cloud_name)
        point_cloud = scene[0].geometry.pointList
        point_cloud.swapCoordinates(1, 2)
        mtg = Tree.skeleton(point_cloud)
        return point_cloud, mtg

    @staticmethod
    def skeleton(point_cloud):
        """
        The skeleton function creates a skeleton(using xu_method) from a pear tree point_cloud.
        This skeleton is stored in a .mtg file.
        This mtg file could be exported or worked with internally.

        :param point_cloud: scene[0].geometry.pointList
        :return: mtg file
        """
        mini, maxi = point_cloud.getZMinAndMaxIndex()
        root = Vector3(point_cloud[mini])

        mtg = mm.initialize_mtg(root)
        z_dist = point_cloud[maxi].z - point_cloud[mini].z
        bin_length = z_dist / XU_SKELETON_BIN_RATIO

        vtx = list(mtg.vertices(mtg.max_scale()))
        start_from = vtx[0]
        mtg = xu_method(mtg, start_from, point_cloud, bin_length, XU_SKELETON_K)
        return mtg

    @staticmethod
    def determine_vertexes(mtg):
        """
        This function determines the lowest and highest vertex point.
        :param mtg:
        :return:
        """
        highest_vertex = 0
        lowest_vertex = 99999999999
        for point in mtg.property('position'):
            if point > highest_vertex:
                highest_vertex = point
            if point < lowest_vertex:
                lowest_vertex = point
        return lowest_vertex, highest_vertex

    @staticmethod
    def determine_root(mtg):
        """
        This function determines the root of a tree
        TODO This function only works if there are no other branches on the root than the 4 leaders.
        If there is a small branch on the root this code wont work, in future we need to improve this method.
        :param mtg:
        """
        lowest_vertex, highest_vertex = Tree.determine_vertexes(mtg)
        root_branch = []
        for point in range(lowest_vertex, highest_vertex):
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
                root_branch.append(Point(point, Vector3(mtg.property('position')[point]), parent, radius))
            else:
                root_branch.append(Point(point, Vector3(mtg.property('position')[point]), parent, radius))
                break
        return root_branch

    def get_branch_ends(self):
        """
        This function gets the end vertexes of the tree.
        These endpoints will be used to determine branch age later.
        :return: end_points = [Point]
        """
        lowest_vertex, highest_vertex = Tree.determine_vertexes(self.mtg)
        end_points = []
        for vertex_id in range(lowest_vertex, highest_vertex):
            if len(self.mtg.Sons(vertex_id)) == 0:
                # debug_message("End point found at {0}".format(vertex_id))
                end_points.append(self.get_point_by_id(vertex_id))
        return end_points

    # def get_point_by_id(self, vid):
    #     # TODO fix this shit
    #     point_object = self.mtg.__getitem__(vid)
    #     return Point(point_object.get('_vid'), point_object.get('position'), point_object.get('radius'))

    def get_point_by_id(self, vertex_id):
        """
        TODO ASK STEVEN IF THIS APPROACH IS OKAY WITH HIM - [LUCA]
        :param vertex_id: A vertex_id from the mtg.
        :return: a Point object created from the vertex data.
        """
        point_object = self.mtg.__getitem__(vertex_id)

        # Check if mtg has radius otherwise just say radius is 1
        if point_object.get('radius') is None:
            radius = 0
        else:
            radius = point_object.get('radius')

        return Point(point_object.get('vid'), point_object.get('position'), point_object.get('parent'), radius)
