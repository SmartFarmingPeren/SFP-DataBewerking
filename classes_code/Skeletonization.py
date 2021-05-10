import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg.io import write_mtg
from openalea.plantgl.math import Vector3
from openalea.plantgl.scenegraph import Scene
from openalea.plantscan3d.serial import max_order
from openalea.plantscan3d.xumethod import xu_method

from utilities.configuration_file import INPUT_POINT_CLOUDS_DIR, XU_SKELETON_BIN_RATIO, XU_SKELETON_K


def get_skeleton(point_cloud):
    """
    The skeleton function creates a skeleton(using xu_method) from a pear tree point_cloud.
    This skeleton is stored in a .mtg file.
    This mtg file could be exported or worked with internally.

    :param point_cloud: scene[0].geometry.pointList
    :return: mtg file
    """
    mini, maxi = point_cloud.getZMinAndMaxIndex()
    root = Vector3(point_cloud[mini])

    mtg = mm.initialize_mtg(root)
    z_dist = point_cloud[maxi].z - point_cloud[mini].z
    bin_length = z_dist / XU_SKELETON_BIN_RATIO

    vtx = list(mtg.vertices(mtg.max_scale()))
    start_from = vtx[0]
    mtg = xu_method(mtg, start_from, point_cloud, bin_length, XU_SKELETON_K)

    return mtg


def create_scene_and_skeletonize(input_point_cloud_name):
    """
    This function creates a scene > points and then converts it to a mtg file.
    :param input_point_cloud_name: name of the point cloud stored in the input point clouds dir
    :return: mtg
    """
    scene = Scene(INPUT_POINT_CLOUDS_DIR + input_point_cloud_name)
    point_cloud = scene[0].geometry.pointList
    point_cloud.swapCoordinates(1, 2)
    mtg = skeleton(point_cloud)
    return point_cloud, mtg


def writeMTGfile(fn, g, properties=[('XX','REAL'), ('YY','REAL'), ('ZZ','REAL'), ('radius','REAL')]):

    if properties == []:
        properties = [(p, 'REAL') for p in g.property_names() if p not in ['edge_type', 'index', 'label']]
    nb_tab = max_order(g)
    str = write_mtg(g, properties, nb_tab=nb_tab)
    f = open(fn, 'w+')
    f.write(str)
    f.close()