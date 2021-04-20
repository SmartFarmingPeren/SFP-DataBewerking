import pickle
import openalea
from openalea.mtg.algo import ancestors, sons
from openalea.mtg.aml import Sons, EdgeType
from visual import *
from openalea.mtg import PlantFrame, MTG, display_mtg
from openalea.mtg.io import write_mtg, read_mtg_file
from openalea.plantgl import *
#from openalea.mtg import *
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


class Branch:
    def __init__(self, start_point, end_point, radius):
        self.start = start_point
        self.end = end_point
        self.rad = radius

class ForkPoint:
    def __init__(self, vtx_start, vtx_end, age):
        self.start = vtx_start
        self.end = vtx_end
        self.a = age

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


def branches(mtg):
    mylist = []
    for x in mtg:
        comp = len(mtg.Sons(x))
        if comp == 0:
            vid_x = mtg.index(x)
            vid_y = mtg.Root(vid_x)
            padje = mtg.Path(vid_x, vid_y)
            padje.reverse()
            count = 1
            if (len(padje) > 3):
                startpoint = padje[0]
                for i in padje:
                    #(any(x.start == startpoint for x in mylist) == False):                                             #voor elke splitsing
                    #if mtg.Father(i, '+') != None:                                                                      #voor elke aftakking
                    if len(mtg.Sons(i)) > 1:
                        mylist.append(ForkPoint(startpoint, mtg.Father(i), count))
                        index = padje.index(mtg.index(i))
                        startpoint = mtg.Father(i)
                        count = count + 1
    return mylist

def trunk(mtg):
    vid_r = mtg.vertices()
    startpoint = vid_r[2]
    d = mtg.get_vertex_property(startpoint)
    for x in mtg:
        if len(mtg.Sons(x)) > 1:
            mytrunk = ForkPoint(startpoint, mtg.Father(x+1), 4)
            break
    return mytrunk


def leaders(mtg, mytrunk):
    startpoint = mytrunk.end
    leaders = []
    dist_1 = 0
    dist_2 = 0
    dist_3 = 0
    dist_4 = 0
    point_1 = None
    point_2 = None
    point_3 = None
    point_4 = None

    for x in mtg:
        comp = len(mtg.Sons(x))
        d = mtg.get_vertex_property(x)
        #if (comp == 0) and (d['edge_type'] != '+'):
        if (comp == 0) and (d.get('edge_type') != '+'):
            count = 0
            padje = mtg.Path(startpoint, x)
            padje.reverse()
            zoek = '+'
            for i in padje:
                k = mtg.get_vertex_property(i)
                
            for key, value in mtg.keys():
                if key == zoek:
                    del mtg[key]


            #for i in padje:
            #    print(i)
            #
            #    if k['edge_type'] == '+':
                #    if count > dist_1:
                #        dist_1 = count
                #        point_1 = mtg.index(i)
                ##    elif count > dist_2:
                 #       dist_2 = count
                 ##       point_2 = mtg.index(i)
                  #  elif count > dist_3:
                  #      dist_3 = count
                  #      point_3 = mtg.index(i)
                  #      #print("test")
                  #  elif count > dist_4:
                  #      dist_4 = count
                  #      point_4 = mtg.index(i)
                #count = count + 1



    leaders.append(ForkPoint(startpoint, point_1, 0))
    leaders.append(ForkPoint(startpoint, point_2, 0))
    leaders.append(ForkPoint(startpoint, point_3, 0))
    leaders.append(ForkPoint(startpoint, point_4, 0))
    print(point_1)
    print(point_2)
    print(point_3)
    print(point_4)
    return leaders

def setup():
    root = Vector3(0, 0, 0)
    mtg = mm.initialize_mtg(root)
    return mtg


def main():
    #scene = Scene('C:/Users/woute/Documents/jammer/gen_2_23_03_expanded.ply')
    #scene = Scene('C:/Users/woute/Documents/jammer/2021_03_19__10_55_07.ply')
    scene = Scene('C:/Users/woute/Documents/jammer/gen_1.ply')
    #scene = Scene('C:/Users/woute/Documents/jammer/simpel.ply')

    #correcte manier voor skeleton
    points = scene[0].geometry.pointList
    points.swapCoordinates(1, 2)
    mtg = setup()
    mtg = skeleton(mtg, points)
    mylist = branches(mtg)
    mylist = list(dict.fromkeys(mylist))

    for x in mylist:
        print(x.start)
        print(x.end)
        print(x.a, "\n")

    mytrunk = trunk(mtg)
    myleaders = leaders(mtg, mytrunk)
    items = mtg.__getitem__(600)
    #rops = mtg.property()





if __name__ == '__main__':
    main()



