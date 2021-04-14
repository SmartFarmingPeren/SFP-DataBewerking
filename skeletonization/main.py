import pickle

from openalea.plantgl.all import *
from openalea.mtg import *
from openalea.plantscan3d import *

import openalea.plantscan3d.mtgmanip as mm
from openalea.plantscan3d.xumethod import xu_method
import openalea.plantscan3d.serial as serial
from openalea.mtg.io import *

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



def main():
    print("started code")
    scene = Scene('D:/PearTreeDataProcessing/Skeletonization/Simpele_boom.ply')
    points = scene[0].geometry.pointList

    mtg = skeleton(points)


    # serial.writefile("teringAidsTest.bmtg", mtg)
    #
    # mtg_test = MTG()
    # mtg_test = MTG("D:/PearTreeDataProcessing/Skeletonization/test.mtg")
    # print(mtg_test)


if __name__ == '__main__':
    main()

