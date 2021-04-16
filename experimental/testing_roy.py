import pickle

import openalea
from openalea.mtg.algo import ancestors, sons
from openalea.mtg.aml import Sons

from openalea.mtg import PlantFrame, MTG

from openalea.mtg.io import write_mtg, read_mtg_file
from openalea.plantgl import *
# from openalea.mtg import *
from openalea.mtg.aml import *
from openalea.mtg import *
from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
from openalea.plantscan3d import *
import openalea.plantscan3d.mtgmanip as mm
from openalea.plantscan3d.xumethod import xu_method
import openalea.plantscan3d.serial as serial


def skeleton(mtg, points, binratio=50, k=30):
    mini, maxi = points.getZMinAndMaxIndex()
    root = Vector3(points[mini])
    mtg = mm.initialize_mtg(root)
    zdist = points[maxi].z - points[mini].z
    binlength = zdist / binratio
    vtx = list(mtg.vertices(mtg.max_scale()))
    startfrom = vtx[0]
    xu_method(mtg, startfrom, points, binlength)
    return mtg


def writefile(fn, obj):
    f = open(fn, 'wb')
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    test = PlantFrame()

def setup():
    root = Vector3(0, 0, 0)
    mtg = mm.initialize_mtg(root)
    return mtg

def main():
    print("program started")
    stack_split = []
    scene = Scene('C:/Minor1/1_branch.ply')
    points = scene[0].geometry.pointList
    points.swapCoordinates(1, 2)
    mtg = setup()
    mtg = skeleton(mtg, points)
    # voor opslaan mtg bestand
    vids_U = mtg.vertices()
    v = vids_U[2]
    items = mtg.__getitem__(v)
    print("dit zijn mijn items ", items)
    std = serial.convertToStdMTG(mtg)
    serial.writeMTGfile('test5.mtg', std)
    g1 = MTG("test5.mtg")
    Activate(g1)
    Scale(1)
    print("IkBenHier1")
    d = DressingData()
    print("IkBenHier2")
    print("Max scale = ", g1.max_scale())
    #pf = PlantFrame(1, Scale=2, DressingData=d)  # doctest: +SKIP
    print("dit zijn mijn items ", items)
    for _ in range(3):
        v_succesor = mtg.Sons(v, RestrictedTo='NoRestriction', EdgeType='*')
        print("items van succesor zijn ", mtg.__getitem__(v))
        print("v succesors zijn: ", v_succesor)
        print("inhoud van stack splitsingen is", stack_split)
        if v_succesor == []:
            print("Einde tak")
            v = stack_split.pop()
        v_succesor = mtg.Sons(v, RestrictedTo='NoRestriction', EdgeType='+')
        if v_succesor != []:
            print("node {0} Heeft aftakking {1}".format(v, v_succesor))
            stack_split.append(v)
            v = v_succesor[0]
        v_succesor = mtg.Sons(v, RestrictedTo='NoRestriction', EdgeType='<')
        if v_succesor != []:
            print("node {0} Heeft succesor {1}".format(v, v_succesor))
            v = v_succesor[0]
        print("Dit is de succesor ", v_succesor)
if __name__ == '__main__':
    print("Ben ik begonnen")
    main()