import pickle

# from openalea.mtg.plantframe.plot_statistic import *
# import PyQt5
# from PyQt4.QtCore import *
import numpy
import openalea.plantscan3d.mtgmanip as mm
import openalea.plantscan3d.serial as serial
from openalea.mtg import *
# from PyQt4.QtGui import *
from openalea.mtg.aml import *
from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
from openalea.plantscan3d.xumethod import xu_method


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


# AlgHeight() aantal v between v1 en v2
def KnipTak(mtg, v1, v2, knipType):
    pathv1_v2 = mtg.path(v1, v2)
    print("mtg.path = ", pathv1_v2)
    if knipType == 1:
        VanafV = v1
        NaarV = v2
        knipAfstand = 5
    elif knipType == 2:
        VanafV = v2
        NaarV = v1
        knipAfstand = 5
    else:
        VanafV = v1
        NaarV = v2
        knipAfstand = 5
    if afstandTussenV1_V2(VanafV, NaarV) > knipAfstand:
        knipLocatie = knipTussenVertex()
    return 0
    # Validate
    return knipLocatie


def afstandTussenV1_V2(mtg, v1, v2):
    path_v1_v2 = mtg.Path(v1, v2)
    for i in path_v1_v2:
        print("Loop door vertex".format(i))
    # Locatie v1
    # Locatie v2
    # bereken afstand
    return (v1)


def getVertexPosition(mtg, v1):
    items = mtg.__getitem__(v1)
    print("keys: ", items.keys())
    print("position = ", items.get('position'))
    stringVector3 = str(items.get('position'))
    print("string vector 3 = ", stringVector3)
    # positions = [int(s) for s in stringVector3.split() if s.isdigit()]
    positions = re.findall(r"[-+]?\d*\.\d+|\d+", stringVector3)
    positions.pop(0)
    print("string positions zijn ", positions)
    # items.get()
    v_coordinate = numpy.asfarray(positions)
    print("numpy array = ", v_coordinate)
    return v_coordinate


def afstandTussenAanliggendeV1_V2(mtg, v1, v2):
    v1_coord = getVertexPosition(mtg, v1)
    v2_coord = getVertexPosition(mtg, v2)
    afstand = numpy.linalg.norm(v1_coord - v2_coord)
    print("afstand v1 tot v2 ", afstand)
    # return afstands


def knipTussenVertex(mtg, v1, v2, afstandv1_v2):
    # Krijg locatie v1, krijg locatie v2.
    # afstandTussen (v1, v2)
    # Beweeg afstand van v1 naar v2 en krijg locatie
    return (x, y, z)


def main():
    print("program started")
    stack_split = []
    scene = Scene('C:/Minor1/klein_Boom.ply')
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
    print("path = ", g1.Path(vids_U[2], vids_U[5]))
    afstandTussenAanliggendeV1_V2(mtg, vids_U[2], vids_U[5])
    # afstandTussenV1_V2(mtg, vids_U[2], vids_U[5])
    # Scale(1)
    # d = DressingData()
    print("Max scale = ", g1.max_scale())
    # pf = PlantFrame(g1, 1, Scale=2, DressingData=d, TopDiameter=1)  # doctest: +SKIP
    print("START PLOTTING")
    # g = MTG('agraf.mtg')
    # dressing_data = dressing_data_from_file('agraf.drf')
    # topdia = lambda x:  g.property('TopDia').get(x)
    # pf = PlantFrame(g1,    DressingData=dressing_data)
    # axes = pf._compute_axes()
    # diameters = pf.algo_diameter()
    # scene = build_scene(pf.g1, pf.origin, axes, pf.points, diameters, 10000)
    # g1.plot_property("position")
    # Viewer.display(scene)
    # _plot(g1)
    # pf.plot_property('length')
    # pf.plot(gc=True, display=False)
    print("dit zijn mijn items ", items)
    '''
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
    '''


if __name__ == '__main__':
    print("Ben ik begonnen")
    main()
