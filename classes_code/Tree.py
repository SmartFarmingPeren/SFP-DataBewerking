from utilities.configuration_file import *
import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg import MTG
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method
from openalea.mtg.aml import *
import openalea.plantscan3d.serial as serial
from graphs.visual import *
import numpy
import re


class Tree:
    """
    TODO The tree class is poop
    """
    def __init__(self, input_point_cloud_name):
        # During the skeletonize a mtg file is created from a point cloud, both are saved for later use
        self.point_cloud, self.mtg = self.create_scene_and_skeletonize(input_point_cloud_name)

        self.root_branch = determine_root(mtg)


        # A tree consists of branches and leaders
        self.branches = []
        self.leaders = []

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
        zdist = point_cloud[maxi].z - point_cloud[mini].z
        binlength = zdist / XU_SKELETON_BIN_RATIO

        vtx = list(mtg.vertices(mtg.max_scale()))
        startfrom = vtx[0]
        mtg = xu_method(mtg, startfrom, point_cloud, binlength, XU_SKELETON_K)
        return mtg

    @staticmethod
    def determine_vertexes(mtg):
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
        lowest_vertex, highest_vertex = Tree.determine_vertexes(mtg)
        for point in range(lowest_vertex, highest_vertex):

            # Check if mtg has radius otherwise just say radius is 1
            try:
                radius = mtg.property('radius')[point]
            except Exception as e:
                print(e)
                radius = 1

            if len(mtg.Sons(point)) == 1:
                root_branch.append(Point(point, Vector3(mtg.property('position')[point]), radius))
            else:
                root_branch.append(Point(point, Vector3(mtg.property('position')[point]), radius))
                break