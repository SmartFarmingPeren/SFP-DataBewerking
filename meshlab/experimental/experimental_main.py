import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg import MTG
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method
from openalea.mtg.aml import *
import openalea.plantscan3d.serial as serial
from graphs.visual import *
import numpy
import re


from utilities.configuration_file import *


class Tree:
    """
    A tree class
    """

    def __init__(self, input_point_cloud_name):
        self.points = None
        #self.mtg = MTG()
        self.xu_skeleton_bin_ratio = 10
        self.xu_skeleton_k = 20

        self.input_point_cloud_name = input_point_cloud_name
        self.create_scene_and_skeletonize()



        # HERE
        self.lowest_vertex = None
        self.highest_vertex = None
        self.determine_vertexes()

        self.root_branch = []
        self.determine_root()
        self.leaders = []  # array with leaders

        self.std = serial.convertToStdMTG(self.mtg)
        serial.writeMTGfile('test5.mtg', self.std)
        self.g1 = MTG("test5.mtg")
        Activate(self.g1)
        self.vids_U = self.mtg.vertices()
        self.branch_ends = []   #array with ends of branches
        self.get_all_branch_ends(self.g1)
        print("branch_ends zijn: ", self.branch_ends)
        self.one_year_fork = []
        self.oneYears = []
        self.twoYears = []
        self.make_one_years(self.g1, self.branch_ends)
        self.make_two_years(self.g1)
        self.print_one_year()
        self.print_two_year()
        plot(self.mtg)

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
                print(e)
                radius = 1

            if len(self.mtg.Sons(point)) == 1:
                self.root_branch.append(Point(point, Vector3(self.mtg.property('position')[point]), radius))
            else:
                self.root_branch.append(Point(point, Vector3(self.mtg.property('position')[point]), radius))
                break

    def determine_leaders(self):
        for x in range(1, len(self.mtg.Sons(self.root_branch[-1]))):
            print()

    def get_all_branch_ends(self, mtg):
        #Geef van de mtg alle takken zonder sons terug
        for i in self.vids_U:
            if mtg.Sons(i, RestrictedTo='NoRestriction', EdgeType='*') == [] and i != 1 and i != 0:
                print ("takeinde = ", i)
                #print ("items van child zijn ", mtg.__getitem__(i))
                item = mtg.__getitem__(i)
                print("line = ", item.get('_line'))
                self.branch_ends.append(item.get('vid'))

    def make_one_years(self, mtg, branch_ends):
        for i in branch_ends:
            print("i = ", i)
            self.v_array = [i]
            counter = 0
            while(mtg.Father(self.v_array[counter], RestrictedTo='NoRestriction', EdgeType='+') == None):
                print("self v_array = ",self.v_array)
                v_child = mtg.Father(self.v_array[counter], RestrictedTo='SameAxis', EdgeType='<')
                #print("items van child zijn ", mtg.__getitem__(self.v_array[counter]))
                #print("V_child = ", v_child)
                #print("sons = ",mtg.Sons(self.v_array[counter], RestrictedTo='NoRestriction', EdgeType='+'))
                if (v_child == []):
                    print("ERROR")
                elif (v_child == None):
                    print("Einde tak ")
                    self.oneYears.append(Branch(self.v_array, self.mtg, 1))
                    break
                elif mtg.Sons(self.v_array[counter], RestrictedTo='NoRestriction', EdgeType='+') != []:
                    print("Tak heeft hier een splitsing ")
                    self.oneYears.append(Branch(self.v_array, self.mtg, 1))
                    break
                else:
                    self.v_array.append(v_child)
                counter+=1
            else:
                self.oneYears.append(Branch(self.v_array, self.mtg, 1))

    def make_two_years(self,mtg):
        for i in self.oneYears:
            aftakking = i.get_aftakking_vertex()
            self.one_year_fork.append(aftakking)
            print("Aftakking = ", mtg.Father(aftakking))
            self.tak_array = [mtg.Father(aftakking, RestrictedTo='NoRestriction', EdgeType='+')]
            counter = 0
            while (mtg.Father(self.tak_array[counter], RestrictedTo='NoRestriction', EdgeType='+') == None):
                print("self tak_array = ", self.tak_array)
                v_child = mtg.Father(self.tak_array[counter], RestrictedTo='SameAxis', EdgeType='<')
                #print("items van child zijn ", mtg.__getitem__(self.tak_array[counter]))
                #print("V_child = ", v_child)
                # print("sons = ",mtg.Sons(self.tak_array[counter], RestrictedTo='NoRestriction', EdgeType='+'))
                if (v_child == []):
                    print("ERROR")
                elif (v_child == None):
                    print("Einde tak ")
                    Tak = Branch(self.tak_array, self.mtg, 2, i)
                    self.twoYears.append(Branch(self.tak_array, self.mtg,2, i))
                    break
                elif mtg.Sons(self.tak_array[counter], RestrictedTo='NoRestriction', EdgeType='+') != [] and counter>1:
                    print("Tak heeft hier een splitsing ")
                    Tak = Branch(self.tak_array, self.mtg, 2, i)
                    self.twoYears.append(Branch(self.tak_array, self.mtg,2 , i))
                    break
                else:
                    self.tak_array.append(v_child)
                counter += 1
            else:
                #this part is suppose to check if a vertex is already in a branch. To prevent duplicates
                #This does not work yet
                #if (self.two_year_does_not_exist(self.tak_array)):
                if (1==1):
                    Tak = Branch(self.tak_array, self.mtg,2, i)
                    self.twoYears.append(Branch(self.tak_array, self.mtg,2, i))
                else:
                    i.add_parent(Tak)

    #def add_parent_to_branch(self):
    def two_year_does_not_exist(self, tak_array):
        for i in self.twoYears:
            if any(elem in i.v_array for elem in tak_array):
                print("Exists")
                return False
            else:
                print("Does not exist")
                return True

    def print_one_year(self):
        for i in self.oneYears:
            #print("i = ", i)
            i.printBranch()

    def print_two_year(self):
        for i in self.twoYears:
            #print("i = ", i)
            i.printBranch()

