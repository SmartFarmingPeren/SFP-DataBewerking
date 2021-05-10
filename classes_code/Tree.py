import openalea.plantscan3d.mtgmanip as mm
import openalea.plantscan3d.serial as serial
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method
from classes_code.Point import Point
from classes_code.Skeletonization import create_scene_and_skeletonize
from graphs.visual import *
from utilities.configuration_file import *
from utilities.debug_log_functions import debug_message, warning_message, error_message


class Tree:
    """
    The tree class is used to load a point cloud, then skeletonize the point cloud.
    After that the created MTG file will be split into: root, leaders, branches and points.
    The tree class is a collection for these items.
    """

    def __init__(self, input_point_cloud_name, root=None, branches=None):
        # During the skeletonize a mtg file is created from a point cloud, both are saved for later use
        self.point_cloud, self.mtg = create_scene_and_skeletonize(input_point_cloud_name)

        # Determine the root branch
        self.root_branch = root if root is not None else self.determine_root(self.mtg)

        # Determine the branch end points
        self.end_points = self.get_branch_ends()
        """
        Point(Vertex id = 136, [x = 24.314960479736328, y = 30.856678676605224, z = 49.268998527526854], parent = 130,  radius = 0)
        Point(Vertex id = 145, [x = 74.78162956237793, y = 39.00424265861511, z = 75.002188205719], parent = 140,  radius = 0)
        Point(Vertex id = 147, [x = 30.688523716396755, y = 46.71216286553277, z = 74.20707617865668], parent = 142,  radius = 0)
        Point(Vertex id = 149, [x = 79.41132493452592, y = 56.58939743041992, z = 63.9347749189897], parent = 144,  radius = 0)
        Point(Vertex id = 151, [x = 30.80686378479004, y = 21.700605912642047, z = 69.77657526189631], parent = 146,  radius = 0)
        Point(Vertex id = 153, [x = 27.471083450317384, y = 22.999549102783202, z = 73.24696884155273], parent = 150,  radius = 0)
        Point(Vertex id = 161, [x = 88.14643046061198, y = 11.989286104838053, z = 47.03911819458008], parent = 160,  radius = 0)
        """

        # # A tree consists of branches and leaders
        # self.branches = branches if branches is not None else self.determine_branch(self.end_points[6].vertex_id)  # TODO implement
        #
        # # self.branches = self.determine_branches()  # TODO implement
        #
        # self.leaders = []  # TODO implement
        self.determine_branch(2)

        # Export the generated skeleton as a mtg file and save it under the input file name
        serial.writeMTGfile(OUTPUT_MTG_DIR + input_point_cloud_name.split(".")[0] + '.mtg',
                            serial.convertToStdMTG(self.mtg))

        # Export a graph as a .html file
        plot(self.mtg, OUTPUT_GRAPHS_DIR + input_point_cloud_name.split(".")[0] + '.html')

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
        for vertex_id in range(lowest_vertex, highest_vertex + 1):
            if len(self.mtg.Sons(vertex_id)) == 0:
                # debug_message("End point found at {0}".format(vertex_id))
                end_points.append(self.get_point_by_id(vertex_id))
        return end_points

    def get_point_by_id(self, vertex_id):
        """
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

    def determine_branch_OLD(self, branch_end_point):
        """
        TODO the while true will get stuck if the root is reached.
        TODO A point from the root branch needs to be added in order to check if the root is reached.
        :param branch_end_point:
        :return:
        """
        # Init a point array, this represents a branch
        points_in_branch = [self.get_point_by_id(branch_end_point)]

        # Add the end point to the branch
        next_point = branch_end_point

        # While a point only has 1 son, the point belongs to the same branch
        while True:
            father = self.mtg.Father(next_point)

            # If a point has 2 sons the branch splits into 2 branches which means the current branch ends.
            if len(self.mtg.Sons(father)) > 1:
                warning_message("Branch end found!")

                # If a split is found then break
                break
            else:
                points_in_branch.append(self.get_point_by_id(father))
                next_point = father

        # Print the current branch from end to start
        debug_message("Printing the whole branch")
        for point in range(0, len(points_in_branch)):
            print(points_in_branch[point])

        # return the current branch
        # TODO create a branch class which consists of a array of points
        return points_in_branch

    def determine_branches_OLD(self):
        # TODO fix this shit
        # Loop trough the tree from end points to the root
        points_in_branch = []
        for end_point in self.end_points:
            points_in_branch.append(end_point)
            father = self.mtg.Father(end_point.vertex_id)
            debug_message("Father = {0}".format(father))
            if len(self.mtg.Sons(father)) > 1:
                # If a split is found then break
                break
            else:
                points_in_branch.append(self.get_point_by_id(father))

        debug_message("Printing every point from this branch")
        for point in range(0, len(points_in_branch)):
            debug_message(points_in_branch[point])

            # TODO THIS IS REMOVED CODE THAT MIGHT BE USEFUL \(0_0)/

    # def get_point_by_id(self, vid):
    #     # TODO fix this shit
    #     point_object = self.mtg.__getitem__(vid)
    #     return Point(point_object.get('_vid'), point_object.get('position'), point_object.get('radius'))

    def determine_branch(self, start_point):
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
        branch = [self.get_point_by_id(start_point)]
        plus_N = []

        # Check if the point has sons
        if len(self.mtg.Sons(start_point)) > 0:
            next_point = start_point
            while True:
                if self.mtg.Sons(next_point) > 1:
                    for son in self.mtg.Sons(next_point):
                        property = self.mtg.get_vertex_property(son)
                        if property.get("edge_type") == "+":
                            # branch.append(self.get_point_by_id(son))
                            # self.determine_branch(son)
                            plus_N.append(son)
                        else:
                            branch.append(son)
                            next_point = son


        else:
            error_message("Point has no sons motherfucker")
