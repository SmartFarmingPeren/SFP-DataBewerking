import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg.aml import MTG
from openalea.mtg.io import write_mtg
from openalea.plantgl.all import *
from openalea.plantscan3d.serial import max_order
from openalea.plantscan3d.xumethod import xu_method

from utilities.configuration_file import *


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
    mtg = skeleton(points)
    return mtg


def writeMTGfile(fn, g, properties=[('XX','REAL'), ('YY','REAL'), ('ZZ','REAL'), ('radius','REAL')]):

    if properties == []:
        properties = [(p, 'REAL') for p in g.property_names() if p not in ['edge_type', 'index', 'label']]
    nb_tab = max_order(g)
    str = write_mtg(g, properties, nb_tab=nb_tab)
    f = open(fn, 'w+')
    f.write(str)
    f.close()

def main():
    """
    The Skeletonization code creates a skeleton from a input point cloud.
    """
    input_point_cloud_name = "Simpele_boom.ply"

    mtg = create_scene_and_skeletonize(input_point_cloud_name)
    # writeMTGfile("hoi.mtg", mtg)

    mtg_lines = write_mtg(mtg, properties=[('XX','REAL'), ('YY','REAL'), ('ZZ','REAL'), ('radius','REAL')])

    # Write the result into a file example.mtg
    filename = 'example.mtg'
    f = open(filename, 'w+')
    f.write(mtg_lines)
    f.close()

if __name__ == '__main__':
    main()