class Leader:
    def __init__(self):
        self.start_point = None
        self.end_point = None


class Branch:
    def __init__(self, v_array, mtg, age, child=None):
        self.v_array = v_array
        self.mtg = mtg
        self.age = age
        self.children = []
        self.children.append(child)
        # self.parent
        #print("making branch", self.v_array)

    def printBranch(self):
        print(self.age, " year: ", self.v_array)

    def add_parent(self, branch):
        self.parent = branch

    def make_two_years(self, mtg):
        print("make two year ")

    def get_aftakking_vertex(self):
        return self.v_array[-1]

    def afstandTussenV1_V2(mtg, v1, v2):
        path_v1_v2 = mtg.Path(v1, v2)
        for i in path_v1_v2:
            print("Loop door vertex".format(i))
        # Locatie v1
        # Locatie v2
        # bereken afstand
        return (v1)

    def getVertexPosition(mtg, v1):
        #Please don't use this, just use vector3.x, vector3.y, vector3.z
        items = mtg.__getitem__(v1)
        print("keys: ", items.keys())
        print("position = ", items.get('position'))
        stringVector3 = str(items.get('position'))
        print("string vector 3 = ", stringVector3)
        positions = [int(s) for s in stringVector3.split() if s.isdigit()]
        positions = re.findall(r"[-+]?\d*\.\d+|\d+", stringVector3)
        positions.pop(0)
        print("string positions zijn ", positions)
        items.get()
        v_coordinate = numpy.asfarray(positions)
        print("numpy array = ", v_coordinate)
        return v_coordinate

    def afstandTussenAanliggendeV1_V2(self, mtg, v1, v2):
        v1_coord = self.getVertexPosition(mtg, v1)
        v2_coord = self.getVertexPosition(mtg, v2)
        afstand = numpy.linalg.norm(v1_coord - v2_coord)
        print("afstand v1 tot v2 ", afstand)
        # return afstands

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

    print("Creating tree object")
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
