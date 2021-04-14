from pyvis.network import Network
import networkx as nx

from openalea.plantgl.all import *

from Skeletonization.main import skeleton
from utilities.configuration_file import *

def main():
    input_point_cloud = "gen_2_23_03_expanded.ply"
    scene = Scene(INPUT_POINT_CLOUDS_DIR + input_point_cloud)
    points = scene[0].geometry.pointList
    
    mtg = skeleton(points)
    nx_graph = nx.cycle_graph(10)
    nx_graph.nodes("MTG(mtg)")


    nt = Network('500px', '500px')
    # populates the nodes and edges data structures
    nt.from_nx(nx_graph)
    nt.show('nx.html')


if __name__ == '__main__':
    main()