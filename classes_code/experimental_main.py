import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg import MTG
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method

from utilities.debug_log_functions import *
import openalea.plantscan3d.serial as serial
from graphs.visual import *


class Tree:
    """
    A tree class
    """

    def __init__(self, input_point_cloud_name):
        self.points = None
        self.mtg = MTG()
        self.xu_skeleton_bin_ratio = 10
        self.xu_skeleton_k = 20

        self.input_point_cloud_name = input_point_cloud_name
        self.create_scene_and_skeletonize()

        self.lowest_vertex = None
        self.highest_vertex = None
        self.determine_vertexes()

        self.root_branch = []
        self.determine_root()
        self.leaders = []  # array with leaders

    def skeleton(self):
        """
        The skeleton function creates a skeleton(using xu_method) from a pear tree point_cloud.
        This skeleton is stored in a .mtg file.
        This mtg file could be exported or worked with internally.

        :param points: scene[0].geometry.pointList
        :param binratio: binratio=50
        :param k: k=20
        :return: mtg file
        """
        mini, maxi = self.points.getZMinAndMaxIndex()
        root = Vector3(self.points[mini])

        mtg = mm.initialize_mtg(root)
        zdist = self.points[maxi].z - self.points[mini].z
        binlength = zdist / self.xu_skeleton_bin_ratio

        vtx = list(mtg.vertices(mtg.max_scale()))
        startfrom = vtx[0]
        self.mtg = xu_method(mtg, startfrom, self.points, binlength, self.xu_skeleton_k)

    def create_scene_and_skeletonize(self):
        """
        This function creates a scene > points and then converts it to a mtg file.
        :param input_point_cloud_name: name of the point cloud stored in the input point clouds dir
        :return: mtg
        """
        scene = Scene(INPUT_POINT_CLOUDS_DIR + self.input_point_cloud_name)
        self.points = scene[0].geometry.pointList
        self.points.swapCoordinates(1, 2)
        self.skeleton()

    def determine_vertexes(self):
        self.highest_vertex = 0
        self.lowest_vertex = 99999999999
        for point in self.mtg.property('position'):
            if point > self.highest_vertex:
                self.highest_vertex = point
            if point < self.lowest_vertex:
                self.lowest_vertex = point


    def determine_root(self):
        for point in range(self.lowest_vertex, self.highest_vertex):

            # Check if mtg has radius otherwise just say radius is 1
            try:
                radius = self.mtg.property('radius')[point]
            except Exception as e:
                error_message(e)
                radius = 1

            if len(self.mtg.Sons(point)) == 1:
                self.root_branch.append(Point(point, Vector3(self.mtg.property('position')[point]), radius))
            else:
                self.root_branch.append(Point(point, Vector3(self.mtg.property('position')[point]), radius))
                break

    def determine_leaders(self):
        for x in range(1, len(self.mtg.Sons(self.root_branch[-1]))):
            print()

class Leader:
    def __init__(self):
        self.start_point = None
        self.end_point = None


class Branch:
    def __init__(self):
        pass


class Point:
    def __init__(self, vid, vector3, radius):
        self.vid = vid
        self.vector = Vector3(vector3)
        self.x = self.vector.x
        self.y = self.vector.y
        self.z = self.vector.z
        self.radius = radius


def main():
    """
    A object oriented approach to a pruning problem
    
    """
    input_point_cloud_name = "Simpele_boom.ply"
    output_mtg_name = "Simpele_boom.mtg"

    info_message("Creating tree object")
    object_tree = Tree(input_point_cloud_name)



    # mtg = object_tree.mtg
    # info_message("Converting and saving MTG to .mtg file")
    # std = serial.convertToStdMTG(mtg)
    # serial.writeMTGfile(OUTPUT_MTG_DIR + output_mtg_name, std)
    #
    # info_message("Plotting mtg as a graph")
    # debug_message(std)
    # plot(std)


if __name__ == '__main__':
    main()
