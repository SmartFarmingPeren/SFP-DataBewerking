import pickle
from openalea.mtg import PlantFrame
from openalea.mtg.io import write_mtg
from openalea.plantgl import *
#from openalea.mtg import *
from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
from openalea.plantscan3d import *
import openalea.plantscan3d.mtgmanip as mm
from openalea.plantscan3d.xumethod import xu_method
import openalea.plantscan3d.serial as serial

from Skeletonization.visual import plot


def skeleton(points, binratio = 50, k = 20):
    mini,maxi = points.getZMinAndMaxIndex()
    root = Vector3(points[mini])
    mtg = mm.initialize_mtg(root)
    zdist = points[maxi].z-points[mini].z
    binlength = zdist / binratio
    vtx = list(mtg.vertices(mtg.max_scale()))
    startfrom = vtx[0]

    mtg = xu_method(mtg, startfrom, points, binlength, k)
    return mtg

def root_points(mtg):
    classes = list(set(mtg.class_name(vid) for vid in mtg.vertices() if mtg.class_name(vid)))
    print(classes)
    def vertices(mtg, class_name='P'):
        return [vid for vid in mtg.vertices() if mtg.class_name(vid) == class_name]

    vids_U = vertices(mtg, 'U')
    print('Nb U', len(vids_U))
    return

def root_points2(g):
    classes = list(set(g.class_name(vid) for vid in g.vertices() if g.class_name(vid)))
    print(classes)
    def vertices(g, class_name='P'):
        return [vid for vid in g.vertices() if g.class_name(vid) == class_name]

    vids_U = vertices(g, 'U')
    vids_N = vertices(g, 'N')
    phi = g.property('phi')
    print('Nb U', len(vids_U))
    plot(g, labels=phi)
    #plot(g, selection=vids_N)
    return

def writefile(fn, obj):
    f = open(fn,'wb')
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    test = PlantFrame()

def main():
    print("started code")
    scene = Scene('D:/PearTreeDataProcessing/Skeletonization/gen_2_23_03_expanded.ply')
    points = scene[0].geometry.pointList
    mtg = skeleton(points)

    #root_points(mtg)
    # root_points2(mtg)
    root_id = 271
    children = mtg.Descendants(root_id)
    plot(mtg, selection=children)
    # plot(mtg)
    #writefile("hallo.bmtg", mtg)


if __name__ == '__main__':
    main()
