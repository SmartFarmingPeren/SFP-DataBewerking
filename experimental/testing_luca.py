import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg.aml import MTG
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method

from utilities.debug_log_functions import *
import openalea.plantscan3d.serial as serial
from graphs.visual import *


class Branch:
    def __init__(self, vtx_start, vtx_end, age):
        self.start = vtx_start
        self.end = vtx_end
        self.a = age

ROOTBRANCHAGE = 4

def skeleton(points, binratio=50, k=20):
    """
    The skeleton function creates a skeleton(using xu_method) from a pear tree point_cloud.
    This skeleton is stored in a .mtg file.
    This mtg file could be exported or worked with internally.

    :param points: scene[0].geometry.pointList
    :param binratio: binratio=50
    :param k: k=20
    :return: mtg file
    """
    mini, maxi = points.getZMinAndMaxIndex()
    root = Vector3(points[mini])

    mtg = mm.initialize_mtg(root)
    zdist = points[maxi].z - points[mini].z
    binlength = zdist / binratio

    vtx = list(mtg.vertices(mtg.max_scale()))
    startfrom = vtx[0]
    mtg = xu_method(mtg, startfrom, points, binlength, k)

    return mtg


def create_scene_and_skeletonize(input_point_cloud_name):
    """
    This function creates a scene > points and then converts it to a mtg file.
    :param input_point_cloud_name: name of the point cloud stored in the input point clouds dir
    :return: mtg
    """
    scene = Scene(INPUT_POINT_CLOUDS_DIR + input_point_cloud_name)
    points = scene[0].geometry.pointList
    points.swapCoordinates(1, 2)
    mtg = skeleton(points, binratio=10)
    return mtg


def trunk(mtg):
    mytrunk = 0
    vid_r = mtg.vertices()
    startpoint = vid_r[2]
    d = mtg.get_vertex_property(startpoint)
    for x in mtg:
        if len(mtg.Sons(x)) > 1:
            mytrunk = Branch(startpoint, mtg.Father(x+1), ROOTBRANCHAGE)
            break
    return mytrunk

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
                        mylist.append(Branch(startpoint, mtg.Father(i), count))
                        index = padje.index(mtg.index(i))
                        startpoint = mtg.Father(i)
                        count = count + 1
    return mylist

def main():
    """
    The Skeletonization code creates a skeleton from a input point cloud.
    """
    input_point_cloud_name = "simpele_simpele_boom.ply"
    output_mtg_name = "simpele_simpele_boom.mtg"

    info_message("Creating skeleton")
    mtg = create_scene_and_skeletonize(input_point_cloud_name)

    info_message("Converting and saving MTG to .mtg file")
    std = serial.convertToStdMTG(mtg)
    serial.writeMTGfile(OUTPUT_MTG_DIR + output_mtg_name, std)

    info_message("Plotting mtg as a graph")
    debug_message(std)
    plot(std)

    mylist = branches(mtg)
    mylist = list(dict.fromkeys(mylist))

    for x in mylist:
        debug_message("start {0}".format(x.start))
        debug_message("end {0}".format(x.end))
        debug_message("age {0}\n".format(x.a))

    mytrunk = trunk(mtg)
    debug_message("start {0}".format(mytrunk.start))
    debug_message("end {0}".format(mytrunk.end))
    debug_message("age {0}".format(mytrunk.a))

if __name__ == '__main__':
    main()