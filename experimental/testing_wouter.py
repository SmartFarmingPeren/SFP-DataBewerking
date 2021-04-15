import pickle

import openalea
from openalea.mtg.algo import ancestors, sons
from openalea.mtg.aml import Sons

from visual import *

from openalea.mtg import PlantFrame, MTG

from openalea.mtg.io import write_mtg, read_mtg_file
from openalea.plantgl import *
#from openalea.mtg import *
from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
from openalea.plantscan3d import *
import openalea.plantscan3d.mtgmanip as mm
from openalea.plantscan3d.xumethod import xu_method
import openalea.plantscan3d.serial as serial



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

def filterpoints(mtg):
    vertexen = mtg.vertices()
    for x in mtg:
        comp = len(mtg.Sons(x))
        #print(comp)
        if comp == 0:
            mals = mtg.__getitem__(x)
            vid_x = mtg.index(x)
            vid_y = mtg.Root(vid_x)
            padje = mtg.Path(vid_x, vid_y)
            #flip padje
            #For i in len(padje)
                 #if parent van padje(i) heeft meer dan 1 zoon
                       If parent label = n dan 2ejaar else 1 dan 2, else if 2 dan 3 
                        Id leider????
       
                       #Parent van padje(i) = 2e jaar
      
            If label from parent padje
            print(padje)

def setup():
    root = Vector3(0, 0, 0)
    mtg = mm.initialize_mtg(root)
    return mtg

def main():
    class Branch:
        def __init__(self, start_point, end_point, radius):
            self.start = start_point
            self.end = end_point
            self.rad = radius

    #scene = Scene('C:/Users/woute/Documents/jammer/gen_2_23_03_expanded.ply')
    #scene = Scene('C:/Users/woute/Documents/jammer/2021_03_19__10_55_07.ply')

    #correcte manier voor skeleton
    scene = Scene('C:/Users/woute/Documents/jammer/simpel.ply')
    points = scene[0].geometry.pointList
    points.swapCoordinates(1, 2)
    mtg = setup()
    mtg = skeleton(mtg, points)

    #voor opslaan mtg bestand
    std = serial.convertToStdMTG(mtg)
    serial.writeMTGfile('test4.mtg', std)
    plot(std)


    #voor lezen mtg bestand
    #test = 'C:/Users/woute/Documents/jammer/mijnsimpel.mtg'
    #mtg = read_mtg_file(test)
    #plot(mtg)

    #voor een enkel item
    all_vids = mtg.vertices             #all verteces
    items = mtg.__getitem__(1)
    print("dit is mijn data", items)

    #alle boom paden
    filterpoints(mtg)

if __name__ == '__main__':
    main()



