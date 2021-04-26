import pickle
import openalea
from openalea.mtg.algo import ancestors, sons
from openalea.mtg.aml import Sons, EdgeType
from graphs.visual import *
from openalea.mtg import PlantFrame, MTG, display_mtg
from openalea.mtg.io import write_mtg, read_mtg_file
from openalea.plantgl import *
#from openalea.mtg import *
from openalea.mtg.aml import *
from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
from openalea.plantscan3d import *
import openalea.plantscan3d.mtgmanip as mm
from openalea.plantscan3d.xumethod import xu_method
import openalea.plantscan3d.serial as serial
from copy import deepcopy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Tree:
    def __init__(self, ply):
        self.scene = Scene(ply)
        self.points = self.scene[0].geometry.pointList
        self.points.swapCoordinates(1, 2)
        self.mtg = setup()
        self.mtg = skeleton(self.mtg, self.points)
        self.vids_U = self.mtg.vertices()
        self.v = self.vids_U[2]
        self.items = self.mtg.__getitem__(self.v)
        print("dit zijn mijn items ", self.items)
        self.std = serial.convertToStdMTG(self.mtg)
        serial.writeMTGfile('test5.mtg', self.std)
        self.g1 = MTG("test5.mtg")
        Activate(self.g1)
        self.branch_ends = []
        self.get_all_branch_ends(self.g1)
        print("branch_ends zijn: ",self.branch_ends)
        self.items = self.mtg.__getitem__(self.branch_ends[0])
        #("dit zijn mijn branch end items ", self.items)
        self.oneYears = []
        self.twoYears = []
        self.make_one_years(self.g1, self.branch_ends)
        self.one_year_fork = []
        self.make_two_years(self.g1)
        self.print_one_year()
        self.print_two_year()
        plot(self.g1)
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
                    self.oneYears.append(OneYearBranch(self.v_array, self.mtg))
                    break
                elif mtg.Sons(self.v_array[counter], RestrictedTo='NoRestriction', EdgeType='+') != []:
                    print("Tak heeft hier een splitsing ")
                    self.oneYears.append(OneYearBranch(self.v_array, self.mtg))
                    break
                else:
                    self.v_array.append(v_child)
                counter+=1
            else:
                self.oneYears.append(OneYearBranch(self.v_array, self.mtg))

    def print_one_year(self):
        for i in self.oneYears:
            #print("i = ", i)
            i.printBranch()

    def print_two_year(self):
        for i in self.twoYears:
            #print("i = ", i)
            i.printBranch()

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
                    Tak = TwoYearBranch(self.tak_array, self.mtg, i)
                    self.twoYears.append(TwoYearBranch(self.tak_array, self.mtg, i))
                    break
                elif mtg.Sons(self.tak_array[counter], RestrictedTo='NoRestriction', EdgeType='+') != [] and counter>1:
                    print("Tak heeft hier een splitsing ")
                    Tak = TwoYearBranch(self.tak_array, self.mtg, i)
                    self.twoYears.append(TwoYearBranch(self.tak_array, self.mtg, i))
                    break
                else:
                    self.tak_array.append(v_child)
                counter += 1
            else:
                #if (self.two_year_does_not_exist(self.tak_array)):
                if (1==1):
                    Tak = TwoYearBranch(self.tak_array, self.mtg, i)
                    self.twoYears.append(TwoYearBranch(self.tak_array, self.mtg, i))
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

class OneYearBranch:
    def __init__(self,v_array, mtg):
        self.v_array = v_array
        self.mtg = mtg
        self.age = 1
        #self.parent
        print("making one year branch", self.v_array)

    def printBranch(self):
        print("one year: ", self.v_array)

    def add_parent(self, branch):
        self.parent = branch

    def make_two_years(self,mtg):
        print("make two year ")

    def get_aftakking_vertex(self):
        return self.v_array[-1]

class TwoYearBranch:
    def __init__(self, v_array, mtg, child):
        self.children = []
        self.children.append(child)
        self.v_array = v_array
        self.mtg = mtg
        self.age = 2
        print("making two year branch", self.v_array)

    def printBranch(self):
        print("two year: ", self.v_array)

    def make_two_years(self, mtg):
        print("make two year ")

    def get_aftakking_vertex(self):
        return self.v_array[-1]

    def add_child(self, child):
        self.children.append(child)

def skeleton(mtg, points, binratio = 50, k = 30):
    mini,maxi = points.getZMinAndMaxIndex()
    root = Vector3(points[mini])
    mtg = mm.initialize_mtg(root)
    zdist = points[maxi].z-points[mini].z
    binlength = zdist / binratio
    vtx = list(mtg.vertices(mtg.max_scale()))
    startfrom = vtx[0]
    xu_method(mtg, startfrom, points, binlength)
    return mtg

def writefile(fn, obj):
    f = open(fn,'wb')
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    test = PlantFrame()

def _add_vertex_properties(self, vid, properties):
    """
    Add a set of properties for a vertex identifier.
    For properties that do not belong to the graph,
    create a new property.
    """
    for name in properties:
        if name not in self._properties:
            self.add_property(name)
        self._properties[name][vid] = properties[name]

def filterpoints(mtg):
    for x in mtg:
        comp = len(mtg.Sons(x))
        print(comp)
        if comp == 0:
            mals = mtg.__getitem__(x)
            vid_x = mtg.index(x)
            vid_y = mtg.Root(vid_x)
            padje = mtg.Path(vid_x, vid_y)
            print(x)
            padje.reverse()
            counter = 1
            print(padje)

def setup():
    root = Vector3(0, 0, 0)
    mtg = mm.initialize_mtg(root)
    return mtg

def main():
    #myTree = Tree('C:/Minor1/gen_5_15_04_expanded.ply')
    myTree = Tree('C:/Minor1/Simpele_boom.ply')
    print("end of program")




if __name__ == '__main__':
    main()



