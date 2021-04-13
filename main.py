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
    scene = Scene('D:/TeringTyfus/gen_2_23_03_expanded.ply')
    points = scene[0].geometry.pointList

    mtg = skeleton(points)
    serial.writefile("hallo.bmtg", mtg)

if __name__ == '__main__':
    main()


'''
Useful links
[1.] https://plantscan3d.readthedocs.io/en/latest/userguide/clean_process.html#point-cloud-segmentation

[2.] https://github.com/fredboudon/plantscan3d/blob/master/example/pipeline.py

[3.] https://plantscan3d.readthedocs.io/en/latest/userguide/reconstruction.html#save-and-export

[4. HEEL NICE] https://plantscan3d.readthedocs.io/en/latest/userguide/clean_process.html

[5.] https://github.com/openalea

[6. Gebruik voor readme] https://docs.anaconda.com/anaconda/user-guide/tasks/pycharm/

[7.] https://github.com/openalea/mtg/blob/master/src/openalea/mtg/mtg.py

[8.] https://stackoverflow.com/questions/31384639/what-is-pythons-site-packages-directory

[9.] https://anaconda.org/fredboudon

[10.] https://github.com/openalea/openalea

[11.] https://github.com/openalea/plantgl

[12.] https://github.com/fredboudon/plantscan3d/tree/master/example

[13. MTG OPENEN EN SHIT] http://virtualplants.github.io/latest/user/index.html#getting-start

[14. ] https://github.com/fredboudon/plantscan3d
'''