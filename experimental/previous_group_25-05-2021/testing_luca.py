import openalea.plantscan3d.mtgmanip as mm
import openalea.plantscan3d.serial as serial
from openalea.plantgl.all import *
from openalea.plantscan3d.xumethod import xu_method

from graphs.visual import *
from utilities.debug_log_functions import *

# class Branch:
#     def __init__(self, vtx_start, vtx_end, age):
#         self.start = vtx_start
#         self.end = vtx_end
#         self.a = age
#
# class IdAndVector:
#     def __init__(self, vector3, id):
#         self.vector3 = Vector3(vector3)
#         self.v_id = id

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
            mytrunk = Branch(startpoint, mtg.Father(x + 1), ROOTBRANCHAGE)
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
                    # (any(x.start == startpoint for x in mylist) == False):                                             #voor elke splitsing
                    # if mtg.Father(i, '+') != None:                                                                      #voor elke aftakking
                    if len(mtg.Sons(i)) > 1:
                        mylist.append(Branch(startpoint, mtg.Father(i), count))
                        index = padje.index(mtg.index(i))
                        startpoint = mtg.Father(i)
                        count = count + 1
    return mylist


def pgltree2mtg(mtg, startfrom, parents, positions, radii=None, filter_short_branch=False,
                angle_between_trunk_and_lateral=60, nodelabel='N'):
    from math import degrees, acos

    rootpos = Vector3(mtg.property('position')[startfrom])
    if norm(positions[0] - rootpos) > 1e-3:
        if len(mtg.children(startfrom)) > 0:
            edge_type = '+'
        else:
            edge_type = '<'
        startfrom = mtg.add_child(parent=startfrom, position=positions[0], label=nodelabel, edge_type=edge_type)

    children, root = determine_children(parents)
    clength = subtrees_size(children, root)

    mchildren = list(children[root])
    npositions = mtg.property('position')
    removed = []
    if len(mchildren) >= 2 and filter_short_branch:
        mchildren = [c for c in mchildren if len(children[c]) > 0]
        if len(mchildren) != len(children[root]):
            removed = list(set(children[root]) - set(mchildren))

    mchildren.sort(key=lambda x: -clength[x])
    toprocess = [(c, startfrom, '<' if i == 0 else '+') for i, c in enumerate(mchildren)]
    while len(toprocess) > 0:
        nid, parent, edge_type = toprocess.pop(0)
        pos = positions[nid]
        parameters = dict(parent=parent, label=nodelabel, edge_type=edge_type, position=pos)
        if radii:
            parameters['radius'] = radii[nid]
        mtgnode = mtg.add_child(**parameters)
        mchildren = list(children[nid])
        if len(mchildren) > 0:
            if len(mchildren) >= 2 and filter_short_branch:
                mchildren = [c for c in mchildren if len(children[c]) > 0]
                if len(mchildren) != len(children[nid]):
                    removed = list(set(children[nid]) - set(mchildren))
            if len(mchildren) > 0:
                mchildren.sort(key=lambda x: -clength[x])
                first_edge_type = '<'
                langle = degrees(
                    acos(dot(direction(pos - npositions[parent]), direction(positions[mchildren[0]] - pos))))
                if langle > angle_between_trunk_and_lateral:
                    first_edge_type = '+'
                edges_types = [first_edge_type] + ['+' for i in range(len(mchildren) - 1)]
                toprocess += [(c, mtgnode, e) for c, e in zip(mchildren, edges_types)]
    print('Remove short nodes ', ','.join(map(str, removed)))
    return mtg


def recursive_tree_loop(from_vertex):
    sons = []


class Tree:
    def __init__(self):
        self.branches = []


class Branch:
    def __init__(self):
        self.start = None
        self.end = None
        self.connected_to = None
        self.points = []

    def __function(self):
        pass


class Point:
    def __init__(self, vector, vid):
        self.vector3 = Vector3(vector)
        self.vid = vid


def main():
    """
    The Skeletonization code creates a skeleton from a input point cloud.
    """
    input_point_cloud_name = "Simpele_boom.ply"
    output_mtg_name = "xander_test.mtg"
    info_message("Creating skeleton")
    mtg = create_scene_and_skeletonize(input_point_cloud_name)

    info_message("Converting and saving MTG to .mtg file")
    std = serial.convertToStdMTG(mtg)
    serial.writeMTGfile(OUTPUT_MTG_DIR + output_mtg_name, std)

    info_message("Plotting mtg as a graph")
    debug_message(std)
    plot(std)

    # tree = Tree()
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # print(mtg.property('position')[3])
    # print(mtg.nb_vertices())
    # lowest_position = 9999
    # highest_position = 0
    # for property in mtg.property('position'):
    #     if property < lowest_position:
    #         lowest_position = property
    #     if property > highest_position:
    #         highest_position = property
    # print(highest_position)
    # print(lowest_position)
    # for position in range(lowest_position, highest_position):
    #     if mtg.Sons(position) > 1:
    #         print(mtg.Sons(position)[0])
    #         print(mtg.Sons(position)[0])
    #     print(mtg.Sons(position))
    #     # print(Vector3(mtg.property('position')[position]))
    #     test = Vector3(mtg.property('position')[position])
    #
    # info_message(mtg.property('label'))
    # info_message(mtg.property('edge_type'))
    #
    # mylist = branches(mtg)
    # mylist = list(dict.fromkeys(mylist))
    #
    # for x in mylist:
    #     debug_message("start {0}".format(x.start))
    #     debug_message("end {0}".format(x.end))
    #     debug_message("age {0}\n".format(x.a))
    #
    # mytrunk = trunk(mtg)
    # debug_message("start {0}".format(mytrunk.start))
    # debug_message("end {0}".format(mytrunk.end))
    # debug_message("age {0}".format(mytrunk.a))


if __name__ == '__main__':
    main()
